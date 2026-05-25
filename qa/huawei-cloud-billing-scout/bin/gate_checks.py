"""Deterministic layout, ripgrep, and documentation checks."""

from __future__ import annotations

import sys
from pathlib import Path

from qa_common import (
    CONTRACTS_FILE,
    DOC_FILE,
    EVALS_FILE,
    QA_DIR,
    ROOT,
    SKILL_DIR,
    expected_version,
    load_json,
    load_yaml,
    parse_skill_frontmatter,
    run_rg,
)

REQUIRED_FILES = (
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "references/cli-installation.md",
    SKILL_DIR / "references/iam-policies.md",
    SKILL_DIR / "references/related-commands.md",
    SKILL_DIR / "references/semantic/catalog.yml",
    SKILL_DIR / "references/semantic/billing-ontology.yml",
    DOC_FILE,
    ROOT / "docs/catalog.yml",
    ROOT / "docs/agents/cursor.md",
    ROOT / "docs/agents/claude-code.md",
    ROOT / "docs/agents/codex.md",
    QA_DIR / "README.md",
    QA_DIR / "assertions/README.md",
    QA_DIR / "bin/gate.py",
    QA_DIR / "bin/verify_ops.py",
    EVALS_FILE,
    CONTRACTS_FILE,
)

FORBIDDEN_SKILL_PATHS = (
    ".DS_Store",
    ".agents",
    "analysis",
    "evals",
    "qa",
    "tests",
    ".workspaces",
)

LEGACY_SEMANTIC = (
    "AccountBalance.yml",
    "AccountChangeRecord.yml",
    "AmortizedCost.yml",
    "BillingStatement.yml",
    "CostAnalysis.yml",
    "CouponChangeRecord.yml",
    "CouponQuota.yml",
    "EnterpriseAndPartnerContext.yml",
    "FreeResourcePackage.yml",
    "MonthlyBillSummary.yml",
    "OrderEvidence.yml",
    "PricingAndIdentity.yml",
    "ReferenceDimensions.yml",
    "ResourceBillDetail.yml",
    "ResourceBillRecord.yml",
    "ResourceUsage.yml",
    "StoredValueCard.yml",
)

QA_FILES_FORBIDDEN_IN_SKILL = (
    "gate.py",
    "skillcheck.toml",
    "policy.skill-scanner.yaml",
    ".markdownlint.json",
)


def check_layout() -> None:
    for path in REQUIRED_FILES:
        if not path.is_file():
            raise SystemExit(f"FAIL: missing file: {path}")
    stale = [
        SKILL_DIR / "references/billing-playbook.md",
        SKILL_DIR / "references/billing-semantics.md",
    ]
    for path in stale:
        if path.exists():
            raise SystemExit(f"FAIL: stale file should be removed: {path.name}")
    for name in LEGACY_SEMANTIC:
        path = SKILL_DIR / "references/semantic" / name
        if path.exists():
            raise SystemExit(f"FAIL: stale semantic shard still exists: {name}")
    for name in FORBIDDEN_SKILL_PATHS:
        if (SKILL_DIR / name).exists():
            raise SystemExit(f"FAIL: forbidden runtime bundle path: {name}")
    skills_parent = SKILL_DIR.parent
    for path in skills_parent.iterdir():
        if path.is_dir() and path.name.endswith("-workspace"):
            raise SystemExit(
                f"FAIL: Skill Creator workspace belongs at repo root, not skills/: {path.name}"
            )
    for name in QA_FILES_FORBIDDEN_IN_SKILL:
        if (SKILL_DIR / name).exists():
            raise SystemExit(f"FAIL: QA gate file must not live in skills/: {name}")
    if list(SKILL_DIR.rglob(".DS_Store")):
        raise SystemExit("FAIL: remove .DS_Store from skills/huawei-cloud-billing-scout")


def _fail_hits(hits: str, message: str) -> None:
    if hits:
        print(hits, file=sys.stderr)
        raise SystemExit(f"FAIL: {message}")


