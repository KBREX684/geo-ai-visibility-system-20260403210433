from app.services.compliance import check_report_compliance


def test_compliance_fails_when_missing_required_sections():
    result = check_report_compliance(
        {
            "disclaimer_text": "",
            "evidence_summary": [],
            "score_breakdown": {},
            "next_actions": [],
        }
    )
    assert result["is_compliant"] is False
    assert len(result["missing_sections"]) == 4


def test_compliance_passes_with_full_report():
    result = check_report_compliance(
        {
            "disclaimer_text": "boundary",
            "evidence_summary": [{"platform": "chatgpt"}],
            "score_breakdown": {
                "visibility": 60,
                "ranking": 50,
                "sentiment": 70,
                "accuracy": 80,
                "total": 62,
            },
            "next_actions": ["action1"],
        }
    )
    assert result["is_compliant"] is True
    assert result["missing_sections"] == []

