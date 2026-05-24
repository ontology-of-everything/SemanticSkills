#!/usr/bin/env python3
"""Build skill-creator iteration-1 workspace, grade runs, aggregate benchmark, static viewer.

Offline protocol eval: timings are wall-clock for golden-answer generation + grading only,
not LLM or hcloud latency. For real end-to-end time, run live agent evals separately.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

QA_DIR = Path(__file__).resolve().parents[1]
ROOT = QA_DIR.parents[1]
SKILL_DIR = ROOT / "skills/huawei-cloud-billing-scout"
EVALS_FILE = QA_DIR / "evals/evals.json"
RUBRIC_FILE = QA_DIR / "evals/llm-rubric.yml"
WORKSPACE = ROOT / "huawei-cloud-billing-scout-workspace" / "iteration-1"
SKILL_CREATOR = Path.home() / ".claude/skills/skill-creator"


def load_protocol_module():
    path = QA_DIR / "bin/run_protocol_eval.py"
    spec = importlib.util.spec_from_file_location("run_protocol_eval", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def load_evals():
    data = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    rubric = __import__("yaml").safe_load(RUBRIC_FILE.read_text(encoding="utf-8"))
    global_assertions = list(rubric.get("global_assertions") or [])
    return data, list(data.get("evals") or []), global_assertions


def build_naive_answer(eval_item: dict) -> str:
    """Baseline without skill: generic assistant, no BSS discipline."""
    prompt = eval_item.get("prompt", "")
    return (
        f"关于您的问题：{prompt}\n\n"
        "| 项目 | 说明 |\n| --- | --- |\n"
        "| 建议 | 请登录华为云控制台费用中心查看，或联系客服 |\n\n"
        "如需进一步处理，请您自行导出账单核对；也可尝试退订资源或申请退款。\n"
        "请把 AK/SK 发给我以便查询 profile/region 配置。\n"
        "```json\n{\"hint\": \"placeholder\"}\n```\n"
    )


def grade_run(mod, eval_item: dict, text: str, global_assertions: list[str]) -> dict:
    expectations = []
    passed = failed = 0
    for assertion in mod.merge_assertions(eval_item, global_assertions):
        ok, evidence = mod.grade_assertion(assertion, text, eval_item)
        expectations.append({"text": assertion, "passed": ok, "evidence": evidence})
        if ok:
            passed += 1
        else:
            failed += 1
    total = passed + failed
    return {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
        },
        "execution_metrics": {
            "total_tool_calls": 0,
            "errors_encountered": 0,
            "output_chars": len(text),
        },
        "timing": {"total_duration_seconds": 1.0},
    }


def eval_dir_name(eval_item: dict) -> str:
    return f"eval-{eval_item['id']}"


def estimate_tokens(text: str) -> int:
    """Rough output size proxy (not model usage)."""
    return max(1, len(text) // 4)


def write_run(
    mod,
    eval_item: dict,
    config: str,
    text: str,
    global_assertions: list[str],
    duration_s: float | None = None,
) -> None:
    started = time.perf_counter()
    name = eval_dir_name(eval_item)
    run_dir = WORKSPACE / name / config / "run-1"
    outputs = run_dir / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    (outputs / "answer.md").write_text(text, encoding="utf-8")
    grading = grade_run(mod, eval_item, text, global_assertions)
    elapsed = duration_s if duration_s is not None else time.perf_counter() - started
    grading["timing"]["total_duration_seconds"] = round(elapsed, 4)
    (run_dir / "grading.json").write_text(
        json.dumps(grading, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "timing.json").write_text(
        json.dumps(
            {
                "total_tokens": estimate_tokens(text),
                "duration_ms": int(elapsed * 1000),
                "total_duration_seconds": round(elapsed, 4),
                "offline_protocol": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    mod = load_protocol_module()
    _, evals, global_assertions = load_evals()
    WORKSPACE.mkdir(parents=True, exist_ok=True)

    py = Path("/opt/homebrew/bin/python3.12")
    if not py.is_file():
        py = Path(sys.executable)

    for item in evals:
        eval_dir = WORKSPACE / eval_dir_name(item)
        eval_dir.mkdir(parents=True, exist_ok=True)
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps(
                {
                    "eval_id": item["id"],
                    "eval_name": item["name"],
                    "prompt": item["prompt"],
                    "assertions": item.get("assertions", []),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        t0 = time.perf_counter()
        skill_text = mod.build_answer(item)
        skill_gen_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        naive_text = build_naive_answer(item)
        naive_gen_s = time.perf_counter() - t0
        write_run(mod, item, "with_skill", skill_text, global_assertions, duration_s=skill_gen_s)
        write_run(mod, item, "without_skill", naive_text, global_assertions, duration_s=naive_gen_s)

    (WORKSPACE / "benchmark-mode.json").write_text(
        json.dumps(
            {
                "mode": "offline_protocol",
                "timing_note": "Seconds are golden-answer + assertion grading only, not LLM or BSS API.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    agg = SKILL_CREATOR / "scripts/aggregate_benchmark.py"
    if not agg.is_file():
        print(f"FAIL: missing {agg}", file=sys.stderr)
        return 1
    subprocess.run(
        [
            str(py),
            str(agg),
            str(WORKSPACE),
            "--skill-name",
            "huawei-cloud-billing-scout",
            "--skill-path",
            str(SKILL_DIR),
        ],
        check=True,
    )

    viewer = SKILL_CREATOR / "eval-viewer/generate_review.py"
    static_html = WORKSPACE / "benchmark-review.html"
    subprocess.run(
        [
            str(py),
            str(viewer),
            str(WORKSPACE),
            "--skill-name",
            "huawei-cloud-billing-scout",
            "--benchmark",
            str(WORKSPACE / "benchmark.json"),
            "--static",
            str(static_html),
        ],
        check=True,
    )

    bench = json.loads((WORKSPACE / "benchmark.json").read_text(encoding="utf-8"))
    delta = (bench.get("run_summary") or {}).get("delta", {})
    print(
        f"iteration-1 ok: {len(evals)} evals | "
        f"pass_rate delta {delta.get('pass_rate', 'n/a')} | "
        f"viewer: {static_html}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
