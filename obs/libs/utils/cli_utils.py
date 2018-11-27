from obs.libs.utils import prompt
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import npyscreen

def question(word):
    answer = False
    while answer not in ["y", "n"]:
        answer = input("{} [y/n]? ".format(word)).lower().strip()

    if answer == "y":
        answer = True
    else:
        answer = False
    return answer

def prompt_generator(form_title, fields):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(form_title)
    data = {}
    for field in fields:
        if field['type'] == 'TitleSelectOne':
            print('{} : '.format(field['name']))
            completer = WordCompleter(field['values'], ignore_case=True)
            for v in field['values']:
                print('- {}'.format(v))
            text = None

            while text not in field['values']:
                text = prompt('Enter your choice : ', completer=completer)

            data[field['key']] = text
        elif field['type'] == 'TitleSelect':
            print('{} : '.format(field['name']))
            completer = WordCompleter(field['values'], ignore_case=True)
            for v in field['values']:
                print('- {}'.format(v))
            data[field['key']] = prompt(
                'Enter your choice or create new : ', completer=completer)
        elif field['type'] == 'TitlePassword':
            data[field['key']] = prompt(
                '{} : '.format(field['name']), is_password=True)
        else:
            data[field['key']] = prompt('{} : '.format(field['name']))
        print('------------------------------')
    
    return data

def form_generator(form_title, fields):
    def myFunction(*args):
        form = npyscreen.Form(name=form_title)
        result = {}
        for field in fields:
            t = field["type"]
            k = field["key"]
            del field["type"]
            del field["key"]

            result[k] = form.add(getattr(npyscreen, t), **field)
        form.edit()
        return result

    return npyscreen.wrapper_basic(myFunction)