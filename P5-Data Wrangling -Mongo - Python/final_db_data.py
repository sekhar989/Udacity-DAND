#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint
import codecs
import json
import re
import xml.etree.ElementTree as ET
import audit_db

## ********** Builds JSON file from OSM. Parses, cleans, and shapes data accordingly ********** ##

# filename = "calcutta_subset.xml"
filename = "Calcutta.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
address_regex = re.compile(r'^addr\:')
street_regex = re.compile(r'^street')
gnis_regex = re.compile(r'^gnis\:')

## All zipcodes in Calcutta are between 700001 & 700120 ###
zipcodes = [str(i) for i in range(700001,700110)]

## Regex Compiler ##
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
digit_only = re.compile(r'\d+')

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Sarani", "Park", "Connector", "Gardens"]

mapping = { "St": "Street", "St.": "Street", "street" : "Street", "Sarani" : "Sarani",
            "Ave" : "Avenue", "Rd." : "Road", "road" : "Road", "ROAD" : "Road", "ROad" : "Road",
            "Rd" : "Road", "N." : "North", "Ln" : "Lane" }



CREATED = ['version', 'changeset', 'timestamp', 'user', 'uid']
IGNORED_TAGS = ['name:ta', 'name:te', 'is_in:city', 'name:de','fax', 'source:name', 'name:uk', 'payment:bitcoin', 
                'name:eo','name:zh', 'AND_a_nosr_r', 'internet_access:fee', 'name:et', 'name:es', 'internet_access',
                'is_capital', 'ref:new', 'area:highway', 'name:it', 'loc_name', 'name:ru', 'phone_2', 'phone_3',
                'phone_1', 'local_ref', 'brand:wikidata', 'capital', 'is_in', 'ref','contact:email', 'name:ja',
                'is_in:continent', 'electrified', 'denomination', 'water', 'name:bn', 'ref:old', 'footway', 'place:cca',
                'craft', 'alt_name:pl','drive_through', 'name_1', 'name:pl', 'admin_level', 'end_date', 'name:hi', 'building_1', 
                'is_in:state', 'old_name', 'passenger_lines', 'AND:importance_level', 'country',  'wheelchair', 'bridge',
                'alt_name:eo', 'toilets:disposal', 'surface', 'wikidata', 'foot_1','emergency', 'is_in:country',
                'building:levels', 'cycleway', 'note', 'name:fr', 'GNS:id', 'description', 'drink', 'is_in:country_code',
                'name:abbr', 'delivery', 'IR:zone','artwork_type', 'url', 'colour', 'outdoor_seating', 'is_in:iso_3166_2',
                'takeaway','created_by']

def format_data(element):
    ignored_tags = IGNORED_TAGS
    node = {}
    if element.tag == "node" or element.tag == "way" :
        
        node['type'] = element.tag

        # Parse attributes
        for a in element.attrib:
            if a in CREATED:
                if 'created' not in node:
                    node['created'] = {}
                node['created'][a] = element.attrib[a]

            elif a in ['lat', 'lon']:
                if 'pos' not in node:
                    node['pos'] = [None, None]
                if a == 'lat':
                    node['pos'][0] = float(element.attrib[a])
                else:
                    node['pos'][1] = float(element.attrib[a])

            else:
                node[a] = element.attrib[a]

        # Iterate tag children
        for tag in element.iter("tag"):
            if not problemchars.search(tag.attrib['k']):
                # Tags with single colon
                if lower_colon.search(tag.attrib['k']):

                    # Ignored Tags
                    if tag.attrib['k'] in ignored_tags:
                        continue

                    # Single colon beginning with addr
                    if tag.attrib['k'].find('addr') == 0:
                        if 'address' not in node:
                            node['address'] = {}

                        sub_attr = tag.attrib['k'].split(':', 1)

                        #*******if addr:city, city = Kolkata *******
                        if sub_attr[1] == "city":
                            node['address'][sub_attr[1]] = "Kolkata"

                        #*******if addr:state, state = West Bengal  *******
                        if sub_attr[1] == "state":
                            node['address'][sub_attr[1]] = "West Bengal"

                        #*******if addr:country, country = India  *******
                        if sub_attr[1] == "country":
                            node['address'][sub_attr[1]] = "India"

                        #*******if street name, audit as street *******
                        if sub_attr[1] == "street":
                            strt = audit_db.dirt_clean(tag.attrib['v'])
                            node['address'][sub_attr[1]] = audit_db.clean_streets(strt, mapping)

                
                        #******* if zipcode, audit as zipcode *******
                        elif sub_attr[1] == "postcode":
                            node['address'][sub_attr[1]] = audit_db.final_zipcode(tag.attrib['v'])

                    # All other single colons processed normally
                    else:
                        node[tag.attrib['k']] = tag.attrib['v']

                # Tags with no colon
                #******* if phone, audit as phone ******* 
                elif tag.attrib['k'] == "phone":
                    node["phone"] = audit_db.final_phone(tag.attrib['v'])

                elif tag.attrib['k'].find(':') == -1:
                    node[tag.attrib['k']] = tag.attrib['v']

            # Iterate 'nd'
            for nd in element.iter("nd"):
                if 'node_refs' not in node:
                    node['node_refs'] = []
                node['node_refs'].append(nd.attrib['ref'])
        
        return node
    else:
        return None


def json_convert(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = format_data(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def main():
    data = json_convert(filename, pretty=False)


if __name__ == '__main__':
    main()