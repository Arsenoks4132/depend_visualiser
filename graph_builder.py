from requests import get
import xml.etree.ElementTree as ET
from re import sub

class GraphBuilder:
    def __init__(self):
        pass

    def build_graph(self, group, artifact, version):
        pass



    def get_pom(self, href):
        xml = get(href)
        with open('temp.xml', 'wt') as file:
            text = xml.text
            text = sub(' xmlns="[^"]+"', '', text, count=1)
            file.write(text)

        root = ET.parse('temp.xml').getroot()
        for dp in root.findall('dependencies/dependency'):
            group = dp.find('groupId').text
            artifact = dp.find('artifactId').text
            version = dp.find('version').text
            print(group, artifact, version)