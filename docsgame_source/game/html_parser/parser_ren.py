"""renpy
init -19 python:
"""
from typing import Union

from pygments import highlight
from pygments.lexers import PythonLexer

from renpy_pygments.lexer import RenPyLexer


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


class Element:
    """Container for data extracted from an HTML Element.
    """
    def __init__(self, name: str, style: str, text: str = '') -> None:
        self.name = name
        self.style = style
        self.text = text

        self.children = []

    def __eq__(self, other) -> bool:
        if (self.name == other.name) and (self.text == other.text):
            return True
        return False


@elem('aside')
def check_aside(element):
    return Element(element.name, 'default', '')


@elem('blockquote')
def check_blockquote(element):
    return Element(element.name, 'default', '')

@elem('main')
def check_main(element):
    return Element(element.name, 'default', '')


@elem('section')
def check_section(element):
    return Element(element.name, 'default', '')


@elem('ol')
def check_ol(element):
    return Element(element.name, 'default', '')


@elem('ul')
def check_ul(element):
    return Element(element.name, 'html_ul', '')


@elem('a')
def check_a(element):
    text = str(element.string)
    return Element(element.name, 'default', f"{{a={element['href']}}}{text}{{/a}}")


@elem('cite')
def check_cite(element):
    text = str(element.string)
    return Element(element.name, 'html_cite', f"{{i}}{text}{{/i}}")


@elem('span')
def check_span(element) -> Union[Element, None]:
    text = str(element.string)
    # An empty <span> has no data we care about preserving.
    if element.string is None:
        return
    return Element(element.name, 'html_span', f"{{i}}{text}{{/i}}")


@elem('h1')
def check_h1(element):
    text = str(element.string)
    return Element(element.name, 'html_h1', text)

@elem('h2')
def check_h2(element):
    text = str(element.string)
    return Element(element.name, 'html_h2', text)


@elem('h3')
def check_h3(element):
    text = str(element.string)
    return Element(element.name, 'html_h3', text)


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
            found_elements = iter_block(el)
            p_str += ''.join([e.text for e in found_elements])

    # Remove carriage return
    clean_p_str = p_str.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')

    return Element(element.name, 'html_p', clean_p_str)


@elem('li')
def check_li(element):
    p_str = '    - '  # List padding

    for el in element.contents:
        if not el.name:
            p_str += str(el.string)
        else:
            found_elements = iter_block(el)
            p_str += ''.join([e.text for e in found_elements])

    return Element(element.name, 'html_li', p_str)


def iter_blocks(element):
    inner_elements: list = []

    for elem in element:
        if elem.name:
            e_elements = iter_block(elem)

            inner_elements = [*inner_elements, *e_elements]

    return inner_elements


def iter_block(element):  # -> list[str]:
    e_elements: list = []

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

        # Ignore the pre tag, only add the code block
        # e_elements.append(Element(element.name, 'default', element_str))

        inner_text = ''
        for sub_elem in element.contents:
            if sub_elem.name == 'code':
                inner_text += check_funcs[check_func](sub_elem)

        e_elements.append(Element('code', 'default', element_str + inner_text))

    elif element.name in ['li', 'p']:
        element_class = elem_funcs[element.name](element)

        # Record children
        elements_x = []
        for elem in element.children:
            elements_x = [*elements_x, *iter_block(elem)]

        element_class.children = elements_x

        e_elements = [*e_elements, element_class]

    elif elem_funcs.get(element.name):
        element_class = elem_funcs[element.name](element)

        if element_class:
            found_elements = iter_blocks(element)

            # Record children
            elements_x = []
            for elem in element.children:
                elements_x = [*elements_x, *iter_block(elem)]

            element_class.children = elements_x

            e_elements = [*e_elements, element_class, *found_elements]

    else:
        # Default for other blocks
        element_str = str(element.string)

        e_elements.append(Element(element.name, 'default', element_str))

    return e_elements