def check_text_guards() -> None:
    doc_paths = [DOC_FILE, SKILL_DIR, ROOT / "README.md", ROOT / "README-CN.md"]
    _fail_hits(
        run_rg("billing-semantics|Semantic entities \\(8\\)", doc_paths),
        "stale documentation text",
    )
    guard_paths = [
        SKILL_DIR,
        DOC_FILE,
        QA_DIR / "README.md",
        QA_DIR / "assertions/README.md",
        QA_DIR / "bin/verify_ops.py",
        CONTRACTS_FILE,
    ]
    _fail_hits(
        run_rg("billing-playbook\\.md|Catalog\\.yml", guard_paths),
        "stale playbook or uppercase catalog reference",
    )
    _fail_hits(
        run_rg("playbook_section|总体判断、分层事实", [SKILL_DIR / "references/semantic/catalog.yml"]),
        "stale catalog.yml routing text",
    )
    catalog = SKILL_DIR / "references/semantic/catalog.yml"
    count_line = run_rg("^name: HuaweiCloudBillingSemanticCatalog$", [catalog], count=True)
    count = int(count_line.rsplit(":", 1)[-1]) if count_line else 0
    if count != 1:
        raise SystemExit("FAIL: catalog.yml must contain exactly one root name block")
    marketplace_paths = [DOC_FILE, ROOT / "docs", ROOT / "README.md", ROOT / "README-CN.md"]
    _fail_hits(
        run_rg("≥2 stars|repo \\*\\*≥2|--agent claude($|[[:space:]])", marketplace_paths),
        "stale marketplace guidance",
    )
    _fail_hits(
        run_rg("--dry-run", [DOC_FILE, ROOT / "README.md", ROOT / "README-CN.md"]),
        "unsupported ClawHub skill publish dry-run guidance",
    )
    _fail_hits(
        run_rg(
            "hcloud[[:space:]]+BSS[[:space:]]+"
            "(Pay|Create|Update|Cancel|Renewal|Reclaim|Set|Send|Delete|Change|Claim|AutoRenewal)"
            "[A-Za-z0-9]+",
            [SKILL_DIR, DOC_FILE],
        ),
        "mutable BSS command example found",
    )


def _semantic_entity_names(skill: Path) -> set[str]:
    names: set[str] = set()
    for path in sorted((skill / "references/semantic").glob("*.yml")):
        if path.name == "catalog.yml":
            continue
        obj = load_yaml(path)
        if obj.get("name") and obj.get("type") != "semantic_ontology":
            names.add(str(obj["name"]))
        for entity in obj.get("entities", []) or []:
            if isinstance(entity, dict) and entity.get("name"):
                names.add(str(entity["name"]))
    return names


def _require_needles(text: str, needles: list[str], label: str) -> None:
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"FAIL: {label} missing: {needle}")


def _check_frontmatter(frontmatter: dict) -> None:
    if frontmatter.get("name") != "huawei-cloud-billing-scout":
        raise SystemExit("FAIL: SKILL.md name mismatch")
    desc = str(frontmatter.get("description", ""))
    if "储值卡" not in desc and "stored-value" not in desc.lower():
        raise SystemExit("FAIL: SKILL.md description missing stored-value card trigger")
    if "license" in frontmatter:
        raise SystemExit("FAIL: SKILL.md must omit license to avoid ClawHub MIT-0 conflict")
    openclaw = (frontmatter.get("metadata") or {}).get("openclaw") or {}
    requires = openclaw.get("requires") or {}
    if "hcloud" not in requires.get("bins", []):
        raise SystemExit("FAIL: metadata.openclaw.requires.bins must include hcloud")
    if "SemanticSkills/tree/main/skills/huawei-cloud-billing-scout" not in openclaw.get("homepage", ""):
        raise SystemExit("FAIL: metadata.openclaw.homepage should point to the skill directory")
    env_vars = {item.get("name"): item for item in openclaw.get("envVars", []) if isinstance(item, dict)}
    for name in ("HUAWEICLOUD_SDK_AK", "HUAWEICLOUD_SDK_SK", "HUAWEICLOUD_SDK_REGION"):
        if name not in env_vars or env_vars[name].get("required") is not False:
            raise SystemExit(f"FAIL: metadata.openclaw.envVars {name} must be optional")


def _check_catalog_entry(entry: dict | None, version: str) -> None:
    if not entry:
        raise SystemExit("FAIL: docs/catalog.yml missing huawei-cloud-billing-scout")
    if entry.get("path") != "skills/huawei-cloud-billing-scout" or entry.get("qa") != "qa/huawei-cloud-billing-scout":
        raise SystemExit("FAIL: docs/catalog.yml path/qa mismatch")
    if entry.get("version") != version:
        raise SystemExit(f"FAIL: docs/catalog.yml version should match VERSION ({version})")
    if entry.get("distribution") != "direct-skill":
        raise SystemExit("FAIL: docs/catalog.yml distribution should be direct-skill")
    if "openclaw" not in entry.get("agents", []):
        raise SystemExit("FAIL: docs/catalog.yml agents should include openclaw")
    if "MIT-0" not in entry.get("clawhub_license", ""):
        raise SystemExit("FAIL: docs/catalog.yml should document ClawHub MIT-0 terms")


