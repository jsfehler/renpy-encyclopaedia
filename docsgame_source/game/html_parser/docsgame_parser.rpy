init python:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from renpylexer.lexer import RenPyLexer


    def check_main(element):
        text = ''
        return text


    def check_section(element):
        text = ''
        return text


    def check_ol(element):
        text = ''
        return text


    def check_ul(element):
        text = ''
        return text


    def check_a(element):
        text = str(element.string)
        return f"{{a={element['href']}}}{text}{{/a}}"


    def check_cite(element):
        text = str(element.string)
        return f"{{i}}{text}{{/i}}"


    def check_h1(element):
        return '{size=+14}' + str(element.string) + '{/size}'


    def check_h2(element):
        return '{size=+4}' + str(element.string) + '{/size}'


    def check_h3(element):
        return '{size=+2}' + str(element.string) + '{/size}'


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

        return clean_p_str


    def check_li(element):
        p_str = '    - '  # List padding

        for el in element.contents:
            if not el.name:
                p_str += str(el.string)
            else:
                found_tags, found_text = iter_block(el)
                p_str += ''.join(found_text)

        return p_str


init 1 python:
    from bs4 import BeautifulSoup


    elem_funcs = {
        'main': check_main,
        'section': check_section,
        'ol': check_ol,
        'ul': check_ul,
        'h1': check_h1,
        'h2': check_h2,
        'h3': check_h3,
        'a': check_a,
        'cite': check_cite,
        'li': check_li,
        'p': check_p,
    }


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

        if element.name in ['main', 'section', 'ol', 'ul']:
            element_str = elem_funcs[element.name](element)

            tags.append(element.name)
            text.append(element_str)

            found_tags, found_text = iter_blocks(element)

            tags = [*tags, *found_tags]
            text = [*text, *found_text]

        # Handle code blocks
        elif element.name == 'pre':
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

        elif elem_funcs.get(element.name):
            element_str = elem_funcs[element.name](element)

            tags.append(element.name)
            text.append(element_str)

        elif element.name == 'blockquote':
            found_tags, found_text = iter_blocks(element)

            tags = [*tags, *found_tags]
            text = [*text, *found_text]

        else:
            # Default for other blocks
            element_str = str(element.string)

            tags.append(element.name)
            text.append(element_str)

        return tags, text

    # Create EncEntry dynamically from user guide.
    enc_enc = Encyclopaedia(name="Ren'Py Encyclopaedia Documentation")

    html_files = get_file_paths('docs/user_guide')

    from pathlib import Path
    import string

    for html in html_files:
        html_path = Path(html)

        subject = string.capwords(html_path.parts[2].replace('-',' '))

        with renpy.open_file(html) as f:
            soup = BeautifulSoup(f.read(), 'html.parser').html.body

        tags = []
        text = []

        for element in soup:
            if element.name:
                found_tags, found_text = iter_block(element)

                tags = [*tags, *found_tags]
                text = [*text, *found_text]

        entry = EncEntry(
            enc_enc,
            name=f"{soup.h1.string}",
            text=text,
            subject=subject,
        )

        entry.tags = tags


    develop_path = 'docs/development.html'
    with renpy.open_file(develop_path) as f:
        soup = BeautifulSoup(f.read(), 'html.parser').html.body

    text = []

    for element in soup:
        if element.name:
            found_tags, found_text = iter_block(element)

            tags = [*tags, *found_tags]
            text = [*text, *found_text]

    dev_entry = EncEntry(
        enc_enc,
        name=f"{soup.h1.string}",
        text=text,
        subject="Development",
    )

    dev_entry.tags = tags
