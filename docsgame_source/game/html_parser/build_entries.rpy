init 1 python:
    from bs4 import BeautifulSoup

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

    tags = []
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
