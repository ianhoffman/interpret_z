from enum import Enum

from lib.token_z import TokenZ


def replace(full_str, to_replace, replacement):
    return full_str.replace(to_replace, replacement)

def number(num, places=0):
    import pdb; pdb.set_trace()
    return ('{:.%sf}' % places).format(num) 


ZephyrFuncs = {
    'number': number,
    'replace': replace 
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
