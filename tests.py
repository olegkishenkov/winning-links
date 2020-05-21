import unittest

from winning_links import find_winning_links as fwl


class TestFindWinningLinks(unittest.TestCase):
    def test_find_winning_links_search_engine_shop(self):
        log_string = '''{
    "client_id": "user15",
    "User-Agent": "Firefox 59",
    "document.location": "https://shop.com/checkout",
    "document.referer": "https://yandex.ru/search/?q=купить+котика",
    "date": "2018-04-03T07:59:13.286000Z"
}'''
        log_string = '''[
{}
]'''.format(log_string)
        links = fwl(log_string)
        self.assertEqual(links, [])