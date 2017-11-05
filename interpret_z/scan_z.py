from interpret_z import ReservedKeywords
from interpret_z import TypesZ
from interpret_z import ZephyrFuncs
from interpret_z import TokenZ


class ScannerZ:
    char_to_token_dict = {
        '(': TokenZ(TypesZ.LPAREN, '('),
        ')': TokenZ(TypesZ.RPAREN, ')'),
        '[': TokenZ(TypesZ.LBRACKET, '['),
        ']': TokenZ(TypesZ.RBRACKET, ']'),
        '.': TokenZ(TypesZ.DOT, '.'),
        ',': TokenZ(TypesZ.COMMA, ','),
        ':': TokenZ(TypesZ.COLON, ':'),
        '?': TokenZ(TypesZ.QUESTION, '?'),
        '+': TokenZ(TypesZ.PLUS, '+'),
        '-': TokenZ(TypesZ.MINUS, '-'),
        '*': TokenZ(TypesZ.MUL, '*'),
        '%': TokenZ(TypesZ.MOD, '%'),
        '/': 'id_div',
        '<': 'id_lt',
        '>': 'id_gt',
        '=': 'id_eq',
        '!': 'id_bang',
        '&': 'id_and',
        '|': 'id_or'
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.zephyr_mode = False # indicates that we're parsing Zephyr code and not txt/html.

    def advance(self, count=1):
        self.pos += count 
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text) - 1:
            return self.text[peek_pos]
        else:
            return None

    def lookback(self):
        lookback_pos = self.pos - 1
        if lookback_pos >= 0:
            return self.text[lookback_pos]
        else:
            return None

    def skip_whitespace(self):
        while self.current_char.isspace() and self.current_char is not None:
            self.advance()

    def identify(self):
        result = ''
        if self.current_char == '/': # Endfor or Endif
            result += self.current_char
            self.advance()
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == '_'
        ):
            result += self.current_char
            self.advance()
        if result in ZephyrFuncs:
            return TokenZ(TypesZ.FUNC, result)
        else:
            return ReservedKeywords.as_dict().get(result, TokenZ(TypesZ.VAR, result))

    def id_and(self):
        if self.peek() == '&':
            self.advance(2)
            return TokenZ(TypesZ.AND, '&&')
        raise NotImplemented('Binary operators haven\'t been implemented yet.')

    def id_bang(self):
        if self.peek() == '=':
            self.advance(2)
            return TokenZ(TypesZ.NEQ, '!=')
        else:
            self.advance()
            return TokenZ(TypesZ.BANG, '!')

    def id_div(self):
        if self.lookback() == '{':
            return self.identify()
        else:
            self.advance()
            return TokenZ(TypesZ.DIV, '/')

    def id_lt(self):
        if self.peek() == '=':
            self.advance(2)
            return TokenZ(TypesZ.LTE, '<=')
        else:
            self.advance()
            return TokenZ(TypesZ.LT, '<')

    def id_eq(self):
        if self.peek() == '=':
            self.advance(2)
            return TokenZ(TypesZ.EQEQ, '==')
        else:
            self.advance()
            return TokenZ(TypesZ.EQ, '=')

    def id_gt(self):
        if self.peek() == '=':
            self.advance(2)
            return TokenZ(TypesZ.GTE, '>=')
        else:
            self.advance()
            return TokenZ(TypesZ.GT, '>')

    def id_or(self):
        if self.peek() == '|':
            self.advance(2)
            return TokenZ(TypesZ.OR, '||')
        raise NotImplemented('Binary operators haven\'t been implemented yet.')

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isnumeric():
            result += self.current_char
            self.advance()
        if self.current_char == '.': # Floating point
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isnumeric():
                result += self.current_char
                self.advance()
            if result[-1] == '.':
                raise Exception('Real val cannot terminate with \'.\'')
            return TokenZ(TypesZ.REAL, float(result))
        return TokenZ(TypesZ.INTEGER, int(result))

    def string(self):
        result = ''
        self.advance() # Skip the quotation mark
        while self.current_char is not None and (
            self.current_char != '\'' and self.current_char != '"'
        ):
            result += self.current_char
            self.advance()
        self.advance() # Skip the closing quotation mark
        return TokenZ(TypesZ.STRING, result)

    def html_or_text(self):
        result = ''
        while self.current_char is not None and self.current_char != '{':
            result += self.current_char
            self.advance()
        if all(css_keyword in result for css_keyword in ['text/css', '<style']):
            # Good indicatio that this is CSS which should be skipped.
            while result[-8:] != '</style>' and self.current_char is not None:
                result += self.current_char
                self.advance()
        return TokenZ(TypesZ.HTML_OR_TEXT, result)

    def tokenize(self):
        if self.current_char is None:
            return None

        if self.current_char == '{':
            self.zephyr_mode = True
            self.advance()
            return TokenZ(TypesZ.LBRACE, '{')
        
        if self.current_char == '}':
            self.zephyr_mode = False
            self.advance()
            return TokenZ(TypesZ.RBRACE, '}')

        if not self.zephyr_mode:
            return self.html_or_text()

        if self.current_char.isspace():
            self.skip_whitespace()

        if self.current_char.isnumeric():
            return self.number()

        if self.current_char == '\'' or self.current_char == '"':
            return self.string()

        if self.current_char.isalpha():
            return self.identify()

        result = self.char_to_token_dict.get(self.current_char)
        if type(result) is str:
            result = getattr(self, result)
            return result()
        elif result is not None:
            self.advance()
            return result
        else:
            import pdb; pdb.set_trace()
            raise Exception('Invalid character: %s' % self.current_char)

    def scan(self):
        tokens = []
        while self.current_char is not None:
            tokens.append(self.tokenize())
        return tokens

