import json

import dateutil.parser

log = json.loads('log.json')

for hop in filter(lambda _: _['document.location'] == 'https://shop.com/checkout', log):
    log_this_client = filter(lambda _: _['client_id'] == hop['client_id'], log)
    iter(log_this_client)
    hop_pre_candidates = []
    while True:
        try:
            hop_ = next(log_this_client)
        except StopIteration:
            break
        else:
            if hop_['document.location'] == hop['document.referer']:
                hop_pre_candidates.append(hop_)
    hop_pre = hop_pre_candidates.sort(key=lambda _: dateutil.parser.parse(_['date']), reverse=True)[0]


