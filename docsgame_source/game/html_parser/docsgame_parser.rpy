init python:
    from pygments import highlight
    from pygments.lexers import PythonLexer


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
        return '{size=+8}' + str(element.string) + '{/size}'


    def check_h3(element):
        return '{size=+4}' + str(element.string) + '{/size}'


    def check_code(element):
        text = str(element.text)
        # Highlight code blocks
        return highlight(
            text, PythonLexer(), RenpyFormatter(style='github-dark'),
        )


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
    }


    def iter_blocks(element):
        inner_text: list[str] = []

        for elem in element:
            #if elem.name:
            inner_text = [*inner_text, *iter_block(elem)]

        return inner_text


    def iter_block(element, inside_code_block: bool = False):  # -> list[str]:
        text = []
        element_str = ''

        if element.name in ['main', 'section', 'ol', 'ul']:
            element_str = elem_funcs[element.name](element)
            text.append(element_str)

            text = [*text, *iter_blocks(element)]

        elif element.name in ['li']:
            element_str = '\n'

            p_str = '    - '  # List padding
            for ee in element.contents:
                if not ee.name:
                    p_str += str(ee.string)
                else:
                    p_str += ''.join(iter_block(ee))

            text.append(p_str)

        elif element.name == 'p':
            element_str = '\n'

            p_str = ''
            for ee in element.contents:
                if not ee.name:
                    p_str += str(ee.string)
                else:
                    p_str += ''.join(iter_block(ee))

            text.append(p_str)

        # Handle code blocks
        elif element.name == 'pre':
            element_str = ''
            text.append(element_str)

            inner_text = ''
            for sub_elem in element.contents:
                if sub_elem.name == 'code':
                    inner_text += check_code(sub_elem)

            text.append(element_str + inner_text)

        elif elem_funcs.get(element.name):
            element_str = elem_funcs[element.name](element)
            text.append(element_str)

        else:
            # Default for other blocks
            element_str = str(element.string)
            text.append(element_str)

        return text

    # Create EncEntry dynamically from user guide.
    enc_enc = Encyclopaedia()

    html_files = get_file_paths('docs/user_guide')

    img_mapper = {
        'docs/user_guide/01-getting-started.html': 'images/getting-started.png',
    }

    for html in html_files:
        img_to_use = img_mapper.get(html)

        with renpy.open_file(html) as f:
            soup = BeautifulSoup(f.read(), 'html.parser').html.body

        text = []

        for element in soup:
            if element.name:
                text = [*text, *iter_block(element)]

        EncEntry(
            enc_enc,
            name=f"{soup.h1.string}",
            text=text,
            subject="User Guide",
            #image=Transform('images/getting-started.png', zoom=0.5),
            image=img_to_use,
        )


    develop_path = 'docs/development.html'
    with renpy.open_file(develop_path) as f:
        soup = BeautifulSoup(f.read(), 'html.parser').html.body

    text = []

    for element in soup:
        if element.name:
            text = [*text, *iter_block(element)]

    EncEntry(
        enc_enc,
        name=f"{soup.h1.string}",
        text=text,
        subject="Development",
    )

screen encyclopaedia_button():
    textbutton "Encyclopaedia" action ShowMenu('encyclopaedia_list', enc_enc)


init:
    $ config.overlay_screens.append('encyclopaedia_button')
