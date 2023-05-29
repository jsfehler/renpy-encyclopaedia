"""renpy
init -85 python:
"""

from pygments.formatter import Formatter


class RenpyFormatter(Formatter):
    """Format tokens to use Ren'Py style tags."""
    def __init__(self, **options):
        super().__init__(**options)

        self.styles = {}

        for token, style in self.style:
            start = ''
            end = ''

            if style['color']:
                start += '{{color=#{}}}'.format(style['color'])
                end = '{/color}' + end

            self.styles[token] = (start, end)

    def format(self, tokensource, outfile):
        lastval = ''
        lasttype = None

        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent

            if ttype == lasttype:
                lastval += value

            else:
                if lastval:
                    stylebegin, styleend = self.styles[lasttype]
                    outfile.write(stylebegin + lastval + styleend)

                lastval = value
                lasttype = ttype
