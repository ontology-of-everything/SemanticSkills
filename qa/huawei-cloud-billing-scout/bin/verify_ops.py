#!/usr/bin/env python3
"""跨层校验：semantic/*.yml ↔ ops_contracts.yml ↔ related-commands.md ↔ 可选 hcloud --help。

函数式流水线：verify() 返回 Report → emit() 负责打印与 exit code。
纯计算在 check_op()；读盘/subprocess 仅在 main() 边界。
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import namedtuple
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("FAIL: PyYAML required (pip install pyyaml)")

# 校验结果：level 为 error | warn
Finding = namedtuple("Finding", "level message")
Report = namedtuple("Report", "findings mode op_count sem_count")

FLAG_RE = re.compile(r"(--[a-zA-Z0-9_.-]+)")
OP_LINE_RE = re.compile(r"hcloud\s+BSS\s+(\w+)")
OP_HEADING_RE = re.compile(r"^(`)?([A-Z][A-Za-z0-9]+)(`)?\s")
# KooCLI 通用参数，文档有但契约可省略
CLI_ONLY = frozenset({"--cli-output", "--cli-query", "--cli-read-timeout"})


def norm_flag(name: str) -> str:
    """统一 CLI 参数名：去默认值，数组下标归一化为 .[N]."""
    name = name.split("=")[0].strip()
    name = re.sub(r"\.\d+\.", ".[N].", name)
    return re.sub(r"\.\d+$", ".[N]", name)


def qa_defaults() -> tuple[Path, Path]:
    """未传参时的默认 skill 目录与契约文件路径。"""
    qa = Path(__file__).resolve().parent.parent
    skill = (qa / "../../skills/huawei-cloud-billing-scout").resolve()
    contracts = (qa / "fixtures/ops_contracts.yml").resolve()
    return skill, contracts


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def parse_semantic(skill_dir: Path) -> dict[str, tuple[str, frozenset[str]]]:
    """从 semantic YAML 提取 op → (实体名, 维度集合)。"""
    out: dict[str, tuple[str, frozenset[str]]] = {}
    for yml in sorted((skill_dir / "references/semantic").glob("*.yml")):
        data = load_yaml(yml)
        entity = data.get("name", yml.stem)
        dims = frozenset(d["name"] for d in data.get("dimensions") or [] if "name" in d)
        ops = []
        if data.get("source_operation"):
            ops.append(data["source_operation"].split("/")[-1])
        ops.extend(item.split("/")[-1] for item in data.get("source_operations") or [])
        for op in ops:
            prev = out.get(op)
            # 同一 Operation 被多实体引用时合并维度
            out[op] = (entity, dims if prev is None else prev[1] | dims)
    return out


def parse_doc_flags(text: str) -> dict[str, frozenset[str]]:
    """从 related-commands.md 按 Operation 提取文档中出现的 CLI 参数。"""
    acc: dict[str, set[str]] = {}
    for section in re.split(r"^## ", text, flags=re.M)[1:]:
        cur: str | None = None
        section_ops: set[str] = set()
        for line in section.splitlines():
            h = OP_HEADING_RE.match(line.strip())
            if h and h.group(2).startswith(("List", "Show")):
                cur = h.group(2)
                section_ops.add(cur)
            m = OP_LINE_RE.search(line)
            if m:
                cur = m.group(1)
                section_ops.add(cur)
            for flag in FLAG_RE.findall(line):
                target = cur or (next(iter(section_ops)) if len(section_ops) == 1 else None)
                if target:
                    acc.setdefault(target, set()).add(norm_flag(flag))
    return {k: frozenset(v) for k, v in acc.items()}


def contract_flags(contract: dict) -> frozenset[str]:
    """契约 YAML 中该 Operation 应覆盖的全部参数（必填 + 文档 + filter 绑定）。"""
    flags = {norm_flag(f) for f in contract.get("required_flags") or []}
    flags.update(norm_flag(f) for f in contract.get("documented_flags") or [])
    flags.update(norm_flag(str(v)) for v in (contract.get("filter_bindings") or {}).values())
    return frozenset(flags)


def fetch_help(op: str) -> frozenset[str] | None:
    """调用 hcloud BSS <op> --help；不可用时返回 None。"""
    try:
        proc = subprocess.run(
            ["hcloud", "BSS", op, "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    params: set[str] = set()
    for line in (proc.stdout + proc.stderr).splitlines():
        if m := re.match(r"\s+(--[a-zA-Z0-9_.\[\]-]+)", line):
            params.add(norm_flag(m.group(1)))
    return frozenset(params)


def flag_in_help(flag: str, help_params: frozenset[str]) -> bool:
    """匹配 help 参数，支持数组下标前缀模糊（如 filters.[N].key）。"""
    return flag in help_params or any(
        hp.startswith(flag.split(".[N].")[0]) for hp in help_params
    )


def err(msg: str) -> Finding:
    return Finding("error", msg)


def warn(msg: str) -> Finding:
    return Finding("warn", msg)


def check_op(
    op: str,
    contract: dict,
    entity: str,
    dims: frozenset[str],
    documented: frozenset[str],
    *,
    with_help: bool,
    warn_only_help: bool,
) -> list[Finding]:
    """单 Operation 三层对齐：契约 ↔ semantic ↔ related-commands ↔ 可选 help。"""
    f: list[Finding] = []
    if (ce := contract.get("entity")) and ce != entity:
        f.append(err(f"{op}: contract entity {ce} != semantic entity {entity}"))
    for dim in contract.get("filter_bindings") or {}:
        if dim not in dims:
            # 预期行为：如 enterprise_project_id 仅 CLI 过滤、不在 semantic 维度
            f.append(warn(f"{op}: filter_binding '{dim}' is CLI-only (not a semantic dimension)"))
    expected = contract_flags(contract)
    if not documented:
        f.append(err(f"{op}: no hcloud template flags found in related-commands.md"))
    f.extend(
        err(f"{op}: contract flag {flag} missing from related-commands.md")
        for flag in sorted(expected - documented)
    )
    if not with_help:
        return f
    help_p = fetch_help(op)
    if help_p is None:
        msg = f"{op}: skipped help check (hcloud unavailable or operation failed)"
        f.append(warn(msg) if warn_only_help else err(msg))
        return f
    f.extend(
        err(f"{op}: contract flag {flag} not found in hcloud --help")
        for flag in sorted(expected)
        if not flag_in_help(flag, help_p)
    )
    f.extend(
        warn(f"{op}: related-commands documents {flag} but contract omits it")
        for flag in sorted(documented - expected - CLI_ONLY)
        if flag_in_help(flag, help_p)
    )
    return f


def verify(
    skill_dir: Path,
    contracts_path: Path,
    *,
    with_help: bool,
    warn_only_help: bool,
) -> Report:
    """纯计算：汇总全部 Finding，不写 stdout。"""
    contracts = load_yaml(contracts_path).get("operations") or {}
    related = (skill_dir / "references/related-commands.md").read_text(encoding="utf-8")
    semantic = parse_semantic(skill_dir)
    doc_flags = parse_doc_flags(related)

    findings: list[Finding] = []
    sem_ops, con_ops = set(semantic), set(contracts)
    findings.extend(
        err(f"missing contract for semantic operation {op}") for op in sorted(sem_ops - con_ops)
    )
    findings.extend(
        err(f"contract operation {op} not referenced in semantic/*.yml")
        for op in sorted(con_ops - sem_ops)
    )
    for op, contract in sorted(contracts.items()):
        if op not in semantic:
            continue
        entity, dims = semantic[op]
        findings.extend(
            check_op(
                op,
                contract,
                entity,
                dims,
                doc_flags.get(op, frozenset()),
                with_help=with_help,
                warn_only_help=warn_only_help,
            )
        )

    mode = "static+help" if with_help else "static"
    return Report(tuple(findings), mode, len(contracts), len(semantic))


def emit(report: Report) -> int:
    """将 Report 打印到 stdout/stderr，返回进程 exit code。"""
    errors = [x for x in report.findings if x.level == "error"]
    for x in report.findings:
        line = f"{'WARN' if x.level == 'warn' else 'FAIL'}: {x.message}"
        print(line, file=sys.stderr if x.level == "error" else sys.stdout)
    if errors:
        print(f"operation verify failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        f"operation verify ok ({report.mode}): {report.op_count} operations, "
        f"{report.sem_count} semantic sources"
    )
    return 0


def find_command_template(related: str, operation: str) -> str | None:
    """在 related-commands.md 的 bash 代码块中查找含该 Operation 的首个模板。"""
    in_block, capture = False, []
    needle = f"hcloud BSS {operation}"
    for line in related.splitlines():
        s = line.strip()
        if s.startswith("```bash"):
            in_block, capture = True, []
        elif s == "```" and in_block:
            text = "\n".join(capture)
            if needle in text:
                return text.strip()
            in_block = False
        elif in_block:
            capture.append(line)
    return None


def print_command(skill_dir: Path, contracts_path: Path, operation: str) -> int:
    """维护者模式：打印 Operation 命令模板（文档优先，否则用契约必填参数拼装）。"""
    contracts = load_yaml(contracts_path).get("operations") or {}
    if operation not in contracts:
        print(f"unknown operation: {operation}", file=sys.stderr)
        print("available:", ", ".join(sorted(contracts)), file=sys.stderr)
        return 1
    related = (skill_dir / "references/related-commands.md").read_text(encoding="utf-8")
    if tpl := find_command_template(related, operation):
        print(tpl)
        return 0
    flags = contracts[operation].get("required_flags") or []
    print(" \\\n  ".join(["hcloud", "BSS", operation, *flags]))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("skill_dir", type=Path, nargs="?")
    p.add_argument("contracts", type=Path, nargs="?")
    p.add_argument("--with-help", action="store_true")
    p.add_argument("--warn-only-help", action="store_true")
    p.add_argument("--print-command", metavar="OPERATION")
    args = p.parse_args(argv)

    default_skill, default_contracts = qa_defaults()
    skill_dir = (args.skill_dir or default_skill).resolve()
    contracts_path = (args.contracts or default_contracts).resolve()

    if args.print_command:
        return print_command(skill_dir, contracts_path, args.print_command)

    with_help = args.with_help or os.environ.get("HUAWEICLOUD_BILLING_SCOUT_VERIFY_HELP", "0") == "1"
    report = verify(
        skill_dir,
        contracts_path,
        with_help=with_help,
        warn_only_help=args.warn_only_help or not with_help,
    )
    return emit(report)


if __name__ == "__main__":
    raise SystemExit(main())
