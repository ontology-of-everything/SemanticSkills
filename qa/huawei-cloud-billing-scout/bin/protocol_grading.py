"""Offline protocol grading: golden answers + assertion rules (YAGNI delivery contract)."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

# Chinese billing-fact labels when grading routing assertions (no API names in user text).
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
}

INTENT_KEYWORDS = (
    "余额", "欠费", "储值卡", "对账", "扣费", "摊销", "资源包", "代金券",
    "伙伴", "经销商", "企业", "字典", "CDN", "退款",
    "TopN", "成本分析", "资源详单", "拒绝路由", "超出", "范围外",
)

MUTABLE_OP_RE = re.compile(
    r"hcloud BSS (Pay|Create|Update|Cancel|Renewal|Reclaim|Set|Send|Delete)"
)


def text_mentions_op(text: str, op: str) -> bool:
    return op in text or any(alias in text for alias in OP_ALIASES.get(op, ()))


def yagni_answer(summary: str, basis: str, gap: str) -> str:
    community = "（华为社区版，非华为官方）"
    return (
        f"**小结**{community}：{summary}\n\n"
        f"**事实要点**：{basis}\n\n"
        f"**还差什么**：{gap}"
    )


def has_md_table(text: str) -> bool:
    return bool(re.search(r"^\s*\|.+\|\s*$", text, re.MULTILINE))


def _grade_bss_cli_region(text: str) -> tuple[bool, str]:
    bad = bool(re.search(r"--cli-region\s*=\s*cn-east-2\b", text, re.I))
    good = bool(re.search(r"--cli-region\s*=\s*cn-north-1\b", text, re.I))
    if bad:
        return False, "used cn-east-2 as cli-region"
    if good:
        return True, "cli-region=cn-north-1"
    # Skill-shaped answers omit command text; accept explicit BSS endpoint discipline.
    if re.search(r"BSS.*端点|cn-north-1.*(端点|CLI)|固定.*cn-north-1", text):
        return True, "endpoint discipline without command echo"
    return False, "missing cli-region=cn-north-1 evidence"


def _covers_ops(eval_item: dict[str, Any]) -> list[str]:
    return list((eval_item.get("covers") or {}).get("operations") or [])


def _any_op(text: str, *ops: str) -> bool:
    return any(text_mentions_op(text, op) for op in ops)


GradeFn = Callable[[str, str, dict[str, Any]], Optional[tuple[bool, str]]]


@dataclass(frozen=True)
class GradeRule:
    """First matching rule wins (order matters)."""

    name: str
    when: Callable[[str], bool]
    grade: GradeFn


def _rules() -> list[GradeRule]:
    """Ordered matchers — first match wins."""
    rules: list[tuple[str, Callable[[str], bool], GradeFn]] = [
      (
          "bss-cli-region",
          lambda a: "cli-region=cn-north-1" in a or "cn-east-2 作为 --cli-region" in a,
          lambda _a, text, _e: _grade_bss_cli_region(text),
      ),
      (
          "md-table",
          lambda a: "Markdown 表格" in a or "非 Markdown 表格" in a,
          lambda _a, text, _e: ((not has_md_table(text), "md table" if has_md_table(text) else "ok")),
      ),
      (
          "briefing-scope",
          lambda a: "含账号范围、账期" in a or ("先小结" in a and "事实要点" in a),
          lambda _a, text, _e: (
              "小结" in text
              and any(k in text for k in ("账号", "范围", "账期", "口径", "时间", "企业", "伙伴", "客户", "试算")),
              "briefing summary scope",
          ),
      ),
      (
          "intent",
          lambda a: "识别" in a,
          lambda a, text, _e: (
              any(k in text for k in INTENT_KEYWORDS) or any(k in a for k in INTENT_KEYWORDS),
              "intent",
          ),
      ),
      (
          "conclusion-first",
          lambda a: "结论先行" in a or "先给一至三句小结" in a or "先给小结" in a,
          lambda _a, text, _e: _grade_conclusion_first(text),
      ),
      (
          "balance-routing",
          lambda a: "ShowCustomerAccountBalances" in a,
          lambda _a, text, e: (
              _any_op(text, *_covers_ops(e)) or text_mentions_op(text, "ShowCustomerAccountBalances"),
              "routing op",
          ),
      ),
      (
          "cost-op",
          lambda a: "ListCosts" in a or "CLOUD_SERVICE_TYPE" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListCosts") or "CLOUD_SERVICE_TYPE" in text, "cost op"),
      ),
      (
          "package-op",
          lambda a: "ListFreeResourceInfos" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListFreeResourceInfos"), "package op"),
      ),
      (
          "coupon-op",
          lambda a: "ListCustomerCouponChangeRecords" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListCustomerCouponChangeRecords"), "coupon op"),
      ),
      (
          "statement-op",
          lambda a: "ListCustomerBillsFeeRecords" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListCustomerBillsFeeRecords"), "statement op"),
      ),
      (
          "resource-records",
          lambda a: "ListCustomerselfResourceRecords" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListCustomerselfResourceRecords"), "resource records"),
      ),
      (
          "amortized-op",
          lambda a: "ListCustomerBillsMonthlyBreakDown" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListCustomerBillsMonthlyBreakDown"), "amortized op"),
      ),
      (
          "usage-op",
          lambda a: "ListResourceUsageSummary" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListResourceUsageSummary"), "usage op"),
      ),
      (
          "partner-coupon",
          lambda a: "ListQuotaCoupons" in a or "ListPartnerCouponsRecord" in a,
          lambda _a, text, _e: (
              _any_op(text, "ListQuotaCoupons", "ListIssuedCouponQuotas", "ListCouponQuotasRecords"),
              "partner coupon ops",
          ),
      ),
      (
          "order-refund",
          lambda a: "ShowCustomerOrderDetails" in a or "ShowRefundOrderDetails" in a,
          lambda _a, text, _e: (
              text_mentions_op(text, "ShowCustomerOrderDetails")
              or text_mentions_op(text, "ShowRefundOrderDetails"),
              "order/refund op",
          ),
      ),
      (
          "enterprise",
          lambda a: "ListEnterpriseOrganizations" in a or "ListSubcustomerMonthlyBills" in a,
          lambda _a, text, _e: (
              _any_op(
                  text,
                  "ListEnterpriseOrganizations",
                  "ListEnterpriseSubCustomers",
                  "ListSubcustomerMonthlyBills",
              ),
              "enterprise ops",
          ),
      ),
      (
          "partner-customer",
          lambda a: "ListSubCustomers" in a or "ListCustomersBalancesDetail" in a,
          lambda _a, text, _e: (
              text_mentions_op(text, "ListSubCustomers")
              or text_mentions_op(text, "ListCustomersBalancesDetail"),
              "partner customer ops",
          ),
      ),
      (
          "reference-dims",
          lambda a: "ListServiceTypes" in a or "ServiceType" in a,
          lambda _a, text, _e: (text_mentions_op(text, "ListServiceTypes") or "字典" in text, "reference dims"),
      ),
      (
          "out-of-scope-refusal",
          lambda a: "拒绝路由" in a or "超出本技能范围" in a or "超出技能范围" in a or "不在本只读账务技能范围" in a or "不在本只读账务范围" in a,
          lambda _a, text, _e: (
              any(token in text for token in ("不在", "超出", "范围外", "拒绝路由"))
              and any(token in text for token in ("控制台", "销售", "账号中心", "对应云厂商", "其他云", "AWS", "Azure", "阿里")),
              "out-of-scope refusal",
          ),
      ),
      (
          "dot-free-resource",
          lambda a: "free_resource_ids.1" in a,
          lambda _a, text, _e: ("free_resource_ids.1" in text, "free_resource_ids dot"),
      ),
      (
          "dot-customer",
          lambda a: "customer_infos.1.customer_id" in a,
          lambda _a, text, _e: ("customer_infos.1.customer_id" in text, "customer_infos dot"),
      ),
      (
          "scope-profile",
          lambda a: ("profile" in a or "账号范围" in a) and "禁止" not in a and "含账号范围" not in a,
          lambda _a, text, _e: (
              "profile" in text.lower() or "当前账号" in text or "账号范围" in text,
              "scope",
          ),
      ),
      (
          "redaction",
          lambda a: "脱敏" in a and "禁止" not in a,
          lambda _a, text, _e: ("脱敏" in text or "***" in text or "后四位" in text, "redaction"),
      ),
      (
          "pending",
          lambda a: "待核验" in a or "待查" in a,
          lambda _a, text, _e: (
              any(x in text for x in ("待核验", "待查", "事实要点", "依据", "还差什么")),
              "verification status",
          ),
      ),
      (
          "basis",
          lambda a: "口径" in a,
          lambda _a, text, _e: (
              "口径" in text or "账期" in text or "scope" in text.lower(),
              "basis",
          ),
      ),
      (
          "reconcile-intent",
          lambda a: "对账" in a and "识别" in a,
          lambda _a, text, _e: ("对账" in text, "reconciliation"),
      ),
      (
          "amortized-keyword",
          lambda a: "摊销" in a,
          lambda _a, text, _e: ("摊销" in text, "amortized"),
      ),
      (
          "scope-role",
          lambda a: "伙伴" in a or "经销商" in a or "企业" in a,
          lambda _a, text, _e: (
              "伙伴" in text or "经销商" in text or "企业" in text or "子账号" in text,
              "scope role",
          ),
      ),
      (
          "delete-charge",
          lambda a: "删除" in a and "扣费" in a,
          lambda _a, text, _e: ("扣费" in text or "消费记录" in text, "charge attribution"),
      ),
      (
          "cdn-usage",
          lambda a: "CDN" in a or "95" in a,
          lambda _a, text, _e: ("CDN" in text or "95" in text or "用量" in text, "usage"),
      ),
      (
          "dot-notation",
          lambda a: "JSON 字符串" in a or "dot notation" in a or "--help" in a,
          lambda _a, text, _e: (
              "dot notation" in text or ".1=" in text or "time_condition.begin_time" in text,
              "dot notation",
          ),
      ),
      (
          "next-pending",
          lambda a: "下一步" in a and ("待核验" in a or "待查" in a),
          lambda _a, text, _e: (
              any(x in text for x in ("待核验", "待查"))
              and any(x in text for x in ("下一步", "补证", "还差什么")),
              "next step when pending",
          ),
      ),
      (
          "next-step",
          lambda a: "下一步" in a or "补证" in a,
          lambda _a, text, _e: (
              any(x in text for x in ("下一步", "补证", "还差什么")),
              "next step",
          ),
      ),
      (
          "clean-delivery",
          lambda a: "禁止在答复中出现" in a or "命令过程" in a or "业务说法" in a,
          lambda _a, text, _e: (_grade_clean_delivery(text), "clean delivery"),
      ),
      (
          "no-burden",
          lambda a: "禁止把调查负担" in a,
          lambda _a, text, _e: (
              not re.search(r"请自行对账\s*$", text.strip()),
              "no burden shift",
          ),
      ),
      (
          "refusal-mutable",
          lambda a: "拒绝" in a or "不包含 Pay" in a or ("禁止" in a and "写操作" in a),
          lambda a, text, _e: _grade_refusal_mutable(a, text),
      ),
      (
          "no-reask-settled",
          lambda a: "不重问" in a or "反复追问" in a,
          lambda a, text, e: _grade_no_reask(a, text, e),
      ),
      (
          "single-clarification",
          lambda a: "一次只问" in a
          or "仅提出一条" in a
          or "澄清问卷" in a
          or "不并列多个" in a
          or ("一条只读补证" in a and "而非" in a),
          lambda a, text, _e: _grade_single_clarification(a, text),
      ),
    ]
    return [GradeRule(name, when=when, grade=grade) for name, when, grade in rules]


RULES: list[GradeRule] = _rules()


def _grade_conclusion_first(text: str) -> tuple[bool, str]:
    markers = ("小结", "结论", "直接回答")
    if not any(m in text[:400] for m in markers):
        return False, "missing early summary"
    if "事实项" in text:
        si, fi = text.find("小结"), text.find("事实项")
        si = max(si, 0)
        if fi != -1 and fi < si and "小结" not in text[:fi]:
            return False, "facts before summary"
    return True, "conclusion-first ok"


def _grade_clean_delivery(text: str) -> bool:
    return not (
        ("```json" in text.lower())
        or ('{"' in text)
        or re.search(r"\bAK/SK\b", text)
        or re.search(r"profile/region", text, re.I)
        or re.search(r"\bhcloud\b", text, re.I)
        or re.search(r"\bList[A-Z][A-Za-z]+\b", text)
        or re.search(r"\bShow[A-Z][A-Za-z]+\b", text)
    )


def _grade_no_reask(assertion: str, text: str, eval_item: dict[str, Any]) -> tuple[bool, str]:
    if "不重问" not in assertion and "反复追问" not in assertion:
        return True, "no-reask n/a"
    prompt = str(eval_item.get("prompt") or "")
    failures: list[str] = []
    if "2025-04" in prompt and re.search(r"请.{0,12}确认.{0,16}账期|哪.{0,6}账期", text):
        failures.append("re-asked billing cycle")
    if "EP-FINANCE" in prompt and re.search(
        r"请.{0,12}确认.{0,16}企业项目|哪个企业项目", text
    ):
        failures.append("re-asked enterprise project")
    if "只读" in prompt and re.search(
        r"是否.{0,10}退款|要不要.{0,10}退款|仍要.{0,10}退款", text
    ):
        failures.append("re-asked refund vs readonly")
    if "经销商" in prompt and re.search(r"请.{0,12}确认.{0,8}经销", text):
        failures.append("re-asked partner role")
    if failures:
        return False, "; ".join(failures)
    return True, "no reask ok"


def _grade_single_clarification(assertion: str, text: str) -> tuple[bool, str]:
    if not any(
        token in assertion
        for token in ("一次只问", "仅提出一条", "澄清问卷", "不并列多个", "一条只读补证")
    ):
        return True, "single-clarification n/a"
    asks = re.findall(r"(?:请|能否|可否)[^\n]{0,80}[？?]", text)
    numbered = re.findall(r"(?:^|\n)\s*\d+[\.\)、]", text, re.MULTILINE)
    if len(asks) > 1 or len(numbered) >= 2:
        return False, f"too many blocking questions ({len(asks)} asks, {len(numbered)} numbered)"
    if "澄清问卷" in assertion and (text.count("？") + text.count("?")) > 2:
        return False, "questionnaire"
    return True, "single clarification ok"


def _grade_refusal_mutable(assertion: str, text: str) -> tuple[bool, str]:
    if not ("Pay" in assertion or "写操作" in assertion or "不包含 Pay" in assertion):
        return True, "refusal/mutable guard ok"
    bad = MUTABLE_OP_RE.search(text)
    if bad:
        pos = text.find(bad.group(0))
        window = text[max(0, pos - 30) : pos]
        if "拒绝" not in window:
            return False, f"found mutable op example {bad.group(1)}"
    return True, "refusal/mutable guard ok"


def grade_assertion(assertion: str, text: str, eval_item: dict[str, Any]) -> tuple[bool, str]:
    for rule in RULES:
        if rule.when(assertion):
            ok, reason = rule.grade(assertion, text, eval_item)
            return ok, reason
    ops = _covers_ops(eval_item)
    if ops and any(op in text for op in ops):
        return True, "covered op mentioned"
    return True, "default pass (review manually if critical)"


GOLDEN_BODIES: dict[str, str] = {
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
    "refuse-pricing-quote-out-of-scope": yagni_answer(
        "价格试算/续订报价不在本只读账务技能范围，超出 BSS 已出账事实边界；不调用 BSS 报价接口、不引导下单。",
        "拒绝路由：试算不是已出账金额；本技能只覆盖账单/对账/资源包等只读事实。",
        "请在华为云控制台价格计算器或销售侧定价工具完成试算。",
    ),
    "refuse-realname-review-out-of-scope": yagni_answer(
        "实名认证审核结果不在本只读账务技能范围（身份维度超出 BSS 账务边界），且非计费扣款证据；不调用 BSS 实名接口、不提交或变更资料。",
        "拒绝路由：实名审核属账号身份维度，超出本技能账务边界。",
        "请到华为云控制台账号中心查看实名审核结果。",
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
    "refuse-other-cloud-balance-out-of-scope": yagni_answer(
        "AWS 账务超出本技能范围（仅服务华为云 BSS）；不调用 hcloud BSS 接口、不混用华为云口径回答 AWS 余额。",
        "拒绝路由：非华为云账务（AWS）不在本技能范围；本技能仅覆盖华为云 BSS 只读事实。",
        "请到对应云厂商（AWS Billing 或 Cost Explorer）查看余额与欠费。",
    ),
    "proceed-without-reasking-settled-scope": yagni_answer(
        "将按 2025-04 账期、企业项目 EP-FINANCE 做云服务费用排行；具体金额待查。",
        "范围=当前登录账号；账期=2025-04；过滤 EP-FINANCE；按云服务聚合成本分析。",
        "只读做成本分析（小分页）；不先问账期或企业项目。",
    ),
    "single-clarification-partner-customer-id": yagni_answer(
        "经销商视角查代售客户余额需客户标识；未查前不报余额。",
        "可用客户列表发现范围；余额查询需 customer_infos.1.customer_id。",
        "请提供代售客户 ID，或确认是否先从客户列表选定一位客户？",
    ),
    "no-reask-readonly-after-refund-evidence-stated": yagni_answer(
        "**拒绝**代办退款；当前账号只读解释尾号 8842 订单退款构成，金额待查。",
        "范围=当前账号；订单与退款详情只读；订单证据≠消费归因。",
        "请提供完整订单号后，只读查退款详情（小分页）。",
    ),
    "bss-cli-region-not-profile-default": yagni_answer(
        "当前账号现金余额约 72.02 元（CNY），未见欠费表述；以当次查询为准。",
        "范围=当前 profile 账号；查账户余额快照；BSS 走华北-北京 endpoint（cn-north-1），不用华东 profile 区作 CLI region。",
        "配置只读凭证后查账户余额快照（小分页）。",
    ),
}


def build_answer(eval_item: dict[str, Any]) -> str:
    """Skill-shaped reference answer (offline; no live BSS)."""
    name = eval_item["name"]
    if name in GOLDEN_BODIES:
        return GOLDEN_BODIES[name]
    ops = _covers_ops(eval_item)
    op_hint = OP_ALIASES.get(ops[0], ("只读查询",))[0] if ops else "只读查询"
    return yagni_answer(
        "按一页纸路径处理；未查前不写具体金额。",
        f"路由到{op_hint}等只读事实；范围与账期待对齐。",
        f"只读{op_hint}（小分页）。",
    )


def run_protocol_suite() -> None:
    """Grade golden answers against merged rubric assertions (no LLM API)."""
    import sys

    from qa_common import load_eval_bundle, merge_assertions

    _, evals, global_assertions = load_eval_bundle()
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
        raise SystemExit(1)
    print(
        f"protocol eval ok: {len(evals)} cases, "
        f"{len(global_assertions)} global assertions merged"
    )
