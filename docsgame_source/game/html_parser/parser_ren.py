"""renpy
init -19 python:
"""
import bs4

from pygments import highlight
from pygments.lexers import PythonLexer

from renpylexer.lexer import RenPyLexer


elem_funcs = {}

def elem(name: str):
    """Register tags via a decorator."""
    def decorator(func):
        elem_funcs[name] = func

        def wrapper(*args, **kwargs):
            elem_content = func(*args, **kwargs)
            return elem_content

        return wrapper

    return decorator


@elem('aside')
def check_aside(element):
    text = ''
    return element.name, text


@elem('blockquote')
def check_blockquote(element):
    text = ''
    return element.name, text

@elem('main')
def check_main(element):
    text = ''
    return element.name, text


@elem('section')
def check_section(element):
    text = ''
    return element.name, text


@elem('ol')
def check_ol(element):
    text = ''
    return element.name, text


@elem('ul')
def check_ul(element):
    text = ''
    return element.name, text


@elem('a')
def check_a(element):
    text = str(element.string)
    return element.name, f"{{a={element['href']}}}{text}{{/a}}"


@elem('cite')
def check_cite(element):
    text = str(element.string)
    return element.name, f"{{i}}{text}{{/i}}"


@elem('span')
def check_span(element):
    text = str(element.string)
    return element.name, f"{{i}}{text}{{/i}}"


@elem('h1')
def check_h1(element):
    return element.name, '{size=+14}' + str(element.string) + '{/size}'


@elem('h2')
def check_h2(element):
    return element.name, '{size=+4}' + str(element.string) + '{/size}'


@elem('h3')
def check_h3(element):
    return element.name, '{size=+2}' + str(element.string) + '{/size}'


def check_py_code(element):
    """pygments is used to highlight the content of code blocks."""
    text = str(element.text)
    return highlight(
        text, PythonLexer(), RenpyFormatter(style='github-dark'),
    )


def check_renpy_code(element):
    """pygments is used to highlight the content of code blocks."""
    text = str(element.text)
    return highlight(
        text, RenPyLexer(), RenpyFormatter(style='github-dark'),
    )


@elem('p')
def check_p(element):
    # In a paragraph, we don't want a separate line per sentence.
    # Instead, join all the strings inside the paragraph.
    p_str = ''

    for el in element.contents:
        if not el.name:
            p_str += str(el.string)
        else:
            # Parse tags inside the paragraph.
            found_tags, found_text = iter_block(el)
            p_str += ''.join(found_text)

    # Remove carriage return
    clean_p_str = p_str.replace('\r\n', ' ').replace('\r', ' ')

    return element.name, clean_p_str


@elem('li')
def check_li(element):
    p_str = '    - '  # List padding

    for el in element.contents:
        if not el.name:
            p_str += str(el.string)
        else:
            found_tags, found_text = iter_block(el)
            p_str += ''.join(found_text)

    return element.name, p_str


def iter_blocks(element):
    inner_tags: list[str] = []
    inner_text: list[str] = []

    for elem in element:
        if elem.name:
            tags, text = iter_block(elem)

            inner_tags = [*inner_tags, *tags]
            inner_text = [*inner_text, *text]

    return inner_tags, inner_text


def iter_block(element, inside_code_block: bool = False):  # -> list[str]:
    tags: list[str] = []
    text: list[str] = []

    element_str = ''

    # Handle code blocks
    if element.name == 'pre':
        check_func = element.attrs['class'][1]

        check_funcs = {
            'python': check_py_code,
            'renpy': check_renpy_code,
            'console': check_py_code,
        }

        element_str = ''

        tags.append('pre')
        text.append(element_str)

        inner_text = ''
        for sub_elem in element.contents:
            if sub_elem.name == 'code':
                inner_text += check_funcs[check_func](sub_elem)

        tags.append('code')
        text.append(element_str + inner_text)

    elif element.name in ['li', 'p']:
        element_tag, element_str = elem_funcs[element.name](element)

        found_tags, found_text = iter_blocks(element)

        tags = [*tags, element_tag]
        text = [*text, element_str]

    elif elem_funcs.get(element.name):
        element_tag, element_str = elem_funcs[element.name](element)

        found_tags, found_text = iter_blocks(element)

        tags = [*tags, element_tag, *found_tags]
        text = [*text, element_str, *found_text]

    else:
        # Default for other blocks
        element_str = str(element.string)

        tags.append(element.name)
        text.append(element_str)

    return tags, text
