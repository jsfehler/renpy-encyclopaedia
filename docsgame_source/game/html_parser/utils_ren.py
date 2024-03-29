"""renpy
init -19 python:
"""

def get_file_paths(prefix:str) -> list[str]:
    """Get the paths to the html files for the docs."""
    rv: list[str] = []

    for path in renpy.list_files():
        if path.startswith(prefix):
            rv.append(path)

    return rv
