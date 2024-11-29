from typing import ClassVar, Iterator, Sequence

from pygments.lexers.agile import PythonLexer
from pygments.token import Name, Operator, Token, _TokenType

from .keywords import keywords, properties

KEYWORDS = set(keywords)
PROPERTIES = set(properties)


class RenPyLexer(PythonLexer):
    """Lexer for the Ren'Py scripting language.

    Based on the Python lexer from Pygments.
    """
    name: str = "Ren'Py"
    aliases: ClassVar[Sequence[str]] = ["renpy", "rpy"]  # type: ignore [reportIncompatibleVariableOverride]
    filenames: ClassVar[Sequence[str]] = ["*.rpy", "*.rpym"]  # type: ignore [reportIncompatibleVariableOverride]

    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]:  # type: ignore [reportIncompatibleMethodOverride]
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
