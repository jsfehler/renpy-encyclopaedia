from distutils.core import setup

files = ["renpy/*"]

setup(
    name="mock_renpy",
    version="0.1",
    description="Mock the Ren'py library for unit test purposes.",
    author="Joshua Fehler",
    author_email="jsfehler@gmail.com",
    packages=["mock_renpy"]
)
