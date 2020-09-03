import xml.etree.ElementTree as ET
from .constants_dataset import xml_dir
from .xml_handler import rekordbox_xml_handler


def main():
    xml_name = 'rekordbox_27_3.xml'
    tree = ET.parse(xml_dir + xml_name)
    dj_playlists = tree.getroot()

    xml_handler = rekordbox_xml_handler()
    xml_handler.create_csv(dj_playlists, xml_name)


if __name__ == '__main__':
    main()
