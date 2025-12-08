from pathlib import Path


def analyze_codebase(directory: str) -> dict:
    """Analyse the codebase in the given directory.

    Returns:
        dict: The content of the codebase.

    """
    files = [x for x in Path(directory).rglob("**") if x.is_file()]
    codebase_context = ""
    for file in files:
        if Path(file).is_file():
            codebase_context += f"""- **{file}**:"""
            try:
                with Path(file).open("r", encoding="utf-8") as f:
                    codebase_context += f.read()
            except UnicodeDecodeError:
                with Path(file).open("r", encoding="latin-1") as f:
                    codebase_context += f.read()
    return {"codebase_context": codebase_context}


def save_blog_post_to_file(blog_post: str, filename: str) -> dict:
    """Save the blog post to a file.

    Returns:
        dict: Saves a blog post to a file.

    """
    with Path(filename).open("w") as f:
        f.write(blog_post)
    return {"status": "success"}
