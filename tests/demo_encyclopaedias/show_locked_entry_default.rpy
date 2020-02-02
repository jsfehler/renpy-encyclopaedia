# Create an encyclopaedia with reverse alphabetical sorting as the
# default sorting mode.
init python:
    encyclopaedia = Encyclopaedia(
        show_locked_buttons=False,
        show_locked_entry=True
    )

    food_list = ["Apple", "Banana", "Carrot", "Deer", "Eel"]

    for x in range(5):
        EncEntry(
            parent=encyclopaedia,
            name=food_list[x],
            text=["Test."]
        )

    locked_entry = EncEntry(
        parent=encyclopaedia,
        name="Mango",
        text=["Test."],
        locked=True
    )