def _check_evals(data: dict, semantic_entities: set[str], contracts: dict) -> int:
    if data.get("skill_name") != "huawei-cloud-billing-scout":
        raise SystemExit("FAIL: eval skill_name mismatch")
    evals = data.get("evals")
    if not isinstance(evals, list) or len(evals) < 24:
        raise SystemExit("FAIL: expected at least 24 eval cases")
    domains: set[str] = set()
    entities: set[str] = set()
    names: set[str] = set()
    required_keys = {"id", "name", "prompt", "expected_output", "files", "assertions", "covers"}
    for item in evals:
        missing = required_keys - item.keys()
        if missing:
            raise SystemExit(f"FAIL: eval {item.get('id')} missing {sorted(missing)}")
        if item["name"] in names:
            raise SystemExit(f"FAIL: duplicate eval name: {item['name']}")
        names.add(item["name"])
        assertions = item["assertions"]
        if not isinstance(assertions, list) or len(assertions) < 4 or len(set(assertions)) != len(assertions):
            raise SystemExit(f"FAIL: eval {item['name']} needs >=4 unique assertions")
        domains.update(item["covers"].get("domains", []))
        entities.update(item["covers"].get("entities", []))
    expected_domains = {
        str(spec.get("domain"))
        for spec in (contracts.get("operations") or {}).values()
        if isinstance(spec, dict) and spec.get("domain")
    }
    if domains != expected_domains:
        raise SystemExit(f"FAIL: eval domain coverage mismatch: {sorted(expected_domains - domains)}")
    missing_entities = semantic_entities - entities
    if missing_entities:
        raise SystemExit(f"FAIL: eval entity coverage missing: {sorted(missing_entities)}")
    llm_eval = data.get("llm_eval") or {}
    if llm_eval.get("rubric") != "evals/llm-rubric.yml":
        raise SystemExit("FAIL: evals.json llm_eval.rubric must be evals/llm-rubric.yml")
    rubric = load_yaml(QA_DIR / "evals/llm-rubric.yml")
    if len(rubric.get("dimensions") or []) < 4:
        raise SystemExit("FAIL: llm-rubric.yml needs >=4 dimensions")
    if len(rubric.get("global_assertions") or []) < 3:
        raise SystemExit("FAIL: llm-rubric.yml needs >=3 global_assertions")
    export_script = QA_DIR / (llm_eval.get("export") or "")
    if not export_script.is_file():
        raise SystemExit(f"FAIL: missing export script: {export_script}")
    return len(evals)


def check_docs_and_evals() -> tuple[int, int]:
    skill = SKILL_DIR
    for path in sorted((skill / "references/semantic").glob("*.yml")) + [ROOT / "docs/catalog.yml"]:
        load_yaml(path)
    _check_frontmatter(parse_skill_frontmatter())
    version = expected_version()
    catalog = load_yaml(ROOT / "docs/catalog.yml")
    entry = next((item for item in catalog.get("skills", []) if item.get("id") == "huawei-cloud-billing-scout"), None)
    _check_catalog_entry(entry, version)
    _require_needles(
        DOC_FILE.read_text(encoding="utf-8"),
        [
            "install payload", "billing-ontology.yml", "catalog.yml",
            "58 unique read-only BSS query operations", "validate.sh", "bin/gate.py",
            "clawhub skill publish", "clawscan-note", "claude-code-skill", "MIT-0",
            "答复格式", "briefing-style", "IM-safe", "hermes.md",
        ],
        "skill docs",
    )
    skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
    _require_needles(
        skill_text,
        [
            "evidence_boundary", "答复", "不转交调查负担", "完整业务 ID",
            "`profile`", "未查不写", "请自行对账", "业务称呼", "业务说法",
            "只问会改变查证路径", "一次一问", "查证路径",
        ],
        "SKILL.md output contract guard",
    )
    if not any(token in skill_text for token in ("0 元或低金额", "不得扩大成整月", "最终出账")):
        raise SystemExit("FAIL: SKILL.md missing low-amount / scope ceiling guard")
    repo_docs = "\n".join(
        (ROOT / rel).read_text(encoding="utf-8")
        for rel in (
            "README.md", "README-CN.md", "docs/authoring.md",
            "docs/agents/cursor.md", "docs/agents/claude-code.md",
            "docs/agents/codex.md", "docs/agents/hermes.md",
        )
    )
    _require_needles(
        repo_docs,
        [
            "clawhub skill publish", "claude-skills", "--agent claude-code",
            "--agent codex", "hermes skills install", "Interaction discipline",
            "一次只问一事",
        ],
        "repo docs marketplace guidance",
    )
    data = load_json(EVALS_FILE)
    contracts = load_yaml(CONTRACTS_FILE)
    semantic_entities = _semantic_entity_names(skill)
    eval_count = _check_evals(data, semantic_entities, contracts)
    return eval_count, len(semantic_entities)
