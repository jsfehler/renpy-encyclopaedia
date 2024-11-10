# @PydevCodeAnalysisIgnore
import re

from .keywords import keywords, properties

from pygments.lexers.agile import PythonLexer
from pygments.token import Token, Name, Operator

import docutils.nodes


KEYWORDS = set(keywords)
PROPERTIES = set(properties)


class RenPyLexer(PythonLexer):
    """A lexer for the Ren'Py scripting language, based on the Python lexer from Pygments.
    """
    name: str = "Ren'Py"
    aliases: list[str] = ["renpy", "rpy"]
    filenames: list[str] = ["*.rpy", "*.rpym"]

    def get_tokens_unprocessed(self, text: str):
        """Tokenize Ren'Py code.

        Args:
            text: The text to tokenize.

        Return:
            An iterable of tokens, where each token is a tuple of the form (index, token, value).
        """
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):

            if value.startswith("###"):
                continue

            if token == Token.Error and value == "$":
                yield index, Token.Keyword, value

            elif token in [Name, Operator.Word] and value in KEYWORDS:
                yield index, Token.Keyword, value

            elif token in Name and value in PROPERTIES:
                yield index, Name.Attribute, value

            else:
                yield index, token, value


def parse_var_node(env, sig: str, signode) -> str:
    """Parse a var node in a Sphinx document.

    Args:
        env: The environment object.
        sig: The signature of the node.
        signode: The signature node.

    Return:
        A reference to the parsed node.
    """
    m = re.match(r'(\S+)(.*)', sig)

    if m.group(1).split('.')[0] in ["config", "gui"]:
        signode += docutils.nodes.Text("define ", "define")

    signode += sphinx.addnodes.desc_name(m.group(1), m.group(1))
    signode += docutils.nodes.Text(m.group(2), m.group(2))

    ref = m.group(1)
    return ref


style_seen_ids = set()


def parse_style_node(env, sig: str, signode) -> str:
    """Parse a style node in a Sphinx document.

    Args:
        env: The environment object.
        sig: The signature of the node.
        signode: The signature node.

    Return:
        A reference to the parsed node.
    """
    m = re.match(r'(\S+)(.*)', sig)

    name = m.group(1)
    desc = m.group(2)
    desc = " - " + desc

    signode += sphinx.addnodes.desc_name(name, name)
    signode += docutils.nodes.Text(desc, desc)

    ref = m.group(1)

    while ref in style_seen_ids:
        print("duplicate id:", ref)
        ref = ref + "_alt"

    style_seen_ids.add(ref)

    return ref
