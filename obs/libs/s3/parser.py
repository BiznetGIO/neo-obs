import yaml


def get_resource(json_data=''):
    keys = ''
    for i in json_data:
        keys = i
    return keys


def get_method(json_data=''):
    resource = get_resource(json_data)
    keys = ''
    for i in json_data[resource]:
        keys = i
    return keys


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def parser(json_data='', static_dir=''):
    resource = get_resource(json_data)
    method = get_method(json_data)
    parameters_key = json_data[resource][method]['parameters']
    template = static_dir + '/template.yml'

    load_template = yaml_parser(template)
    template_project = load_template[resource][method]['parameters']
    parameters_project = dict(template_project)

    data = {}
    for i in parameters_project:
        data_index = load_template[resource][method]['parameters'][i]
        data[i] = data_index

    for a in parameters_project:
        if data[a]['default']:
            parameters_key[a] = data[a]['default']

    parameters = {}
    for i in parameters_project:
        parameters[i] = parameters_key[i]
    return parameters
