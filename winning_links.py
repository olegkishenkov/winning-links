import json
import urllib.parse

import dateutil.parser


def is_checkout(link):
    result = urllib.parse.urlparse(link)
    return (result.hostname == 'shop.com') and (result.path == '/checkout')


def is_ours(link):
    result = urllib.parse.urlparse(link)
    return result.hostname == 'referal.ours.com'


def is_theirs(link):
    result = urllib.parse.urlparse(link)
    return (result.hostname == 'ad.theirs1.com') or (result.hostname == 'ad.theirs2.com')


def find_winning_links(log_str):
    log = json.loads(log_str)
    winning_links = []
    for hop in filter(lambda _: is_checkout(_['document.location']), log):
        log_this_client = list(filter(lambda _: _['client_id'] == hop['client_id'], log))
        for hop_this in log_this_client:
            winning_link_candidate = hop['document.referer']
            for hop_ in log_this_client:
                if hop_['document.location'] == hop_this['document.referer']:
                    if dateutil.parser.parse(hop_['date']) < dateutil.parser.parse(hop_this['date']):
                        winning_link_candidate = hop_['document.referer']
            if is_ours(winning_link_candidate):
                winning_links.append(winning_link_candidate)
                break
            if is_theirs(winning_link_candidate):
                break
    return winning_links


if __name__ == '__main__':
    with open('log.json') as log_fh:
        log_str = log_fh.read()
    print(find_winning_links(log_str))
