from sys import argv
from graph_builder import GraphBuilder
import xml.etree.ElementTree as et


def main(args):
    if len(args) < 2:
        print('Не указан путь к конфигурационному файлу')
        return

    config_path = args[1]
    try:
        root = et.parse(config_path).getroot()
    except FileNotFoundError:
        print('Не удаётся открыть конфигурационный файл')
        return

    package = dict()

    try:
        p_uml = root.find('PlantUml').text
        package['group'] = root.find('groupId').text
        package['artifact'] = root.find('artifactId').text
        package['version'] = root.find('version').text
        code = root.find('code').text
    except AttributeError:
        print('Неверные параметры конфигурации')
        return

    if len(args) > 2 and args[2] == '--clear-cache':
        GraphBuilder.clear_cache()

    builder = GraphBuilder()
    builder.build_graph(code, package)
    GraphBuilder.draw_graph(code, p_uml)


if __name__ == '__main__':
    main(argv)
