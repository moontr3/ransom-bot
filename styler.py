# Guide to ANSI markdown
# https://gist.github.com/kkrypt0nn/a02506f3712ff2d1c8ca7c9e0aed7c06
# This library is written by moontr3
# https://github.com/moontr3/

import random
from typing import *

# Pairs of BG/text color that the program shouldn't
# generate because of text being too close in shade
# to background color
DEFAULT_EXCLUDED_PAIRS: List[Tuple[int,int]] = [
  # (bg, fg)
    (40, 30),

    (41, 31),

    (44, 32),
    (46, 32),

    (44, 33),
    (46, 33),
    
    (41, 34),
    (42, 34),
    (43, 34),
    (44, 34),
    (45, 34),
    (46, 34),

    (41, 35),
    (42, 35),
    (43, 35),
    (44, 35),
    (46, 35),

    (42, 36),
    (43, 36),
    (44, 36),
    (45, 36),
    (46, 36),

    (47, 37),

    (47, None),
]

# All supported BG colors (None - no formatting applied)
BG_COLORS: List[int] = [
    None,
    40, # Firefly dark blue
    41, # Orange
    42, # Marble blue
    43, # Greyish turquoise
    44, # Gray
    45, # Indigo
    46, # Light gray
    47, # White
]
# All supported text/FG colors (None - no formatting applied)
FG_COLORS: List[int] = [
    None,
    30, # Gray blue
    31, # Red
    32, # Green
    33, # Yellowuoise
    34, # Blue
    35, # Pink
    36, # Cyan
    37, # White
]


# style

class Style:
    def __init__(self, fg:int, bg:int, bold:bool, underline:bool):
        '''
        Represents a text style.
        '''
        self.fg: int = fg
        self.bg: int = bg
        self.bold: bool = bold
        self.underline: bool = underline


    def get_text(self) -> str:
        '''
        Returns an ASCII representation of the style.
        '''
        styles: List[int] = []
        
        if self.bold: styles.append(1)
        if self.underline: styles.append(4)

        if self.fg != None:
            styles.append(self.fg)
        if self.bg != None:
            styles.append(self.bg)

        return f'\u001b[{";".join(map(str, styles))}m'


# randomly styles given text

def style_single_string(
    string: str,
    reset: bool = True,
    excluded_pairs: List[Tuple[int,int]] = DEFAULT_EXCLUDED_PAIRS
) -> str:
    '''
    Randomly styles given text with one style.
    '''
    # creating random style
    bold = random.choice([True, False])
    underline = random.choice([True, False])

    # colors
    bg = random.choice(BG_COLORS)
    fg = random.choice(FG_COLORS)

    while (bg, fg) in excluded_pairs:
        bg = random.choice(BG_COLORS)
        fg = random.choice(FG_COLORS)

    # styling
    style = Style(fg, bg, bold, underline)
    string = style.get_text() + string

    if reset:
        string += '\u001b[0m'

    return string


# randomly styles given text with multiple styles

class Token:
    def __init__(self, name: str, meta: str):
        self.name: str = name
        self.meta: str = meta


    def split_token(self) -> 'List[Token]':
        '''
        Splits the meta of this token into multiple tokens.
        '''
        return [Token(self.name, meta) for meta in list(self.meta)]
    

    def __repr__(self) -> str:
        return f'{self.name: <10} {self.meta}'


def style_text(
    text: str,
    individual_styling: Literal[
        'letter', 'word'
    ]='letter',
    word_separation: Literal[
        'newline', 'twonewlines', 'codeblock', 'spaces'
    ]='newline',
    newline_separation: Literal[
        'newline', 'twonewlines', 'codeblock'
    ]='newline',
    symbol_separation: Literal[
        'spacebetween', 'spacein', 'both', 'none'
    ]='both',
    case: Literal[
        'asis', 'random', 'allcaps', 'alllower'
    ]='random'
) -> str:
    '''
    Styles given text with multiple styles for each letter.
    '''
    # changing case
    if case == 'random':
        newtext = ''

        for i in text:
            if random.random() > 0.5:
                newtext += i.upper()
            else:
                newtext += i.lower()

        text = newtext

    if case == 'allcaps':
        text = text.upper()

    if case == 'alllower':
        text = text.lower()

    # splitting newlines
    _tokens: List[Token] = []

    # choosing newline separator
    if newline_separation == 'newline':
        separator = Token('nostyle', '\n')
        
    if newline_separation == 'twonewlines':
        separator = Token('nostyle', '\n\n')

    if newline_separation == 'codeblock':
        separator = Token('nostyle', '\n```\n```ansi\n')

    # adding tokens
    index = 0
    for i in text.split('\n'):
        _tokens.append(Token('meta', i))

        index += 1
        if index < len(text.split('\n')):
            _tokens.append(separator)

    # choosing word separator
    if word_separation == 'newline':
        separator = Token('nostyle', '\n')

    if word_separation == 'twonewlines':
        separator = Token('nostyle', '\n\n')

    if word_separation == 'codeblock':
        separator = Token('nostyle', '\n```\n```ansi\n')

    if word_separation == 'spaces':
        separator = Token('nostyle', '  ')

    # splitting words/letters
    tokens: List[Token] = []

    for t in _tokens:
        # non-meta token
        if t.name != 'meta':
            tokens.append(t)
            continue

        # splitting token into words
        word_tokens: List[Token] = []

        for i in t.meta.split():
            word_tokens.append(Token('style', i))
            word_tokens.append(Token('nostyle', ' '))


        # splitting words into letters if needed
        index = 0
        if individual_styling == 'letter':
            for i in word_tokens:
                if i.name == 'nostyle': continue
                
                for _t in i.split_token():
                    if symbol_separation in ['spacein', 'both']:
                        if random.random() > 0.5:
                            _t.meta = ' '+_t.meta
                        if random.random() > 0.5:
                            _t.meta = _t.meta+' '

                    tokens.append(_t)

                    if symbol_separation in ['spacebetween', 'both']:
                        if random.random() > 0.4:
                            tokens.append(Token('nostyle', ' '))

                index += 1
                if index < len(word_tokens):
                    tokens.append(separator)
        else:
            for i in word_tokens:
                tokens.append(i)

                index += 1
                if index < len(word_tokens):
                    tokens.append(separator)

    # converting tokens to string
    out = ''

    for i in tokens:
        if i.name == 'style':
            out += style_single_string(i.meta)

        elif i.name == 'nostyle':
            out += i.meta

    return out
    