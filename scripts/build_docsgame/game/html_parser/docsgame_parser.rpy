init python:
    def rip_link(link: list[str]) -> str:
        name = link[0]
        url = "<" + link[1]
        return f"{{a={url}}}{name}{{/a}}"


    def check_code(element, input_str) -> str:
        element_sting = str(element.string)
        link = element_sting.split("<")

        if len(link) == 1:
            return f"{input_str} {link[0]}"

        if len(link) == 2:
            return f"{input_str} {rip_link(link)}"

        return input_str


init 1 python:
    from bs4 import BeautifulSoup

    from pygments import highlight
    from pygments.lexers import PythonLexer

    # Create EncEntry dynamically from user guide.
    enc_enc = Encyclopaedia()

    html_files = get_file_paths('docs/user_guide')

    img_mapper = {
        'docs/user_guide/getting-started.html': 'images/getting-started.png',
    }

    for html in html_files:
        img_to_use = img_mapper.get(html)

        with renpy.open_file(html) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        text = []

        inside_code_block = False

        for element in soup:
            if element.name == 'h1':
                element_str = '{size=+12}' + str(element.string) + '{/size}'

            elif element.name == 'h2':
                element_str = '{size=+8}' + str(element.string) + '{/size}'

            elif element.name == 'p':
                element_str = ''

                # Code block directive. Don't display it.
                if str(element.string) == '.. code-block:: python':
                    inside_code_block = True
                    continue

                # Iterate through paragraph.
                for sub_elem in element.contents:
                    if sub_elem.name == 'code':
                        element_str = check_code(sub_elem, element_str)

                    elif sub_elem.name == 'em':
                        for el in sub_elem.contents:

                            if el.name == 'code':
                                element_str = check_code(el, element_str)


                            else:
                                element_str += ' ' + str(el.string).strip("\n")

                    else:
                        element_str += str(sub_elem.string)

            # Handle code blocks
            elif inside_code_block and element.name == 'pre':
                element_str = ''

                for sub_elem in element.contents:
                    element_string = str(element.string)

                    # Highlight code blocks
                    element_str += highlight(
                        element_string, PythonLexer(), RenpyFormatter(style='github-dark'),
                    )

            else:
                element_str = str(element.string)

            text.append(element_str)


        EncEntry(
            enc_enc,
            name=f"{soup.h1.string}",
            text=text,
            subject="User Guide",
            #image=Transform('images/getting-started.png', zoom=0.5),
            image=img_to_use,
        )


screen encyclopaedia_button():
    textbutton "Encyclopaedia" action ShowMenu('encyclopaedia_list', enc_enc)


init:
    $ config.overlay_screens.append('encyclopaedia_button')
