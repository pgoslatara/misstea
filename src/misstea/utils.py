from datetime import datetime


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
