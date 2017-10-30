from enum import Enum
from urllib.parse import quote

from lib.token_z import TokenZ


ZephyrFuncs = {
    'length': lambda t: len(t),
    'number': lambda n, places=0: ('{:.%sf}' % places).format(n),
    'replace': lambda s, old, new: s.replace(old, new),
    'substr': lambda string, start, end: string[start:end],
    'u': lambda text: quote(text)
}


class TypesZ(Enum):
    AND = 'AND'
    BANG = 'BANG'
    COLON = 'COLON'
    COMMA = 'COMMA'
    DIV = 'DIV'
    DOT = 'DOT'
    EQ = 'EQ'
    EQEQ = 'EQEQ'
    FUNC = 'FUNC'
    GT = 'GT'
    GTE = 'GTE'
    HTML_OR_TEXT = 'HTML_OR_TEXT'
    INTEGER = 'INTEGER'
    LBRACE = 'LBRACE'
    LBRACKET = 'LBRACKET'
    LPAREN = 'LPAREN'
    LT = 'LT'
    LTE = 'LTE'
    MINUS = 'MINUS'
    MOD = 'MOD'
    MUL = 'MUL'
    NEQ = 'NEQ'
    OR = 'OR'
    PLUS = 'PLUS'
    QUESTION = 'QUESTION'
    RBRACE = 'RBRACE'
    RBRACKET = 'RBRACKET'
    RPAREN = 'RPAREN'
    REAL = 'REAL'
    STRING = 'STRING'
    VAR = 'VAR'

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self) 


class ReservedKeywords(Enum):
    AS = 'as'
    ELSE = 'else'
    ENDFOR = '/foreach'
    ENDIF = '/if'
    FALSE = 'false'
    FORLOOP = 'foreach'
    IF = 'if'
    TRUE = 'true'

    def __eq__(self, other):
        return self.name == other

    @classmethod
    def as_dict(cls):
        return {
            m.value: TokenZ(m.name, None)
            for m in cls.__members__.values()
        }
