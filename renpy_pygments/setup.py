from setuptools import setup, find_packages


setup(
    name="renpylexer",
    packages=find_packages(),
    entry_points =
    """
    [pygments.lexers]
    renpylexer = renpylexer.lexer:RenPyLexer
    """,
)
