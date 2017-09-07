import xml.etree.cElementTree as ET
import pprint as pp
import re
from collections import defaultdict
"""""
Audits the zipcodes & gives correct zipcode output
"""""

## Raw Source File ##
# filename = "calcutta_subset.xml"
filename = "Calcutta.osm"

## All zipcodes in Calcutta are between 700001 & 700110 ###
zipcodes = [str(i) for i in range(700001,700110)]

## Regex Compiler ##
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
digit_only = re.compile(r'\d+')

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Sarani", "Park", "Connector", "Gardens"]

mapping = { "St": "Street", "St.": "Street", "street" : "Street", "Sarani" : "Sarani",
            "Ave" : "Avenue", "Rd." : "Road", "road" : "Road", "ROAD" : "Road", "ROad" : "Road",
            "Rd" : "Road", "N." : "North", "Ln" : "Lane" }

## ********** ZipCodes ********** ##

## returns if zip-code like ##
def is_zipcode(elem):
    return 'addr:postcode' in elem.attrib['k']


## Correct zipcode as output ##
def right_zipcode(code):    
    for z in zipcodes:
        if code in z:
            return z   

## adds any invalid zipcodes (not in format 'dddddd') to a dict ##
def audit_zipcode(bad_zipcodes, zipcode):
    if not re.match(r'^\d{6}$', zipcode):
        bad_zipcodes[zipcode] += 1

# ## Audit plus Edit Zipcodes ##
# def final_zipcode(final_zipcodes, zipcode):
#     if not re.match(r'^\d{6}$', zipcode):
#         z = right_zipcode(zipcode[-3:])
#         final_zipcodes[z] += 1
#     else:
#         final_zipcodes[zipcode] += 1

#     return final_zipcodes


## Audit plus Edit Zipcodes ##
def final_zipcode(zipcode):
    if not re.match(r'^\d{6}$', zipcode):
        z = right_zipcode(zipcode[-3:])
        return z
    else:
        return zipcode


## ********** Streets ********** ##

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            # print street_type

def dirt_clean(string):
    string = string.replace(",", "")
    string = string.strip(')')
    string = string.split(' ')
    string = string[:3]
    string = " ".join(string)
    return string

def clean_streets(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in expected:
            return name
            # clean_street[street_type].add(name)
        elif street_type not in expected:
            if street_type in mapping.keys():
                name = re.sub(street_type_re, mapping[street_type], name)
                return name
                # clean_street[mapping[street_type]].add(name)
            else:
                return name
                # clean_street["Others"].add(name)
    
    # return clean_streets


## ********** Phone Numbers ********** ##
def is_phone(elem):
    return 'phone' in elem.attrib['k']

def audit_phone(number_types, phone):
    if digit_only.match(phone):
        number_types['digit_only'] += 1
    else:
        number_types['other'] += 1
    return number_types

def right_phone(phone_number):
    return re.sub(r'[\D|\s]+', '', phone_number)[-10: ]

def final_phone(phone):
    if digit_only.match(phone):
        return phone
    else:
        d = right_phone(phone)
        return d

# def final_phone(final_phone, phone):
#     if digit_only.match(phone):
#         final_phone[phone] += 1
#     else:
#         d = right_phone(phone)
#         final_phone[d] += 1
#     return final_phone

##  ##
def audit(osmfile, limit=-1):
    
    # open osm file
    osm_file = open(osmfile, "r")

    # initialize dictionaries
    street_types = defaultdict(set)
    cln_strt = defaultdict(set)
    bad_zipcodes = defaultdict(int)
    final_zipcodes = defaultdict(int)
    bad_phone = defaultdict(int)
    final_phone_nums = defaultdict(int)
    audit_phone_nums = defaultdict(int)

    ## Parsing through elements
    for _, elem in ET.iterparse(osm_file, events=("start",)):
        # check if node or way type
        if elem.tag == "node" or elem.tag == "way":
            # iterate through `tag` children
            for tag in elem.iter("tag"):
                
                #*******if street name, audit as street*******
                if is_street_name(tag):
                    strt = dirt_clean(tag.attrib['v'])
                    audit_street_type(street_types, strt)
                    # clean_streets(cln_strt, strt, mapping)

                
                #******* if zipcode, audit as zipcode ******* 
                if is_zipcode(tag):
                    audit_zipcode(bad_zipcodes, tag.attrib['v'])
                    # final_zipcode(final_zipcodes, tag.attrib['v'])

                #******* if phone, audit as phone ******* 
                if is_phone(tag):
                    audit_phone(bad_phone, tag.attrib['v'])
                    # final_phone(final_phone_nums, tag.attrib['v'])


    # for i in final_phone_nums.keys():
        # audit_phone(audit_phone_nums, i)

    # return data
    print "Bad zipcodes: \n"
    pp.pprint(dict(bad_zipcodes))
    # print "\n"
    # print "Final corrected zipcodes of Calcutta: \n"
    # pp.pprint(dict(final_zipcodes))

    print "Bad Streets: \n"
    pp.pprint(dict(street_types))
    # print "\n"
    # print "Final Cleaned Streets of Calcutta: \n"
    # pp.pprint(dict(cln_strt))

    print "Bad Phone Numbers: \n"
    pp.pprint(dict(bad_phone))
    # print "\n"
    # print "Final corrected Phone Numbers of Calcutta: \n"
    # pp.pprint(dict(final_phone_nums))
    # print "Recheck: \n"
    # pp.pprint(dict(audit_phone_nums))

if __name__ == "__main__":
    audit(filename)