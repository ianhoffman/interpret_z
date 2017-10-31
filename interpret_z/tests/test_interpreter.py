import unittest

from interpret_z import render
from interpret_z import InterpreterZ
from interpret_z import ParserZ
from interpret_z.scan_z import ScannerZ


class ParserTestCase(unittest.TestCase):
    def _get_interpreted_result(self, text, context):
        context = context or {}
        pz = ParserZ(ScannerZ(text))
        tree = pz.parse()
        iz = InterpreterZ(tree, context)
        return iz.interpret()

    def _assert_all_equal(self, test_cases, context=None):
        for statement, expected in test_cases:
            wrapped = '{' + statement + '}'
            expected = str(expected)
            if expected in ('True', 'False'):
                expected = expected.lower()
            self.assertEqual(
                self._get_interpreted_result(wrapped, context),
                expected
            )

    def test_binary_operators(self):
        self._assert_all_equal(
            (
                ('1 * 2', 2),
                ('1 / 2', 0.5),
                ('2 + 3 / 4 - 2 * 6', -9.25),
                ('(2 + 3) / (4 - 2) * 6', 15.0)
            )
        )

    def test_boolean_operators(self):
        self._assert_all_equal(
            (
                ('1 == 1', True),
                ('1 != 1', False),
                ('1 <= 1', True),
                ('1 < 1', False),
                ('1 >= 1', True),
                ('1 > 1', False)
            )
        )

    def test_boolean_statements(self):
        self._assert_all_equal(
            (
                ('1 == 1 && 1 != 1', False),
                ('1 == 1 || 1 != 1', True),
                ('1 * 1 && 1 != 1', False),
                ('1 - (3 / 3) || 1 - 1 == 2', False),
                # This is a known issue: Python evaluates the following two
                # expressions to 0, but Zephyr evaluates them to false.
                # ('1 && 2 && 0', False),
                # ('1 - 1 && 1 == 1', False),
                # Same thing for this expression: Python evaluates it to 1,
                # but Zephyr expects false.
                # ('(1 || 0) && 1', True)
                # Same goes here: Python expects 2, but Zephyr expected true.
                # ('1 && 2 || 0', 2),
            )
        )

    def test_ternary_statement(self):
        self._assert_all_equal(
            (
                ('1 == 2 ? 1 + 1 : 2 * 2', 4),
                ('1 == (2 > 1 ? 1 : 2) ? (3 - 2) : 6', 1)
            )
        )

    def test_if_logic(self):
        self._assert_all_equal(
            (
                ('if 1 == 1}{1}{else}{2}{/if', 1),
                ('if 1 == 2}{1}{else}{2}{/if', 2),
                ('if (0 == 1 ? 0 : 1) == 1}{3 * 4}{else}{2}{/if', 12),
                ('if 0}{0}{else if 1}{1}{else}{2}{/if', 1),
                ('if 0}{0}{else if 1}{1}{else if 2}{2}{else if 3}{3}{else}{4}{/if', 1),
                (
                    'if 0}{0}{else if 1 == 0}'
                    '{1}'
                    '{else if 2 <= 0 && 3 - 2 == 1}'
                    '{2}'
                    '{else if 3}'
                    '{3}'  
                    '{else}'
                    '{4}'
                    '{/if', 
                    3
                )
            )
        )

    def test_bang_logic(self):
        self._assert_all_equal(
            (
                ('!7', False),
                ('!(7 == 4)', True),
                ('if !(7 == 4) == 0}{1}{else}{2}{/if', 2),
                ('if !4 == 4 || 1 == 1}{1}{else}{2}{/if', 1),
                ('!(1 == 2 ? 1 : 2)', False)
            )
        )

    def test_string_logic(self):
        self._assert_all_equal(
            (
                ('\'123\' + \'hi\'', '123hi'),
                ('\'123\' + 1', '1231'),
                ('\'123\' / \'hi\'', 0)
            )
        )

    def test_var_logic(self):
        context = {
            'x': 1
        }
        self._assert_all_equal(
            (
                ('x', 1),
                ('x == 2', False),
                ('if x == 1}{1}{else}{2}{/if', 1)
            ),
            context=context
        )
        with self.assertRaises(Exception):
            self._assert_all_equal(
                (
                    ('y', 1),
                ),
                context=context
            )

    def test_assignment_logic(self):
        self._assert_all_equal(
            (
                ('x = 1}{x', 1),
                ('x = (3 * 4)}{12', 12),
                ('x = 1}{x}{x = 2}{x', 12),
                ('x = 1}{y = x * 2}{y', 2)
            )
        )

    def test_for_loop_logic(self):
        context = {
            'numbers': [1, 2, 3, 4]
        }
        self._assert_all_equal(
            (
                ('foreach numbers as x}{x}{/foreach', '1234'),
            ),
            context=context
        )

    def test_arrays(self):
        self._assert_all_equal(
            (
                (
                    'x = [1, 2, 3, 4]}'
                    '{foreach x as i}{i}{/foreach',
                    1234
                ),
            )
        )

    def test_dot_notation(self):
        self._assert_all_equal(
            (
                ('x.id', 1),
                ('x.y.val', 3)
            ),
            context={
                'x': {
                    'id': 1,
                    'y': {
                        'val': 3
                    }
                }
            }
        )

    def test_subscripts(self):
        self._assert_all_equal(
            (
                ('x[0]', 1),
                ('x[1]', 2),
                ('x[2].id', 12),
                ('y.var[0]', 20),
                ('z = 0}{x[z]', 1),
            ),
            context={
                'x': [1, 2, {'id': 12}],
                'y': {'var': [20]}
            }
        )

    def test_functions(self):
        self._assert_all_equal(
            (
                ("replace('hi there', 'hi', 'hello')", 'hello there'),
                ('number(12, 2)', '12.00'), # Str to preserve decimals
                ('number(12)', '12'),
                (
                    'u(\'random+param=random&another=123\')', 
                    'random%2Bparam%3Drandom%26another%3D123'
                ),
                (
                    'replace(replace(url_stub, profile.vars.is_confirmed ? '
                    '\'/replace/me\' : u(\'/replace/me\'), ' 
                    'profile.vars.is_confirmed ? \'/collection/decor\' : '
                    'u(\'/collection/decor\')), \'tkadditionalparamstk\', ' 
                    'profile.vars.is_confirmed ? \'guid=12345\' : ' 
                    '\'guid%3D12345\')', 
                    '/collection/decor?guid=12345'
                )
            ),
            context={
                'url_stub': '/replace/me?tkadditionalparamstk',
                'profile': {
                    'vars': {
                        'is_confirmed': True
                    }
                }
            }
        )

    def test_with_html(self):
        template = '<div class="product-grid">' \
                   '<ol>' \
                   '<li>' \
                   '{st_product.id} - {st_product.name}' \
                   '</li>' \
                   '</ol>' \
                   '<ol>' \
                   '{foreach st_related_products as s_rp}' \
                   '<li>{s_rp.id} - {s_rp.name}</li>' \
                   '{/foreach}' \
                   '</ol>' \
                   '</div>'
        result = '<div class="product-grid">' \
                 '<ol>' \
                 '<li>' \
                 '1 - Nice Chair' \
                 '</li>' \
                 '</ol>' \
                 '<ol>' \
                 '<li>2 - Chair Two</li>' \
                 '<li>3 - Chair Three</li>' \
                 '<li>4 - Chair Four</li>' \
                 '</ol>' \
                 '</div>'
        context = {
            'st_product': {
                'id': 1,
                'name': 'Nice Chair'
            },
            'st_related_products': [
                {
                    'id': 2,
                    'name': 'Chair Two'
                },
                {
                    'id': 3,
                    'name': 'Chair Three'
                },
                {
                    'id': 4,
                    'name': 'Chair Four'
                }
            ]
        }

        sz = ScannerZ(template)
        pz = ParserZ(sz)
        iz = InterpreterZ(pz.parse(), context)
        self.assertEqual(
            result, iz.interpret()
        )

    def test_render(self):
        result = render(
            '<div>{st_product.title}</div>',
            {
                'st_product': {
                    'title': 'Nice Chair'
                }
            }
        )
        self.assertEqual(
            result,
            '<div>Nice Chair</div>'
        )


if __name__ == '__main__':
    unittest.main()
