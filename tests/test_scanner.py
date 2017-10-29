import unittest

from lib.const_z import TypesZ
from lib.scan_z import ScannerZ
from lib.token_z import TokenZ


class TokenZTestCase(unittest.TestCase):
    def test_token_init_and_str(self):
        z_tokens = [TokenZ(z_type.name, 'foo') for z_type in TypesZ]
        for i, z_type in enumerate(TypesZ):
            self.assertEqual(
                str(z_tokens[i]),
                'TokenZ({z_type}, foo)'.format(
                    z_type=z_type.name
                )
            )


class ScannerZTestCase(unittest.TestCase):
    def test_scanner_init(self):
        content = 'foobar'
        sz = ScannerZ(content)
        self.assertEqual(sz.pos, 0)
        self.assertEqual(sz.text, content)
        self.assertEqual(sz.current_char, content[0])

    def test_tokenize(self):
        content = '{123 abc 3.001}'
        sz = ScannerZ(content)
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(LBRACE, {)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(INTEGER, 123)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(VAR, abc)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(REAL, 3.001)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(RBRACE, })'
        )

    def test_tokenize_math(self):
        content = '{1 + 2 / 3.001}'
        sz = ScannerZ(content)
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(LBRACE, {)',
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(INTEGER, 1)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(PLUS, +)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(INTEGER, 2)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(DIV, /)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(REAL, 3.001)'
        )

    def test_tokenize_control_flow(self):
        content = '{foreach}{if}{/if}{/foreach}'
        sz = ScannerZ(content)
        sz.tokenize() # Skip LBRACE
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(FORLOOP, None)'
        )
        sz.tokenize() # Skip RBRACE
        sz.tokenize() # Skip LBRACE
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(IF, None)'
        )
        sz.tokenize() # Skip RBRACE
        sz.tokenize() # Skip LBRACE
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(ENDIF, None)'
        )
        sz.tokenize() # Skip RBRACE
        sz.tokenize() # Skip LBRACE
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(ENDFOR, None)'
        )

    def test_tokenize_conditionals(self):
        content = '{< <= == = >= >}'
        sz = ScannerZ(content)
        sz.tokenize() # skip LBRACE
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(LT, <)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(LTE, <=)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(EQEQ, ==)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(EQ, =)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(GTE, >=)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(GT, >)'
        )

    def test_complex_statement(self):
        content = '{st_product.id > 3 ? replace(st_product[1], \'foo\', \'bar\')}'
        expected_results = (
            'TokenZ(LBRACE, {)',
            'TokenZ(VAR, st_product)',
            'TokenZ(DOT, .)',
            'TokenZ(VAR, id)',
            'TokenZ(GT, >)',
            'TokenZ(INTEGER, 3)',
            'TokenZ(QUESTION, ?)',
            'TokenZ(FUNCTION, replace)',
            'TokenZ(LPAREN, ()',
            'TokenZ(VAR, st_product)',
            'TokenZ(LBRACKET, [)',
            'TokenZ(INTEGER, 1)',
            'TokenZ(RBRACKET, ])',
            'TokenZ(COMMA, ,)',
            'TokenZ(STRING, foo)',
            'TokenZ(COMMA, ,)',
            'TokenZ(STRING, bar)',
            'TokenZ(RPAREN, ))',
            'TokenZ(RBRACE, })'
        )
        sz = ScannerZ(content)
        for er in expected_results:
            self.assertEqual(
                str(sz.tokenize()),
                er
            )

    def test_with_html_content(self):
        content = '<div class="test-class">{zephyr_code}</div><a {zephyr_code}>'
        expected_results = (
            'TokenZ(HTML_OR_TEXT, <div class="test-class">)',
            'TokenZ(LBRACE, {)',
            'TokenZ(VAR, zephyr_code)',
            'TokenZ(RBRACE, })',
            'TokenZ(HTML_OR_TEXT, </div><a )',
            'TokenZ(LBRACE, {)',
            'TokenZ(VAR, zephyr_code)',
            'TokenZ(RBRACE, })',
            'TokenZ(HTML_OR_TEXT, >)'
        )
        sz = ScannerZ(content)
        for er in expected_results:
            self.assertEqual(
                str(sz.tokenize()),
                er
            )

    def test_css_is_not_zephyr(self):
        content = '<style type="text/css"> #id { padding: 10px }</style>{sailthru}'
        sz = ScannerZ(content)
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(HTML_OR_TEXT, <style type="text/css"> #id { padding: 10px }</style>)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(LBRACE, {)'
        )
        self.assertEqual(
            str(sz.tokenize()),
            'TokenZ(VAR, sailthru)'
        )


if __name__ == '__main__':
    unittest.main()

