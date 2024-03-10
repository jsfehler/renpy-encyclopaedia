"""renpy
init -85 python in enc_utils:
"""
import re
import textwrap


def text_block(text: str) -> str:
    """Wrap strings to remove whitespace and line breaks, but preserve blank lines.

    The intended use case for this function is on triple quoted strings.

    Args:
        text: The string to wrap.

    Example:
        >>> wrapped_text = text_block(\"\"\"\\
        >>> Whitespace on the left is removed,
        >>> and newlines are removed.
        >>> This means even if you break lines to make writing text easier,
        >>> when the text is displayed it won't use those arbitrary breaks.
        >>>
        >>> However, blank lines (i.e.: paragraph breaks) are kept. When used
        >>> with triple quoted strings, this can make writing large entries
        >>> much easier.
        >>>
        >>> The slash (\\) at the start of the string is necessary to avoid
        >>> a blank first line.
        >>> \"\"\")
    """
    dedented_text = textwrap.dedent(text)

    paragraphs = re.split(r'\n\n', dedented_text)

    clean_paragraphs = [paragraph.replace('\n', ' ') for paragraph in paragraphs]

    output_text = '\n\n'.join(clean_paragraphs)
    return output_text
