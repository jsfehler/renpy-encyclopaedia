from setuptools import setup, find_packages


setup(
    name="renpylexer",
    packages=find_packages(),
    install_requires=[
        'docutils',
        'pygments',
    ],
    entry_points =
    """
    [pygments.lexers]
    renpylexer = renpylexer.lexer:RenPyLexer
    """,
)
