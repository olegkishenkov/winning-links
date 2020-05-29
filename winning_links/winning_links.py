import json
import logging
import pprint
import sys
from urllib.parse import urlparse, urljoin

import dateutil.parser

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _is_checkout(link):
    result = urlparse(link)
    return (result.hostname == 'shop.com') and (result.path == '/checkout')


def _is_ours(link):
    result = urlparse(link)
    return result.hostname == 'referal.ours.com'


def _is_theirs(link):
    result = urlparse(link)
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
    Each hop represents a single log entry, the outer loop walks through all the hops to the checkout webpage,
    the second loop traces back the chain of hops that is attached to the mentioned checkout-ending hop. Once a
    hop is discovered the search (backward) for the next hop continues from the beginning of the inner loop.
    The traceback ends when a hop in the chain is either classified as a hop from our link or a hop from their link
    or we have looped over all the hops by the related client
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
    logging.debug('initialized winning_links to []')
    for hop in filter(lambda _: _is_checkout(_[location_key]), log):
        logger.info(
            'checking the hop from {} to {} by client {}'.format(
                hop[referer_key],
                hop[location_key],
                hop[client_key]
            )
        )
        client = hop[client_key]
        log_this_client = list(filter(lambda _: _[client_key] == client, log))
        log_this_client_len = len(log_this_client)
        referer_prev = urljoin('https://shop.com', 'checkout') #hop[referer_key]
        date_prev = dateutil.parser.parse('9999-12-12T23:59:59.286000Z')
        i = 0
        while i < log_this_client_len:
            if not (log_this_client[i][location_key] == referer_prev):
                i += 1
                logger.info('location != referer_prev, going to the next hop_...')
                continue
            if not dateutil.parser.parse(log_this_client[i][date_key]) < date_prev:
                i += 1
                logger.info('this hop is fresher than the previous, going to the next hop...')
                continue
            if _is_ours(log_this_client[i][referer_key]):
                if client_ids:
                    winning_links.append((client, log_this_client[i][referer_key]))
                else:
                    winning_links.append(log_this_client[i][referer_key])
                logger.info('a winning link {} found and stored! \ngoing to the next checkout case...'.format(
                        log_this_client[i][referer_key],
                    )
                )
                break
            if _is_theirs(log_this_client[i][referer_key]):
                logger.info(
                    'a losing link found {} - this chain is our shame! going to the next checkout case...'.format(
                        log_this_client[i][referer_key],
                    )
                )
                break
            referer_prev = log_this_client[i][referer_key]
            logger.info('hop from {} to {} found, going back...'.format(
                log_this_client[i][referer_key],
                log_this_client[i][location_key],
            ))
            i = 0
    logger.debug('winning_links {}'.format(pprint.pformat(winning_links)))
    return winning_links


if __name__ == '__main__':
    argv1 = list(sys.argv)
    argv1.sort(key=lambda _: -_.startswith('--debug'))
    try:
        logger.setLevel(getattr(logging, argv1[0].split('=')[1]))
    except IndexError:
        pass

    with open(sys.argv[1]) as log_fh:
        log_str = log_fh.read()

    output_str = find_winning_links(log_str, client_ids=True)

    with open(sys.argv[2], 'w') as output_fh:
        output_fh.write(json.dumps(output_str))