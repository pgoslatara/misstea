from pathlib import Path


def read_file(path: str) -> str:
    """Read the contents of a file at the specified path.

    Args:
        path (str): The path of the file to read.

    Returns:
        str: The contents of the file.

    """
    return Path(path).read_text()


def write_to_file(path: str, content: str) -> str:
    """Write content to a file at the specified path.

    If the file exists, it will be overwritten. If it doesn't exist, it will be created.

    Args:
        path (str): The path of the file to write to.
        content (str): The content to write to the file.

    Returns:
        str: A confirmation message.

    """
    Path(path).write_text(content)
    return f"Successfully wrote to {path}."


def replace_in_file(path: str, search: str, replace: str) -> str:
    """Replace a string in a file.

    Args:
        path (str): The path of the file to modify.
        search (str): The string to search for.
        replace (str): The string to replace with.

    Returns:
        str: A confirmation message.

    """
    content = Path(path).read_text()
    new_content = content.replace(search, replace)
    Path(path).write_text(new_content)
    return f"Successfully replaced text in {path}."
