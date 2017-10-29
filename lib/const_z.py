from enum import Enum

from lib.token_z import TokenZ


ZephyrFuncs = {
    'replace'
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
    FUNCTION = 'FUNCTION'
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
