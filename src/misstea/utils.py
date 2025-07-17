from datetime import datetime, timezone
from typing import Dict


def get_current_date() -> Dict[str, str]:
    """Get the current date in UTC.

    Returns:
        dict: Current date in UTC.

    """
    report = f"The current date is {datetime.now(timezone.utc).date()}."
    return {"status": "success", "report": report}


def get_current_time() -> Dict[str, str]:
    """Get the current time in UTC.

    Returns:
        dict: status and result or error msg.

    """
    now = datetime.now(timezone.utc)
    report = f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')} UTC."
    return {"status": "success", "report": report}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code.

    Args:
        obj (Any): The object to serialize.

    Returns:
        str: The ISO formatted string if the object is a datetime object.

    Raises:
        TypeError: If the object type is not serializable.

    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
