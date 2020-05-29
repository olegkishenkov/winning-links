import logging
import unittest

try:
    from winning_links import find_winning_links as fwl, _is_checkout, _is_ours, _is_theirs
except (ImportError, ModuleNotFoundError) as e:
    from winning_links.winning_links import find_winning_links as fwl, _is_checkout, _is_ours, _is_theirs

logging.basicConfig()
winning_links_logger = logging.getLogger('winning_links')
winning_links_logger.setLevel(logging.DEBUG)


class TestFindWinningLinks(unittest.TestCase):
    def test_find_winning_links__search_engine_to_checkout(self):
        log_str = '''    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://yandex.ru/search/?q=купить+котика",
        "date": "2018-04-03T07:59:13.286000Z"
    }'''
        log_str = '''[
{}
]'''.format(log_str)
        links = fwl(log_str)
        self.assertEqual(links, [])

    def test_find_winning_links__ours_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, ['https://referal.ours.com/?ref=0xc0ffee'])

    def test_find_winning_links__theirs1_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://ad.theirs1.com/?src=q1w2e3r4",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, [])

    def test_find_winning_links__ours_to_theirs1_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://ad.theirs1.com/?src=q1w2e3r4",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://ad.theirs1.com/?src=q1w2e3r4",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, [])

    def test_find_winning_links__theirs1_to_ours_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://referal.ours.com/?ref=0xc0ffee",
        "document.referer": "https://ad.theirs1.com/?src=q1w2e3r4",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, ['https://referal.ours.com/?ref=0xc0ffee'])

    def test_find_winning_links__ours_to_cart_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/cart",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://shop.com/cart",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, ['https://referal.ours.com/?ref=0xc0ffee'])

    def test_find_winning_links__theirs1_to_cart_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/cart",
        "document.referer": "https://ad.theirs1.com/?src=q1w2e3r4",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://shop.com/cart",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, [])

    def test_find_winning_links__ours_to_cart_to_checkout_to_cart_to_checkout(self):
        """
        when a client reaches the checkout twice not leaving the shop, the affiliate link she
        came to the shop with is counted twice
        """
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/cart",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://shop.com/cart",
        "date": "2018-04-03T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/cart",
        "document.referer": "https://shop.com/checkout",
        "date": "2018-04-04T07:59:13.286000Z"
    },
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://shop.com/cart",
        "date": "2018-04-05T07:59:13.286000Z"
    }
]'''
        links = fwl(log_str)
        self.assertEqual(links, [
            'https://referal.ours.com/?ref=0xc0ffee',
            'https://referal.ours.com/?ref=0xc0ffee',
        ])

    def test_find_winning_links__client1_ours_to_checkout__client2_theirs1_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user16",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://ad.theirs1.com/?src=q1w2e3r4",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        self.assertTrue(('user15', 'https://referal.ours.com/?ref=0xc0ffee') in fwl(log_str, client_ids=True))
        self.assertFalse(('user16', 'https://ad.theirs1.com/?src=q1w2e3r4') in fwl(log_str, client_ids=True))

    def test_find_winning_links__client1_ours_to_checkout__client2_ours_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user15",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-04-02T07:59:13.286000Z"
    },
    {
        "client_id": "user16",
        "User-Agent": "Firefox 59",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://referal.ours.com/?ref=123hexcode",
        "date": "2018-04-03T07:59:13.286000Z"
    }
]'''
        self.assertTrue(('user15', 'https://referal.ours.com/?ref=0xc0ffee') in fwl(log_str, client_ids=True))
        self.assertTrue(('user16', 'https://referal.ours.com/?ref=123hexcode') in fwl(log_str, client_ids=True))

    def test_find_winning_links__client_ours_to_index_to_products_to_cart_to_checkout(self):
        log_str = '''[
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/",
        "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
        "date": "2018-05-23T18:59:13.286000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/products/id?=10",
        "document.referer": "https://shop.com/",
        "date": "2018-05-23T18:59:20.119000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/products/id?=25",
        "document.referer": "https://shop.com/products/id?=10",
        "date": "2018-05-23T19:04:20.119000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/cart",
        "document.referer": "https://shop.com/products/id?=25",
        "date": "2018-05-23T19:05:13.123000Z"
    },
    {
        "client_id": "user7",
        "User-Agent": "Chrome 65",
        "document.location": "https://shop.com/checkout",
        "document.referer": "https://shop.com/cart",
        "date": "2018-05-22T18:05:59.224000Z"
    }
]'''
        self.assertTrue(('user7', 'https://referal.ours.com/?ref=0xc0ffee') in fwl(log_str, client_ids=True))

    def test_find_winning_links__client1_to_products_to_checkout__client2_to_products_to_checkout(self):
        log_str = '''[
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
                "date": "2018-05-23T18:59:13.286000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://ad.theirs1.com/?src=q1w2e3r4",
                "date": "2018-05-23T18:59:13.286000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-05-23T18:59:20.119000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-05-23T18:59:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-05-23T19:04:20.119000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-05-23T19:04:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-05-23T19:05:13.123000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-05-23T19:05:13.123000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart",
                "date": "2018-05-22T18:05:59.224000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart",
                "date": "2018-05-22T18:05:59.224000Z"
            }
        ]'''
        self.assertTrue(('user7', 'https://referal.ours.com/?ref=0xc0ffee') in fwl(log_str, client_ids=True))
        self.assertFalse(('user8', 'https://ad.theirs1.com/?src=q1w2e3r4') in fwl(log_str, client_ids=True))


class TestUnderscoreFunctions(unittest.TestCase):
    def test__is_checkout__this_shop_checkout(self):
        self.assertTrue(_is_checkout('https://shop.com/checkout'))

    def test__is_checkout__another_shop_checkout(self):
        self.assertFalse(_is_checkout('https://anothershop.com/checkout'))

    def test__is_checkout__this_shop_product(self):
        self.assertFalse(_is_checkout('https://shop.com/products/id?=25'))

    def test__is_ours__ours(self):
        self.assertTrue(_is_ours('https://referal.ours.com/?ref=0xc0ffee'))

    def test__is_ours__shop(self):
        self.assertFalse(_is_ours('https://shop.com/products/id?=10'))

    def test__is_ours__theirs(self):
        self.assertFalse(_is_ours('https://ad.theirs1.com/?src=q1w2e3r4'))

    def test__is_theirs__thiers(self):
        self.assertTrue(_is_theirs('https://ad.theirs1.com/?src=q1w2e3r4'))

    def test__is_theirs__ours(self):
        self.assertFalse(_is_theirs('https://referal.ours.com/?ref=0xc0ffee'))

    def test__is_theirs__shop(self):
        self.assertFalse(_is_ours('https://shop.com/products/id?=10'))


if __name__ == '__main__':
    unittest.main()
