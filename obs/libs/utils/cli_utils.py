from obs.libs.utils import prompt
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import os
import codecs
import yaml
import npyscreen
import shutil
import git


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
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print(form_title)
    data = {}
    for field in fields:
        if field["type"] == "TitleSelectOne":
            print("{} : ".format(field["name"]))
            completer = WordCompleter(field["values"], ignore_case=True)
            for v in field["values"]:
                print("- {}".format(v))
            text = None

            while text not in field["values"]:
                text = prompt("Enter your choice : ", completer=completer)

            data[field["key"]] = text
        elif field["type"] == "TitleSelect":
            print("{} : ".format(field["name"]))
            completer = WordCompleter(field["values"], ignore_case=True)
            for v in field["values"]:
                print("- {}".format(v))
            data[field["key"]] = prompt(
                "Enter your choice or create new : ", completer=completer
            )
        elif field["type"] == "TitlePassword":
            data[field["key"]] = prompt("{} : ".format(field["name"]), is_password=True)
        else:
            data[field["key"]] = prompt("{} : ".format(field["name"]))
        print("------------------------------")

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


def get_key(manifest_file):
    try:
        manifest = {"stack": {"cloudian": [], "s3": []}}

        obs_templates = codecs.open(manifest_file, encoding="utf-8", errors="strict")
        manifest["data"] = yaml.load(obs_templates.read())
        manifest_data = eval(str(manifest["data"]))
        del manifest_data["deploy"]
        for (key, value) in manifest_data.items():
            manifest["stack"][key] = [i for i, v in value.items()]
        return manifest

    except Exception as e:
        raise


def initdir(manifest):
    active_catalog = list()
    for (k, v) in manifest["stack"].items():
        stack_key = manifest["stack"][k]
        if len(stack_key) > 0:
            mkdir("{}/{}".format(manifest["deploy_dir"], k))
            active_catalog.append(k)
    return active_catalog


def do_deploy_dir(manifest_file):
    try:
        manifest = {}
        manifest_dir = os.path.dirname(os.path.realpath(manifest_file))
        manifest["deploy_dir"] = "{}/.deploy".format(manifest_dir)

        if not os.path.isdir(manifest["deploy_dir"]):
            os.makedirs(manifest["deploy_dir"])

        key = get_key(manifest_file)
        manifest["stack"] = key["stack"]
        manifest["data"] = key["data"]

        return manifest

    except Exception as e:
        raise


def template_url(dest):
    mkdir(dest)
    return {"local": dest}


def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


def template_git(url, dir):
    try:
        chk_repo = os.path.isdir(dir)
        if chk_repo:
            shutil.rmtree(dir)

        git.Repo.clone_from(url, dir)
        # real_url = os.path.dirname(os.path.realpath(dir))

        return True

    except Exception as e:
        return False


def get_project(manifest_file):
    key = get_key(manifest_file)

    manifest = list()
    manifest += [cloudian for cloudian in key["stack"]["cloudian"]]
    manifest += [s3 for s3 in key["stack"]["s3"]]

    return manifest
