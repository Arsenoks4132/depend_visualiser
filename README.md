# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```bash
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Виртуальное окружение

```shell
python -m venv venv
venv\Scripts\activate
```

# 3. Установка зависимостей

```shell
pip install -r requirements.txt
```

# 4. Запуск программы

```shell
py main.py
```

# 5. Тестирование

Для запуска тестирования необходимо запустить следующий скрипт:

```shell
pytest -v
```

Для генерации отчета о покрытии тестами необходимо выполнить команду:

```shell
coverage run --branch -m pytest test_builder.py
```

Просмотр результатов покрытия:

```shell
coverage report
```

# Конфигурационный файл

Пример конфигурационного файла:

```xml
<config>
    <PlantUml>PlantUml/plantuml-1.2024.7.jar</PlantUml>
    <code>PlantUml/graph.txt</code>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>6.1.6</version>
</config>
```

Где:

- **PlantUml** - Путь к программе отрисовки графа
- **code** - Путь к файлу-результату в виде кода
- **groupId**, **artifactId**, **version** - Характеристики пакета с сайта [Maven](https://mvnrepository.com/)

# Примеры работы

![image](https://github.com/user-attachments/assets/f2faea32-1d58-4dd0-b259-9aeca9f2f72c)

![image](https://github.com/user-attachments/assets/ebeb1bb7-4919-416b-9a2b-2b4b5fc059a1)

# Тесты

Результаты покрытия тестами:

![image](https://github.com/user-attachments/assets/7ae88fce-ed04-4512-a6e3-c13ea7485c45)
