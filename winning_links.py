import json
import urllib.parse

import dateutil.parser


def _is_checkout(link):
    result = urllib.parse.urlparse(link)
    return (result.hostname == 'shop.com') and (result.path == '/checkout')


def _is_ours(link):
    result = urllib.parse.urlparse(link)
    return result.hostname == 'referal.ours.com'


def _is_theirs(link):
    result = urllib.parse.urlparse(link)
    return (result.hostname == 'ad.theirs1.com') or (result.hostname == 'ad.theirs2.com')


def find_winning_links(
        log_str,
        client_ids=False,
        client_key='client_id',
        location_key='document.location',
        referer_key='document.referer',
        date_key='date',
):

    log = json.loads(log_str)
    winning_links = []
    for hop in filter(lambda _: _is_checkout(_[location_key]), log):
        client = hop[client_key]
        log_this_client = list(filter(lambda _: _[client_key] == client, log))
        for hop_this in log_this_client:
            winning_link_candidate = hop[referer_key]
            for hop_ in log_this_client:
                if hop_[location_key] == hop_this[referer_key]:
                    if dateutil.parser.parse(hop_[date_key]) < dateutil.parser.parse(hop_this[date_key]):
                        winning_link_candidate = hop_[referer_key]
            if _is_ours(winning_link_candidate):
                if client_ids:
                    winning_links.append((client, winning_link_candidate))
                else:
                    winning_links.append(winning_link_candidate)
                break
            if _is_theirs(winning_link_candidate):
                break
    return winning_links


if __name__ == '__main__':
    with open('log.json') as log_fh:
        log_str = log_fh.read()
    print(find_winning_links(log_str, client_ids=True))
