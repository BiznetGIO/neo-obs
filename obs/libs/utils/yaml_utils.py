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