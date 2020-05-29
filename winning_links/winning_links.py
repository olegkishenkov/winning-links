import json
import logging
import sys
import urllib.parse

import dateutil.parser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logger = logging.getLogger()


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
    """
    Finds affiliate links that led a client to a shop.
    Each hop represents a single log entry, the outer loop walks through all the hops to the checkout page,
    the second and the third loop trace back the chain of hops that is attached to the mentioned checkout-ending hop.
    :param log_str: a JSON-serialized log string with an array of objects with the following attributes: client_key,
    location_key, referer_key, date_key
    :param client_ids:
    :param client_key:
    :param location_key:
    :param referer_key:
    :param date_key:
    :return: a list of affiliate links or if client_ids is set to True a list of tuples of the form (<client-id>,
    <affiliate-link>)
    """

    log = json.loads(log_str)
    winning_links = []
    for hop in filter(lambda _: _is_checkout(_[location_key]), log):
        logger.debug(
            'checking the hop from {} to {} by client {}'.format(
                hop[referer_key],
                hop[location_key],
                hop[client_key]
            )
        )
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
    if '--debug' in sys.argv:
        logger.setLevel(logging.DEBUG)

    with open(sys.argv[1]) as log_fh:
        log_str = log_fh.read()

    output_str = find_winning_links(log_str, client_ids=True)

    with open(sys.argv[2], 'w') as output_fh:
        output_fh.write(json.dumps(output_str))