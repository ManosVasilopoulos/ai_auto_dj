import xml.etree.ElementTree as ET
from .constants_dataset import xml_dir
from .xml_handler import vdj_xml_handler

def main():
    xml_name = 'virtual_dj_17_12.xml'
    tree = ET.parse(xml_dir + xml_name)
    vdj_database = tree.getroot()

    xml_handler = vdj_xml_handler()

    xml_handler.create_csv(vdj_database, xml_name)


if __name__ == '__main__':
    main()
