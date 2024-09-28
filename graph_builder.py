from requests import get
import xml.etree.ElementTree as et
from re import sub
from os import listdir


class GraphBuilder:
    def __init__(self):
        self.href = 'https://repo1.maven.org/maven2/'
        self.start = True
        self.lines = set()

    def build_url(self, package: dict[str, str]):
        url = (f"{self.href}{'/'.join(package['group'].split('.'))}/"
               f"{package['artifact']}/{package['version']}/"
               f"{package['artifact']}-{package['version']}.pom")
        return url

    def load_xml(self, package: dict[str, str]):
        f_name = f"{package['artifact']}_{package['version']}.xml"

        if f_name not in listdir('cache'):
            url = self.build_url(package)
            package_pom = get(url)
            if package_pom.status_code == 200:
                with open(f'cache/{f_name}', 'wt') as file:
                    text = sub(' xmlns="[^"]+"', '', package_pom.text, count=1)
                    file.write(text)
            else:
                print('Не удалось открыть репозиторий пакета')
                return

        return et.parse(f'cache/{f_name}').getroot()

    def build_graph(self, code: str, package: dict[str, str]):
        graph_code = ('@startuml\n\n\n' +
                      self.__build_graph(package) +
                      '\n\n@enduml')
        with open(code, 'wt') as file:
            file.write(graph_code)

        self.lines = set()

    def __build_graph(self, package: dict[str, str]):
        pom = self.load_xml(package)
        line = f"{package['artifact']}: {package['version']}\n\n".replace('-', '_')
        graph_code = ''
        if line not in self.lines:
            graph_code = line
            self.lines.add(line)

        for dp in pom.findall('dependencies/dependency'):
            pkg = dict()

            optional = dp.find('optional')
            if optional is not None:
                if optional.text == 'true':
                    continue

            pkg['group'] = dp.find('groupId').text
            pkg['artifact'] = dp.find('artifactId').text
            pkg['version'] = dp.find('version').text

            art_from = package['artifact'].replace('-', '_')
            art_to = pkg['artifact'].replace('-', '_')

            line = f"{art_from} -down-> {art_to}\n\n"
            if line not in self.lines:
                graph_code += line
                self.lines.add(line)

            graph_code += self.__build_graph(pkg)

        return graph_code

    # def get_pom(self, href):
    #     xml = get(href)
    #     with open('temp.xml', 'wt') as file:
    #         text = sub(' xmlns="[^"]+"', '', xml.text, count=1)
    #         file.write(text)
    #
    #     root = et.parse('temp.xml').getroot()
    #     for dp in root.findall('dependencies/dependency'):
    #         group = dp.find('groupId').text
    #         artifact = dp.find('artifactId').text
    #         version = dp.find('version').text
