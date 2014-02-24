import json
from collections import OrderedDict, defaultdict
import sys, os, re, copy, datetime, unicodecsv

def group_files(d):
    out = OrderedDict()
    publisher_re = re.compile('(.*)\-[^\-]')
    for k,v in d.items():
        out[k] = OrderedDict()
        for k2,v2 in v.items():
            if type(v2) == list:
                out[k][k2] = OrderedDict()
                v2.sort()
                for listitem in v2:
                    publisher = publisher_re.match(listitem).group(1)
                    if not publisher in out[k][k2]:
                        out[k][k2][publisher] = []
                    out[k][k2][publisher].append(listitem)
            else:
                out[k][k2] = v2
    return out

current_stats = {
    'aggregated': json.load(open('./stats-calculated/current/aggregated.json'), object_pairs_hook=OrderedDict),
    'inverted_publisher': json.load(open('./stats-calculated/current/inverted-publisher.json'), object_pairs_hook=OrderedDict),
    'inverted_file': json.load(open('./stats-calculated/current/inverted-file.json'), object_pairs_hook=OrderedDict),
    'download_errors': []
}
current_stats['inverted_file_grouped'] = group_files(current_stats['inverted_file'])
ckan_publishers = json.load(open('./data/ckan_publishers.json'), object_pairs_hook=OrderedDict)
ckan = json.load(open('./stats-calculated/ckan.json'), object_pairs_hook=OrderedDict)
gitdate = json.load(open('./stats-calculated/gitdate.json'), object_pairs_hook=OrderedDict)
with open('./data/downloads/errors') as fp:
    for line in fp:
        if line != '.\n':
            current_stats['download_errors'].append(line.strip('\n').split(' ', 3))
data_tickets = defaultdict(list)
with open('./data/issues.csv') as fp:
    # Skip BOM
    fp.read(3)
    reader = unicodecsv.DictReader(fp)
    for issue in reader:
        data_tickets[issue['data_provider_regisrty_id']].append(issue)


def get_publisher_stats(publisher, stats_type='aggregated'):
    try:
        return json.load(open('./stats-calculated/current/{0}-publisher/{1}.json'.format(stats_type, publisher)), object_pairs_hook=OrderedDict)
    except IOError:
        return {}
