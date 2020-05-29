import json
import sys
import logging

try:
    from winning_links import find_winning_links
except (ImportError, ModuleNotFoundError) as e:
    from winning_links.winning_links import find_winning_links

argv1 = list(sys.argv)
argv1.sort(key=lambda _: -_.startswith('--debug'))

try:
    logging.basicConfig()
    logger = logging.getLogger('winning_links')
    logger.setLevel(getattr(logging, argv1[0].split('=')[1]))
except IndexError:
    pass

with open(sys.argv[1]) as log_fh:
    log_str = log_fh.read()

output_str = find_winning_links(log_str, client_ids=True)

with open(sys.argv[2], 'w') as output_fh:
    output_fh.write(json.dumps(output_str))