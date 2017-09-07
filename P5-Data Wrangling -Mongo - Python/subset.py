
from pprint import pprint
import xml.etree.ElementTree as ET

in_file = 'Calcutta.osm'
out_file = 'calcutta_subset.xml'


def main(file_in, file_out):

    root = ET.Element('osm')

    for _, elem in ET.iterparse(file_in, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            tag_type = elem.tag
            if len([child.tag for child in elem.iter("tag")]) >= 2:
                print '.'
                node = ET.SubElement(root, tag_type, attrib=elem.attrib)
                for tag in elem.iter("tag"):
                    child = ET.SubElement(node, 'tag', attrib=tag.attrib)

    tree = ET.ElementTree(root)
    tree.write(file_out)

if __name__ == '__main__':
    main(in_file, out_file)