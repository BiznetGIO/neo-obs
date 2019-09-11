from obs.libs.utils import yaml_utils, cli_utils, vars_utils
from obs.libs.utils.lambdafunc import *


def get_stack():
    d_stack = yaml_utils.get_index(yaml_utils.repodata())
    f_stack = [
        {
            "type": "TitleSelectOne",
            "name": "Select Stack :",
            "key": "stack",
            "values": d_stack,
        }
    ]
    stack = cli_utils.form_generator("Stack list", f_stack)
    try:
        return d_stack[stack["stack"].value[0]]
    except:
        return None


def get_project(templates):
    d_template = yaml_utils.get_index(yaml_utils.repodata()[templates])
    f_template = [
        {
            "type": "TitleSelectOne",
            "name": "Select template :",
            "key": "template",
            "values": d_template,
        }
    ]
    template = cli_utils.form_generator("Templates", f_template)
    try:
        return d_template[template["template"].value[0]]
    except:
        return None


def setup_form(stack, project, parent=None):
    init = {
        "form": [{"type": "TitleText", "name": "User Id", "key": "userId"}],
        "depend": [],
        "number": [],
        "stack": stack,
        "project": project,
        "parent": parent,
    }

    if parent:
        init["parent"] = parent

    repo = yaml_utils.repodata()[stack][project]
    if yaml_utils.check_key(repo, "parameters"):
        param = repo["parameters"]
        param_index = yaml_utils.get_index(param)
        for index in param_index:
            prop = param[index]
            if not yaml_utils.check_key(prop, "default"):
                if not yaml_utils.check_key(prop, "dependences"):
                    init["form"].append(
                        {"type": "TitleText", "name": prop["label"], "key": index}
                    )
                    if prop["type"] == "number":
                        init["number"].append(index)
                else:
                    depend = prop["dependences"]
                    if depend.split(":")[0] == "func":
                        func_name = depend.split(":")[1]
                        init["form"].append(
                            {
                                "type": "TitleSelectOne",
                                "name": prop["label"],
                                "key": index,
                                "scroll_exit": True,
                                "values": globals()[func_name](),
                                "max_height": 7,
                                "value": [0],
                            }
                        )
                    if depend.split(":")[0] == "repo":
                        repo_name = depend.split(":")[1]
                        init["depend"].append(
                            {"name": prop["label"], "key": index, "repo": repo_name}
                        )
    return init


def exec_form(stack, project):
    form = {}
    f_init = list()
    parent_form = setup_form(stack, project)
    f_init.append(parent_form)
    form["init"] = list(reversed(f_init))
    return form


def dump(data):
    d_dump = {"deploy": []}
    d_depend = []
    for d_yml in data:
        pre_yml = {d_yml["userId"]: {"template": d_yml["template"]}}
        for k, v in d_yml.items():
            if k not in ["userId", "template", "stack", "parent"]:
                if not yaml_utils.check_key(pre_yml[d_yml["userId"]], "parameters"):
                    pre_yml[d_yml["userId"]]["parameters"] = {k: v}
                else:
                    pre_yml[d_yml["userId"]]["parameters"].update({k: v})

        if not yaml_utils.check_key(d_dump, d_yml["stack"]):
            d_dump[d_yml["stack"]] = pre_yml
        else:
            d_dump[d_yml["stack"]].update(pre_yml)

        if d_yml["parent"]:
            d_depend.append({"key": d_yml["parent"], "val": d_yml["userId"]})
        else:
            if len(d_depend) > 0:
                for k_depend in d_depend:
                    pre_yml[d_yml["userId"]]["parameters"].update(
                        {k_depend["key"]: k_depend["val"]}
                    )

        d_dump["deploy"].append("{}.{}".format(d_yml["stack"], d_yml["userId"]))
    return d_dump


def init(stack=None, project=None):
    select_stack = stack
    while not select_stack:
        select_stack = get_stack()

    select_project = project
    while not select_project:
        select_project = get_project(select_stack)

    fields = exec_form(select_stack, select_project)

    data = list()

    for field in fields["init"]:
        f_field = eval(str(field["form"]))
        validate = False
        while not validate:
            f_form = eval(str(field["form"]))
            form = cli_utils.form_generator("Setup {}".format(field["project"]), f_form)
            for k, v in form.items():
                if isinstance(v.value, list):
                    for role in f_field:
                        if role["key"] == k:
                            form[k] = role["values"][v.value[0]]
                else:
                    form[k] = v.value

            if field["parent"]:
                form["parent"] = field["parent"]
            else:
                form["parent"] = None
            form["stack"] = field["stack"]
            form["template"] = field["project"]
            """ Check if data is null """
            null_data = 0
            for k_data, v_data in form.items():
                if v_data == "":
                    null_data += 1
                if len(field["number"]) > 0:
                    if k_data in field["number"]:
                        if vars_utils.isint(v_data):
                            form[k_data] = int(v_data)
                        elif vars_utils.isfloat(v_data):
                            form[k_data] = float(v_data)
                        else:
                            null_data += 1

            if null_data == 0:
                validate = True
                data.append(form)

    yaml_utils.yaml_create("obs.yml", dump(data))
    return yaml_utils.read_file("obs.yml")
