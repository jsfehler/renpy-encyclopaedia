import os
from pathlib import Path

import markdown


docsgame_html_dir_name = 'docsgame_html'

DOCSGAME_USER_GUIDE_PATH = Path(f"{os.getcwd()}/docsgame/game/docs/user_guide")


def markdown_to_html(md: markdown.Markdown, input_path: Path) -> list[Path]:
    """Convert a directory of markdown files to html format."""
    if not input_path.is_dir():
        raise NotADirectoryError(f"{str(input_path)} was not found.")

    paths = []

    # Create docsgame directory if it doesn't exist.
    DOCSGAME_USER_GUIDE_PATH.mkdir(parents=True, exist_ok=True)

    # Convert every md file to html.
    for i in input_path.iterdir():
        j = Path(input_path, i)

        # Don't scan itself
        if i.name == docsgame_html_dir_name:
            continue

        name = i.name.split('.')[0] + '.html'

        html = Path(DOCSGAME_USER_GUIDE_PATH, Path(f"{name}"))

        md.convertFile(str(j), output=str(html))

        paths.append(html)

    return paths


if __name__ == "__main__":
    md = markdown.Markdown()
    DOCS_USER_GUIDE_PATH = Path(f"{os.getcwd()}/docs/user_guide")

    paths = markdown_to_html(md, input_path=DOCS_USER_GUIDE_PATH)
