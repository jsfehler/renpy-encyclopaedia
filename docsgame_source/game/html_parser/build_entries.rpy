init 1 python:
    from bs4 import BeautifulSoup

    # Create EncEntry dynamically from user guide.
    enc_enc = Encyclopaedia(
        name="Ren'Py Encyclopaedia Documentation",
        entry_screen='docs_entry',
        sorting_mode=SortMode.SUBJECT,
    )

    html_files = get_file_paths('docs/user_guide')

    from pathlib import Path
    import string

    for html in html_files:
        html_path = Path(html)

        subject = string.capwords(html_path.parts[2].replace('-',' '))

        with renpy.open_file(html) as f:
            soup = BeautifulSoup(f.read(), 'html.parser').html.body

        elements = []

        for element in soup:
            if element.name:
                found_elements = iter_block(element)

                elements = [*elements, *found_elements]

        entry = EncEntry(
            enc_enc,
            name=f"{soup.h1.string}",
            text='',
            subject=subject,
        )

        entry.elements = elements

    develop_path = 'docs/tools.html'
    with renpy.open_file(develop_path) as f:
        soup = BeautifulSoup(f.read(), 'html.parser').html.body


    elements = []

    for element in soup:
        if element.name:
            found_elements = iter_block(element)

            elements = [*elements, *found_elements]

    dev_entry = EncEntry(
        enc_enc,
        name=f"{soup.h1.string}",
        text='',
        subject="Development",
    )

    dev_entry.elements = elements
