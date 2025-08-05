import json

from misstea.sub_agents.outlook.agent import get_my_calendar


def test_get_my_calendar_e2e():
    result = get_my_calendar(date_of_interest="2024-08-01")
    report = json.loads(result["report"])

    assert result["status"] == "success"
    assert isinstance(report, list)
    assert len(report) > 0
    assert "subject" in report[0]
    assert "start" in report[0]
    assert "end" in report[0]
