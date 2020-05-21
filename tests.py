import unittest

from winning_links import find_winning_links as fwl


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
