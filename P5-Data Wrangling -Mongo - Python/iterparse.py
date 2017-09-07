
####>>>>>Iterative Parsing through an XML File<<<<<####

import xml.etree.cElementTree as ET
import pprint as pp
import re
from collections import defaultdict
import operator

# filename = 'calcutta_subset.xml'
filename = 'Calcutta.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

####>>>>> Basic Tags count <<<<<####
def count_tags(filename):
    tree = ET.iterparse(filename)
    tags = dict()
    for event, element in tree:
        tags.setdefault(element.tag, 0)
        tags[element.tag] += 1
    return tags

####>>>>>Checking for regex characters in  tags == "tags"<<<<<####
def char_check(filename, keys):
    for event, element in ET.iterparse(filename):
        if element.tag == "tag":
            if lower.search(element.attrib['k']):
                keys['lower'] += 1
            elif lower_colon.search(element.attrib['k']):
                keys['lower_colon'] += 1
            elif problemchars.search(element.attrib['k']):
                keys['problemchars'] += 1
            else:
                keys['other'] += 1
    return keys

####>>>>> keys stored in each `tag` element, in the `k` attribute <<<<<####
def count_k_tags(filename):
    tag_keys_count = {}
    t_k_cnt = 0
    for _, element in ET.iterparse(filename, events=("start",)):
        if element.tag == 'tag' and 'k' in element.attrib:
            tag_keys_count.setdefault(element.get('k'), 0)
            tag_keys_count[element.get('k')] += 1
    
    # t_k_cnt = sum(tag_keys_count.values())
    tag_keys_count = sorted(tag_keys_count.items(), key=operator.itemgetter(1))[::-1]
    
    return tag_keys_count

def sample_k_data(filename, tags, data_limit=15):
    tags = [i[0] for i in tags]
    data = defaultdict(set)

    for _, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if 'k' not in tag.attrib or 'v' not in tag.attrib:
                    continue
                key = tag.get('k')
                val = tag.get('v')
                if key in tags and len(data[key]) < data_limit:
                    data[key].add(val)
    return dict(data)

## ***** Main **** ##
def main(filename):
    print "Tags Count: \n"
    pp.pprint(count_tags(filename))
    print "\n"
    print "'k' atrribute Char Check: \n"
    pp.pprint(char_check(filename, keys))
    print "\n"
    print "'k' Tags Count: \n"
    tags_k_count = count_k_tags(filename)
    pp.pprint(tags_k_count)
    print "\n"
    print "sample'k' data: \n"
    pp.pprint(sample_k_data(filename, tags_k_count))


if __name__ == '__main__':
    main(filename)