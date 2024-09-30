import pytest
from shutil import rmtree
from os import listdir, makedirs

from graph_builder import GraphBuilder
from main import main


@pytest.fixture
def builder():
    gb = GraphBuilder()
    return gb


@pytest.mark.parametrize(
    'args, expected', [
        ([], 'Не указан путь к конфигурационному файлу\n'),
        ([1], 'Не указан путь к конфигурационному файлу\n'),
        ([1, '2'], 'Не удаётся открыть конфигурационный файл\n'),
        ([0, 'cache/test.xml'], 'Неверные параметры конфигурации\n')
    ]
)
def test_main(builder, capfd, args, expected):
    with open('cache/test.xml', 'wt') as file:
        file.write('<abc></abc>')
    main(args)
    out, err = capfd.readouterr()
    assert out == expected


@pytest.mark.parametrize(
    'arg', [
        True,
        False
    ]
)
def test_init_1(arg):
    if ('cache' in listdir('.')) is arg:
        if arg:
            rmtree('cache')
        else:
            makedirs('cache')
    GraphBuilder()
    assert ('cache' in listdir('.'))


@pytest.mark.parametrize(
    'field, value', [
        ('href', 'https://repo1.maven.org/maven2/'),
        ('lines', set())
    ]
)
def test_init_2(builder, field, value):
    assert builder.__dict__[field] == value


@pytest.mark.parametrize(
    'arg, expected', [
        ({'group': 'test_group', 'artifact': 'test_artifact', 'version': '1.0.0'},
         'https://repo1.maven.org/maven2/test_group/test_artifact/1.0.0/test_artifact-1.0.0.pom'
         ),
        ({'group': 'test_group.grp', 'artifact': 'test_artifact', 'version': '1.0.0'},
         'https://repo1.maven.org/maven2/test_group/grp/test_artifact/1.0.0/test_artifact-1.0.0.pom'
         ),
        ({'group': 'test_gr', 'artifact': 'test_art', 'version': '1.2.0'},
         'https://repo1.maven.org/maven2/test_gr/test_art/1.2.0/test_art-1.2.0.pom'
         ),
        ({'grp': 'test'},
         'Неправильный словарь с параметрами пакета\n'
         )
    ]
)
def test_build_url(builder, arg, expected, capfd):
    if 'group' in arg:
        assert builder.build_url(arg) == expected
    else:
        builder.build_url(arg)
        out, err = capfd.readouterr()
        assert out == expected


@pytest.mark.parametrize(
    'arg, expected', [
        ({'group': 'io.micrometer', 'artifact': 'micrometer-observation', 'version': '1.12.5'},
         'https://github.com/micrometer-metrics/micrometer'
         ),
        ({'group': 'org.springframework', 'artifact': 'spring-core', 'version': '6.1.6'},
         'https://github.com/spring-projects/spring-framework'
         ),
        ({'group': 'org', 'artifact': 'spring', 'version': '6.1.6'},
         'Не удалось открыть репозиторий пакета\n'
         )
    ]
)
def test_load_xml(builder, arg, expected, capfd):
    xm = builder.load_xml(arg)
    if xm is not None:
        assert xm.find('url').text == expected
    else:
        out, err = capfd.readouterr()
        assert out == expected


@pytest.mark.parametrize(
    'code, package, expected', [
        ('PlantUml/graph.txt',
         {'group': 'org.springframework', 'artifact': 'spring-jcl', 'version': '6.1.6'},
         '''@startuml


spring_jcl: 6.1.6



@enduml'''
         ),
        ('PlantUml/graph.txt',
         {'group': 'org.springframework', 'artifact': 'spring-expression', 'version': '6.1.6'},
         '''@startuml


spring_expression: 6.1.6

spring_expression -down-> spring_core

spring_core: 6.1.6

spring_core -down-> spring_jcl

spring_jcl: 6.1.6



@enduml'''
         ),
        ('PlantUml/graph.txt',
         {'group': 'org', 'artifact': 'spring', 'version': '123'},
         '@startuml\n\n\n\n\n@enduml'
         )
    ]
)
def test_build_graph(builder, code, package, expected):
    builder.build_graph(code, package)
    with open(code, 'rt') as file:
        assert file.read() == expected


@pytest.mark.parametrize(
    'package, expected', [
        ({'group': 'org.springframework', 'artifact': 'spring-jcl', 'version': '6.1.6'},
         '''spring_jcl: 6.1.6\n\n'''
         ),
        ({'group': 'org.springframework', 'artifact': 'spring-expression', 'version': '6.1.6'},
         '''spring_expression: 6.1.6

spring_expression -down-> spring_core

spring_core: 6.1.6

spring_core -down-> spring_jcl

spring_jcl: 6.1.6

'''
         ),
        ({'group': 'org', 'artifact': 'spring', 'version': '123'},
         ''
         )
    ]
)
def test_build_graph_pr(builder, package, expected):
    assert builder._build_graph(package) == expected


@pytest.mark.parametrize(
    'code, p_uml', [
        ('PlantUml/graph.txt', 'PlantUml/plantuml-1.2024.7.jar'),
        ('PlantUml/graph_2.txt', 'PlantUml/plantuml-1.2024.7.jar')
    ]
)
def test_draw_graph(code, p_uml):
    GraphBuilder.draw_graph(code, p_uml)
    if code[code.find('/') + 1:] in listdir('PlantUml'):
        assert code[code.find('/') + 1:].replace('.txt', '.png') in listdir('PlantUml')
    else:
        assert True
