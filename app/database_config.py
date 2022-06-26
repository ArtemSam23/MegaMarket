# Файл доя конфигурации базы данных

from configparser import ConfigParser


def config(filename='app/database.ini', section='postgresql'):
    # создаем parser
    parser = ConfigParser()
    # файл конфигурации должен быть в директории app
    parser.read(filename)

    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} is not found in {filename} file.')
    return db_config


if __name__ == '__main__':
    print("postgresql://{user}:{password}@{host}/{database}".format(**config(filename="database.ini")))
