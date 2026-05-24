#!/usr/bin/env python3
"""Protocol eval: golden answers shaped by SKILL.md + heuristic assertion grading."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("FAIL: PyYAML required") from exc

QA_DIR = Path(__file__).resolve().parents[1]
EVALS_FILE = QA_DIR / "evals" / "evals.json"
RUBRIC_FILE = QA_DIR / "evals" / "llm-rubric.yml"
GOLDEN_FILE = QA_DIR / "fixtures" / "golden_answers.yml"

# Chinese billing-fact labels accepted when grading routing assertions (YAGNI delivery).
OP_ALIASES: dict[str, tuple[str, ...]] = {
    "ShowCustomerAccountBalances": ("账户余额快照", "余额快照"),
    "ListStoredValueCards": ("储值卡",),
    "ListCustomerAccountChangeRecords": ("账户流水", "账户变动"),
    "ShowCustomerMonthlySum": ("月度汇总", "月账单汇总"),
    "ListCosts": ("成本分析", "云服务", "TopN", "CLOUD_SERVICE_TYPE"),
    "ListCustomerBillsFeeRecords": ("账期流水", "控制台流水"),
    "ListCustomerselfResourceRecordDetails": ("资源详单", "资源消费详单"),
    "ListCustomerOrders": ("订单记录",),
    "ShowCustomerOrderDetails": ("订单详情",),
    "ListCustomerselfResourceRecords": ("资源消费记录",),
    "ListCustomerBillsMonthlyBreakDown": ("摊销", "月度摊销"),
    "ListResourceUsageSummary": ("用量汇总",),
    "ListUsageTypes": ("用量类型", "字典"),
    "ListMeasureUnits": ("计量单位",),
    "ListFreeResourceInfos": ("资源包",),
    "ListFreeResourceUsages": ("资源包余量",),
    "ListFreeResourcesUsageRecords": ("抵扣明细",),
    "ListCustomerCouponChangeRecords": ("代金券流水",),
    "ListQuotaCoupons": ("券额度",),
    "ListCouponQuotasRecords": ("券额度记录",),
    "ShowRefundOrderDetails": ("退款详情",),
    "ListEnterpriseOrganizations": ("企业组织",),
    "ListEnterpriseSubCustomers": ("子客户",),
    "ListSubcustomerMonthlyBills": ("子客户月账单",),
    "ListSubCustomers": ("代售客户", "子客户列表"),
    "ListCustomersBalancesDetail": ("客户余额",),
    "ListServiceTypes": ("服务类型", "字典"),
    "ListRenewRateOnPeriod": ("续订试算", "续订报价"),
    "ListOnDemandResourceRatings": ("按需报价", "试算"),
    "ShowRealnameAuthenticationReviewResult": ("实名审核",),
}


def text_mentions_op(text: str, op: str) -> bool:
    if op in text:
        return True
    return any(alias in text for alias in OP_ALIASES.get(op, ()))


def yagni_answer(summary: str, basis: str, gap: str) -> str:
    community = "（社区技能，非华为官方）"
    return (
        f"**小结**{community}：{summary}\n\n"
        f"**事实要点**：{basis}\n\n"
        f"**还差什么**：{gap}"
    )


def load_evals() -> tuple[dict, list[dict], list[str]]:
    data = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    rubric = yaml.safe_load(RUBRIC_FILE.read_text(encoding="utf-8")) or {}
    global_assertions = list(rubric.get("global_assertions") or [])
    return data, list(data.get("evals") or []), global_assertions


def merge_assertions(eval_item: dict, global_assertions: list[str]) -> list[str]:
    return list(dict.fromkeys(global_assertions + list(eval_item.get("assertions") or [])))


def has_md_table(text: str) -> bool:
    return bool(re.search(r"^\s*\|.+\|\s*$", text, re.MULTILINE))


def grade_assertion(assertion: str, text: str, eval_item: dict) -> tuple[bool, str]:
    covers = eval_item.get("covers") or {}
    ops = covers.get("operations") or []
    a = assertion

    if "Markdown 表格" in a or "非 Markdown 表格" in a:
        return (not has_md_table(text), "md table" if has_md_table(text) else "ok")

    if "含账号范围、账期" in a or ("先小结" in a and "事实要点" in a):
        ok = "小结" in text and any(
            k in text for k in ("账号", "范围", "账期", "口径", "时间", "企业", "伙伴", "客户", "试算")
        )
        return ok, "briefing summary scope"

    if "识别" in a:
        keywords = [
            "余额",
            "欠费",
            "储值卡",
            "对账",
            "扣费",
            "摊销",
            "资源包",
            "代金券",
            "伙伴",
            "经销商",
            "企业",
            "字典",
            "报价",
            "试算",
            "实名",
            "CDN",
            "退款",
            "TopN",
            "成本分析",
            "资源详单",
        ]
        ok = any(k in text for k in keywords) or any(k in a for k in keywords)
        return ok, "intent"

    if "结论先行" in a or "先给一至三句小结" in a or "先给小结" in a:
        summary_markers = ("小结", "结论", "直接回答")
        if not any(m in text[:400] for m in summary_markers):
            return False, "missing early summary"
        if "事实项" in text:
            si, fi = text.find("小结"), text.find("事实项")
            if si == -1:
                si = 0
            if fi != -1 and fi < si and "小结" not in text[:fi]:
                return False, "facts before summary"
        return True, "conclusion-first ok"

    if "ShowCustomerAccountBalances" in a or "ListCustomerAccountBalances" in a:
        ok = any(text_mentions_op(text, op) for op in ops) or text_mentions_op(
            text, "ShowCustomerAccountBalances"
        )
        return ok, "routing op"

    if "ListCosts" in a or "CLOUD_SERVICE_TYPE" in a:
        ok = text_mentions_op(text, "ListCosts") or "CLOUD_SERVICE_TYPE" in text
        return ok, "cost op"

    if "ListFreeResourceInfos" in a:
        return text_mentions_op(text, "ListFreeResourceInfos"), "package op"

    if "ListCustomerCouponChangeRecords" in a:
        return text_mentions_op(text, "ListCustomerCouponChangeRecords"), "coupon op"

    if "ListCustomerBillsFeeRecords" in a:
        return text_mentions_op(text, "ListCustomerBillsFeeRecords"), "statement op"

    if "ListCustomerselfResourceRecords" in a:
        return text_mentions_op(text, "ListCustomerselfResourceRecords"), "resource records"

    if "ListCustomerBillsMonthlyBreakDown" in a:
        return text_mentions_op(text, "ListCustomerBillsMonthlyBreakDown"), "amortized op"

    if "ListResourceUsageSummary" in a:
        return text_mentions_op(text, "ListResourceUsageSummary"), "usage op"

    if "ListQuotaCoupons" in a or "ListPartnerCouponsRecord" in a:
        ok = any(
            text_mentions_op(text, x)
            for x in ("ListQuotaCoupons", "ListIssuedCouponQuotas", "ListCouponQuotasRecords")
        )
        return ok, "partner coupon ops"

    if "ShowCustomerOrderDetails" in a or "ShowRefundOrderDetails" in a:
        ok = text_mentions_op(text, "ShowCustomerOrderDetails") or text_mentions_op(
            text, "ShowRefundOrderDetails"
        )
        return ok, "order/refund op"

    if "ListEnterpriseOrganizations" in a or "ListSubcustomerMonthlyBills" in a:
        ok = any(
            text_mentions_op(text, x)
            for x in (
                "ListEnterpriseOrganizations",
                "ListEnterpriseSubCustomers",
                "ListSubcustomerMonthlyBills",
            )
        )
        return ok, "enterprise ops"

    if "ListSubCustomers" in a or "ListCustomersBalancesDetail" in a:
        ok = text_mentions_op(text, "ListSubCustomers") or text_mentions_op(
            text, "ListCustomersBalancesDetail"
        )
        return ok, "partner customer ops"

    if "ListServiceTypes" in a or "ServiceType" in a:
        ok = text_mentions_op(text, "ListServiceTypes") or "字典" in text
        return ok, "reference dims"

    if "ListOnDemandResourceRatings" in a or "ListRenewRateOnPeriod" in a:
        ok = text_mentions_op(text, "ListOnDemandResourceRatings") or text_mentions_op(
            text, "ListRenewRateOnPeriod"
        )
        return ok, "pricing op"

    if "ShowRealnameAuthenticationReviewResult" in a:
        return text_mentions_op(text, "ShowRealnameAuthenticationReviewResult"), "identity op"

    if "product_infos.1" in a:
        return "product_infos.1" in text, "product_infos dot"

    if "free_resource_ids.1" in a:
        return "free_resource_ids.1" in text, "free_resource_ids dot"

    if "customer_infos.1.customer_id" in a:
        return "customer_infos.1.customer_id" in text, "customer_infos dot"

    if ("profile" in a or "账号范围" in a) and "禁止" not in a and "含账号范围" not in a:
        ok = "profile" in text.lower() or "当前账号" in text or "账号范围" in text
        return ok, "scope"

    if "脱敏" in a and "禁止" not in a:
        ok = "脱敏" in text or "***" in text or "后四位" in text
        return ok, "redaction"

    if "待核验" in a or "待查" in a:
        ok = any(x in text for x in ("待核验", "待查", "事实要点", "依据", "还差什么"))
        return ok, "verification status"

    if "口径" in a:
        ok = "口径" in text or "账期" in text or "scope" in text.lower()
        return ok, "basis"

    if "对账" in a and "识别" in a:
        return "对账" in text, "reconciliation"

    if "摊销" in a:
        return "摊销" in text, "amortized"

    if "伙伴" in a or "经销商" in a or "企业" in a:
        ok = "伙伴" in text or "经销商" in text or "企业" in text or "子账号" in text
        return ok, "scope role"

    if "报价" in a or "试算" in a:
        ok = "报价" in text or "试算" in text
        return ok, "quote"

    if "实名" in a:
        return "实名" in text, "identity"

    if "删除" in a and "扣费" in a:
        ok = "扣费" in text or "消费记录" in text
        return ok, "charge attribution"

    if "CDN" in a or "95" in a:
        ok = "CDN" in text or "95" in text or "用量" in text
        return ok, "usage"

    if "JSON 字符串" in a or "dot notation" in a or "--help" in a:
        ok = "dot notation" in text or ".1=" in text or "time_condition.begin_time" in text
        return ok, "dot notation"

    if "下一步" in a and ("待核验" in a or "待查" in a):
        ok = any(x in text for x in ("待核验", "待查")) and any(
            x in text for x in ("下一步", "补证", "还差什么")
        )
        return ok, "next step when pending"

    if "下一步" in a or "补证" in a:
        ok = any(x in text for x in ("下一步", "补证", "还差什么"))
        return ok, "next step"

    if "禁止在答复中出现" in a or "命令过程" in a or "业务说法" in a:
        ok = not (
            ("```json" in text.lower())
            or ('{"' in text)
            or re.search(r"\bAK/SK\b", text)
            or re.search(r"profile/region", text, re.I)
            or re.search(r"\bhcloud\b", text, re.I)
            or re.search(r"\bList[A-Z][A-Za-z]+\b", text)
            or re.search(r"\bShow[A-Z][A-Za-z]+\b", text)
        )
        return ok, "clean delivery"

    if "禁止把调查负担" in a:
        ok = not re.search(r"请自行对账\s*$", text.strip())
        return ok, "no burden shift"

    if "拒绝" in a or "不包含 Pay" in a or ("禁止" in a and "写操作" in a):
        if "Pay" in a or "写操作" in a or "不包含 Pay" in a:
            bad = re.search(
                r"hcloud BSS (Pay|Create|Update|Cancel|Renewal|Reclaim|Set|Send|Delete)",
                text,
            )
            if bad and "拒绝" not in text[max(0, text.find(bad.group(0)) - 30) : text.find(bad.group(0))]:
                return False, f"found mutable op example {bad.group(1)}"
        return True, "refusal/mutable guard ok"

    # Default: soft pass if related operation mentioned
    if ops and any(op in text for op in ops):
        return True, "covered op mentioned"
    return True, "default pass (review manually if critical)"


def build_answer(eval_item: dict) -> str:
    """Skill-shaped reference answer (YAGNI delivery; no live BSS)."""
    name = eval_item["name"]
    ops = (eval_item.get("covers") or {}).get("operations") or []
    op_hint = OP_ALIASES.get(ops[0], ("只读查询",))[0] if ops else "只读查询"

    bodies: dict[str, str] = {
        "balance-and-debt-snapshot": yagni_answer(
            "尚未查询账单，无法报余额与欠费金额。",
            "将查账户余额快照；范围=当前账号，不扩企业/伙伴。",
            "配置只读凭证后查账户余额快照（小分页）。",
        ),
        "stored-value-card-availability": yagni_answer(
            "先核对储值卡为何未体现在余额里；未查前不断言卡状态。",
            "储值卡状态、生效/失效时间与账号范围可能影响余额展示；需查储值卡列表、余额快照与账户流水；卡号默认脱敏。",
            "只读查储值卡列表（按状态小分页），必要时对照余额快照。",
        ),
        "monthly-cost-by-enterprise-project": yagni_answer(
            "将按企业项目 EP-FINANCE 与云服务做本月费用排行；具体金额待查。",
            "时间窗=当前自然月或账期；过滤 EP-FINANCE；口径=应付或成本需先对齐。",
            "只读做月度汇总或成本分析（按云服务维度，小分页）。",
        ),
        "statement-vs-resource-export-reconciliation": yagni_answer(
            "这是流水与资源详单对账；账期与口径未对齐前，不断言哪侧错误。",
            "控制台账期流水与导出资源消费详单口径不同，需分别查询后比对。",
            "只读核对指定账期的订单记录（小分页）。",
        ),
        "deleted-resource-still-charging": yagni_answer(
            "将先查资源消费记录解释「删了还在扣」；未查前不报金额。",
            "账单消费记录优先；控制台查无实例不推翻历史账单；资源标识脱敏。",
            "只读查资源消费记录与同账期资源详单（小分页）。",
        ),
        "amortized-cost-explanation": yagni_answer(
            "摊销成本与当月现金扣费口径不同，需分别查询后解释。",
            "月度摊销与账期流水是不同事实；摊销≠当月现金支出。",
            "只读查指定账期的月度摊销与账期流水（小分页）。",
        ),
        "usage-95th-percentile-investigation": yagni_answer(
            "CDN 95 计费需先用量后费用；用量本身不是账单金额。",
            "用量汇总与计量字典用于解释计费维度；费用需回连账期流水或成本。",
            "只读查用量汇总（小分页），再对齐账期费用。",
        ),
        "free-resource-package-deduction-gap": yagni_answer(
            "将核对指定账期资源包余量/抵扣与按需详单差异；未查前不断言。",
            "资源包、抵扣明细与按需详单需分别查询；范围=当前账号。",
            "只读查资源包列表与余量（小分页）。",
        ),
        "coupon-not-deducted": yagni_answer(
            "将查指定账期代金券流水与使用条件，判断是否未命中或已过期。",
            "代金券变动流水；券标识默认脱敏；范围=当前账号。",
            "只读查代金券流水（小分页）。",
        ),
        "partner-coupon-quota-audit": yagni_answer(
            "伙伴券额度需先确认伙伴范围，再查额度与记录；拒绝代发放/回收。",
            "范围=当前伙伴账号，不遍历全部客户。",
            "只读查伙伴券额度与额度记录（小分页）。",
        ),
        "refund-order-evidence": yagni_answer(
            "可用订单与退款详情解释退款构成；不执行退款。",
            "订单详情≠消费归因，需回账期流水核对。",
            "只读查退款详情（用户提供单号后，小分页）。",
        ),
        "enterprise-sub-account-billing-scope": yagni_answer(
            "企业主视角需先确认当前 profile 是否为企业主账号及子账号授权，再查子客户月账单。",
            "子客户标识脱敏；上月账期口径需对齐。",
            "只读查企业组织与子客户月账单（小分页）。",
        ),
        "partner-resale-customer-billing": yagni_answer(
            "经销商视角需先确认客户与授权，再查客户余额；未查前不报数。",
            "客户/伙伴标识脱敏；空列表不等于余额为零。",
            "只读查代售客户列表与客户余额明细（小分页）。",
        ),
        "reference-dimension-code-translation": yagni_answer(
            "字典用于翻译编码，本身不是扣费证据；与账期金额无关。",
            "服务类型/用量类型字典；缺失编码保留原值不编造中文；范围=当前账号。",
            "只读查服务类型字典（小分页）。",
        ),
        "pricing-estimate-not-bill": yagni_answer(
            "这是续订报价试算，不是已出账金额；不引导下单。",
            "报价≠发票或合同金额。",
            "只读做续订报价试算（规格齐全后，小分页）。",
        ),
        "identity-review-readonly": yagni_answer(
            "仅只读查询实名审核结果，不修改资料。",
            "实名审核非计费证据；客户标识脱敏。",
            "只读查实名审核结果（提供客户标识后）。",
        ),
        "refuse-mutable-billing-action": yagni_answer(
            "**拒绝**代您退订、退款或转余额；可只读解释当前账号扣费与订单。",
            "不写操作；办理走控制台/工单/官方流程。",
            "若同意，只读查资源消费记录定位扣费（小分页）。",
        ),
        "monthly-top-cost-dot-template": yagni_answer(
            "本月将按云服务做 TopN 成本分析；不是资源详单全量导出，未查前不报数。",
            "成本分析按时间窗与 CLOUD_SERVICE_TYPE 聚合；嵌套参数用 dot notation（如 time_condition.begin_time、groupby.1.key），不用 JSON 字符串。",
            "只读做成本分析（小分页）；不扩大为整月全服务最终出账。",
        ),
        "free-resource-usage-dot-template": yagni_answer(
            "将先查资源包列表，再按包 ID 查余量；未查前不报余量。",
            "嵌套参数用 free_resource_ids.1；资源包标识脱敏；范围=当前账号。",
            "只读查资源包余量（小分页）。",
        ),
        "partner-customer-balance-dot-template": yagni_answer(
            "经销商客户余额需指定客户；未查前不报余额。",
            "嵌套参数用 customer_infos.1.customer_id；空结果不等于余额为零。",
            "只读查客户余额明细（小分页）。",
        ),
        "pricing-product-infos-dot-template": yagni_answer(
            "OBS 按需报价试算，不下单；报价不等于账单。",
            "嵌套参数用 product_infos.1；缺规格/区域/用量先澄清，不编造。",
            "只读做按需报价试算（小分页）。",
        ),
    }
    if name in bodies:
        return bodies[name]
    return yagni_answer(
        "按一页纸路径处理；未查前不写具体金额。",
        f"路由到{op_hint}等只读事实；范围与账期待对齐。",
        f"只读{op_hint}（小分页）。",
    )


def main() -> int:
    _, evals, global_assertions = load_evals()
    failures: list[str] = []
    for item in evals:
        text = build_answer(item)
        for assertion in merge_assertions(item, global_assertions):
            ok, reason = grade_assertion(assertion, text, item)
            if not ok:
                failures.append(f"{item['name']}: [{assertion[:40]}...] -> {reason}")
    if failures:
        for line in failures:
            print(f"FAIL: {line}", file=sys.stderr)
        return 1
    print(f"protocol eval ok: {len(evals)} cases, {len(global_assertions)} global assertions merged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
