import json
import sys

from .winning_links import find_winning_links

with open(sys.argv[1]) as log_fh:
    log_str = log_fh.read()

output_str = find_winning_links(log_str, client_ids=True)

with open(sys.argv[2], 'w') as output_fh:
    output_fh.write(json.dumps(output_str))