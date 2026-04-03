REQUIRED_SECTIONS = [
    "capability_boundary",
    "evidence_chain",
    "score_explanation",
    "next_actions",
]


def check_report_compliance(report: dict) -> dict:
    missing = []
    if not report.get("disclaimer_text"):
        missing.append("capability_boundary")
    if not report.get("evidence_summary"):
        missing.append("evidence_chain")
    score_breakdown = report.get("score_breakdown") or {}
    needed_scores = {"visibility", "ranking", "sentiment", "accuracy", "total"}
    if not needed_scores.issubset(set(score_breakdown.keys())):
        missing.append("score_explanation")
    if not report.get("next_actions"):
        missing.append("next_actions")

    return {
        "is_compliant": len(missing) == 0,
        "required_sections": REQUIRED_SECTIONS,
        "missing_sections": missing,
    }


DEFAULT_DISCLAIMER = (
    "本报告目标是提升AI可见性指标，不承诺具体排名或必被推荐。"
    "结果受平台算法波动、AI Overviews机制变化、第三方收录延迟等影响。"
)

