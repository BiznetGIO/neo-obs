from obs.libs.utils import yaml_utils

import yaml, os


def check_extension(file):
    filename, file_extension = os.path.splitext(file)
    if file_extension == '.obs':
        return True
    elif file_extension == '':
        raise Exception("Ingat Ganteng Extension File "+filename+" Harus Ada")
    else:
        raise Exception("Nda Bisa Ganteng Extension File Harus .ocha")


def file_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data

        except yaml.YAMLError as exc:
            print(exc)


def repodata():
    abs_path = os.path.dirname(os.path.realpath(__file__))
    repo_file = "{}/templates/repo.yml".format(abs_path)
    return yaml_parser(repo_file)


def get_index(dictionary):
    return [key for (key, value) in dictionary.items()]


def check_key(dict, val):
    try:
        if dict[val]:
            return True
    except Exception as e:
        return False


def yaml_create(out_file, data):
    with open(out_file, 'w') as outfile:
        try:
            yaml.dump(data, outfile, default_flow_style=False)
            return True

        except yaml.YAMLError as exc:
            print(exc)


def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()