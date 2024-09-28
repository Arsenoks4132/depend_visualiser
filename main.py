from sys import argv
from graph_builder import GraphBuilder
import xml.etree.ElementTree as et


def main():
    if len(argv) > 1:
        config_path = argv[1]
        try:
            root = et.parse(config_path).getroot()
            p_uml = root.find('PlantUml').text
            package = dict()
            package['group'] = root.find('group').text
            package['artifact'] = root.find('artifact').text
            package['version'] = root.find('version').text
            code = root.find('code').text
        except FileNotFoundError:
            print('Не удаётся открыть конфигурационный файл')
            return

        builder = GraphBuilder()
        builder.build_graph(code, package)

    else:
        print('Не указан путь к конфигурационному файлу')


if __name__ == '__main__':
    main()
