import json
import logging
from pathlib import Path

import chardet
import yaml  # Added this import

logger = logging.getLogger(__name__)


def list_directory_contents(
    directory_path: str, include_subdirectories: str = "yes", type_filter: str = "all"
) -> str:
    """Recursively traverses a directory and its subdirectories, returning a list of objects based on the specified type_filter.

    Args:
        directory_path (str): The path to the directory to scan.
        include_subdirectories: (Optional(str)): An optional string argument that can be "yes" or "no". Defaults to "yes".
        type_filter (Optional(str)): An optional string argument that can be "files", "directories", or "all". Defaults to "all".

    Returns:
        str: List of objects matching the type_filter.

    Raises:
        ValueError: If an invalid include_subdirectories or type_filter is provided.
        FileNotFoundError: If the specified directory_path does not exist or is not a directory.

    """
    path = Path(directory_path)
    if not path.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    if include_subdirectories == "yes":
        iter_item = path.rglob("*")
    elif include_subdirectories == "no":
        iter_item = path.iterdir()
    else:
        raise ValueError(
            f"include_subdirectories must be 'yes' or 'no'. Instead for `{include_subdirectories}`."
        )

    results = []
    for item in iter_item:
        if type_filter == "files":
            if item.is_file():
                results.append(item)
        elif type_filter == "directories":
            if item.is_dir():
                results.append(item)
        elif type_filter == "all":
            results.append(item)
        else:
            raise ValueError(
                f"Invalid type_filter: {type_filter}. Must be 'files', 'directories', or 'all'."
            )
    return json.dumps([str(x.absolute()) for x in results])


def read_directory(path: str) -> str:
    """Read the contents of all files at the specified path.

    Args:
        path (str): The path to read.

    Returns:
        dict[str, str]: The path to the file and the contents of the file.

    """
    data = {}
    for file_path in Path(path).glob("**/*"):
        if file_path.is_file() and file_path.suffix not in [
            ".0",
            ".1",
            ".2",
            ".3",
            ".4",
            ".5",
            ".6",
            ".7",
            ".8",
            ".9",
            ".10",
            ".11",
            ".12",
            ".a",
            ".ani",
            ".bz2",
            ".dat",
            ".exe",
            ".fits",
            ".gz",
            ".gzip",
            ".ico",
            ".idx",
            ".jpg",
            ".jpeg",
            ".lzma",
            ".mat",
            ".mo",
            ".nc",
            ".npy",
            ".npz",
            ".obj",
            ".pack",
            ".pkl",
            ".png",
            ".pyc",
            ".rev",
            ".sav",
            ".so",
            ".testcase",
            ".wav",
            ".webp",
            ".whl",
            ".woff2",
            ".xz",
            ".z",
            "",
        ]:
            try:
                data[str(file_path.absolute())] = read_file(str(file_path.absolute()))
            except UnicodeDecodeError:
                logger.error(f"Failed to read {file_path.suffix}")
                data[str(file_path.absolute())] = (
                    "Unable to read due to UnicodeDecodeError."
                )

    # return json.dumps(data)
    logger.debug(f"{data=}")
    return json.dumps(data)


def read_file(file_path: str, encoding: str = "") -> str | None:
    """Read a file, attempt to auto-detect encoding if not specified.

    If the file is a YAML file, it returns the parsed YAML content.

    Args:
        file_path (str): The path to the file.
        encoding (str | None): The encoding to use. If None, chardet will attempt detection.

    Returns:
        str | dict | list | None: The content of the file if successful, parsed if YAML, otherwise None.

    """
    path_obj = Path(file_path)
    if not path_obj.is_file():
        logger.error(f"The file '{file_path}' was not found.")
        return None

    # YAML
    if path_obj.suffix in [".yaml", ".yml"]:
        try:
            with path_obj.open(mode="r", encoding=encoding) as f:
                content = f.read()

                return yaml.safe_load(content)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file '{file_path}': {e}")
            return None

    # If encoding is not provided, attempt to detect it
    if not encoding:
        try:
            with path_obj.open(mode="rb") as f:
                raw_data = f.read(4096)  # Read up to 4KB for detection
            detection_result = chardet.detect(raw_data)
            if detected_encoding := detection_result["encoding"]:
                confidence = detection_result["confidence"]

                logger.debug(
                    f"Detected encoding: '{detected_encoding}' with confidence: {confidence:.2f}"
                )
                encoding = detected_encoding
            else:
                logger.debug(
                    f"Could not reliably detect encoding for '{file_path}'. Falling back to 'utf-8'."
                )
                encoding = "utf-8"
        except Exception as e:
            logger.debug(
                f"Error during encoding detection for '{file_path}': {e}. Falling back to 'utf-8'."
            )
            encoding = "utf-8"

    try:
        with path_obj.open(mode="r", encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        logger.error(
            f"Could not decode file '{file_path}' with encoding '{encoding}'. Please ensure the correct encoding is specified or auto-detection failed."
        )
        return None
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while reading '{file_path}' with encoding '{encoding}': {e}"
        )
        return None


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
