from requests import get
import xml.etree.ElementTree as et
from re import sub
from os import listdir, makedirs
from shutil import rmtree
from subprocess import call


class GraphBuilder:
    def __init__(self):
        self.href = 'https://repo1.maven.org/maven2/'
        self.lines = set()
        if 'cache' not in listdir('.'):
            makedirs('cache')

    @staticmethod
    def clear_cache():
        if 'cache' in listdir('.'):
            rmtree('cache')
        if 'cache' not in listdir('.'):
            makedirs('cache')

    def build_url(self, package: dict[str, str]):
        try:
            url = (f"{self.href}{'/'.join(package['group'].split('.'))}/"
                   f"{package['artifact']}/{package['version']}/"
                   f"{package['artifact']}-{package['version']}.pom")
        except KeyError:
            print('Неправильный словарь с параметрами пакета')
            return ''
        return url

    def load_xml(self, package: dict[str, str]):
        f_name = f"{package['artifact']}_{package['version']}.xml"

        if 'cache' not in listdir('.'):
            makedirs('cache')

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
                      self._build_graph(package) +
                      '\n\n@enduml')

        with open(code, 'wt') as file:
            file.write(graph_code)

        self.lines = set()

    def _build_graph(self, package: dict[str, str]):
        package['version'] = self.fix_version(package['version'])

        try:
            line = f"{package['artifact'].replace('.', '_')}: {package['version']}\n\n".replace('-', '_')
        except KeyError:
            print('Неправильный словарь с параметрами пакета')
            return ''

        graph_code = ''
        if line not in self.lines:
            graph_code = line
            self.lines.add(line)

        pom = self.load_xml(package)

        if not pom:
            return ''

        for dp in pom.findall('dependencies/dependency'):
            pkg = dict()

            optional = dp.find('optional')
            if optional is not None:
                if optional.text == 'true':
                    continue

            try:
                pkg['group'] = dp.find('groupId').text
                pkg['artifact'] = dp.find('artifactId').text
                pkg['version'] = dp.find('version').text
            except AttributeError:
                continue

            art_from = package['artifact'].replace('-', '_').replace('.', '_')
            art_to = pkg['artifact'].replace('-', '_').replace('.', '_')

            line = f"{art_from} -down-> {art_to}\n\n"
            if line not in self.lines:
                graph_code += line
                self.lines.add(line)

            graph_code += self._build_graph(pkg)

        return graph_code

    def fix_version(self, version):
        if '[' in version:
            version = version[1:version.find(',')]
        return version
    @staticmethod
    def draw_graph(code, p_uml):
        call(['java', '-jar', p_uml, code])
