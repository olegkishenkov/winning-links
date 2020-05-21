import json
import urllib.parse

import dateutil.parser


def is_checkout(link):
    return urllib.parse.urlparse(link).hostname == 'https://shop.com/checkout'


def is_ours(link):
    return _(link) == 'referral.ours'


log = json.loads('log.json')
winning_links = []

for hop in filter(lambda _: is_checkout(['document.location']), log):
    log_this_client = list(filter(lambda _: _['client_id'] == hop['client_id'], log))
    hop_this = log_this_client[0]
    while True:
        hop_pre = None
        for hop_ in log_this_client:
            if hop_['document.location'] == hop['document.referer']:
                if dateutil.parser.parse(hop_['date']) < dateutil.parser.parse(hop['date']):
                    hop_pre = hop_
        if is_ours(hop_pre['document.referrer']):
            winning_links.append(hop_pre['document.referrer'])
            break

print(winning_links)
