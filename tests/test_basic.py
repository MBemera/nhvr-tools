from nhvr_mcp.formatters import format_response
from nhvr_mcp.knowledge import FATIGUE_RULES
from nhvr_mcp.tools import get_fatigue_rules


def test_format_response_json():
    result = format_response({"key": "value"}, "json")
    assert "\"key\"" in result


def test_get_fatigue_rules_standard():
    result = get_fatigue_rules("standard", "markdown")
    assert FATIGUE_RULES["standard"]["summary"] in result
