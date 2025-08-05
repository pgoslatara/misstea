from datetime import datetime, timezone

import pytest

from misstea.utils import get_current_date, get_current_time, json_serial


def test_get_current_date():
    result = get_current_date()
    assert result["status"] == "success"
    assert str(datetime.now(timezone.utc).date()) in result["report"]


def test_get_current_time():
    result = get_current_time()
    assert result["status"] == "success"
    assert (
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        in result["report"]
    )


def test_json_serial():
    now = datetime.now()
    assert json_serial(now) == now.isoformat()
    with pytest.raises(TypeError):
        json_serial(123)
