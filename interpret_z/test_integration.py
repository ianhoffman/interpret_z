import os
import unittest
import urllib

from interpret_z import render

class FullIntegrationTestCase(unittest.TestCase):
    context = {
        'beacon_ssl': 'placeholder_beacon',
        'profile': {
            'optout': False,
            'vars': {
                'is_confirmed': False,
                'is_trade': True,
                'unsubscribe_token': 'rand_val'
            }
        },
        'should_show_unsubscribe': True,
        'st_offer': {
            'amount_off': 0,
            'counter_price': 60.00,
            'id': 1
        },
        'st_product': {
            'first_image_attr_dict': {
                'src': 'random_src',
                'srcset': 'random_srcset',
                'sizes': 'some sizes'
            },
            'price': 60.00,
            'title': 'test chair',
            'url': 'placeholder_url'
        },
        'st_related_products': [
            {
                'first_image_attr_dict': {
                    'src': 'random_src',
                    'srcset': 'random_srcset',
                    'sizes': 'some sizes'
                },
                'is_sold': False,
                'num_favorites': 100,
                'price': 120,
                'title': 'rand title',
                'trade_discount_percent': 10,
                'trade_price': 100,
                'url': 'some_url'
            },
            {
                'first_image_attr_dict': {
                    'src': 'random_src',
                    'srcset': 'random_srcset',
                    'sizes': 'some sizes'
                },
                'is_sold': False,
                'num_favorites': 2,
                'price': 120,
                'title': 'rand title',
                'trade_discount_percent': 10,
                'trade_price': 100,
                'url': 'some_url'
            }
        ],
        'subject': 'whatever',
        'unsub_messaging_type_code': 'rand_val',
        'url_stub': urllib.parse.quote('/replace/me?tkadditionalparamstk')
    }

    def test_render_complex_template(self):
        cwd = os.getcwd()
        txt_path = cwd + '/interpret_z/tests/offer_counter_to_buyer.txt'
        html_path = cwd + '/interpret_z/tests/offer_counter_to_buyer.html'

        with open(txt_path, 'r') as f:
            txt_content = f.read()
            result = render(txt_content, self.context)
            self.assertIn('$60', result)

        with open(html_path, 'r') as f:
            html_content = f.read()
            result = render(html_content, self.context)
            self.assertIn('$60', result)
            self.assertIn('$100', result)
            self.assertIn('<strong>Product #:</strong> 1', result)
            self.assertNotIn('/replace/me', result)
            self.assertNotIn('st_product', result)


if __name__ == '__main__':
    unittest.main()
