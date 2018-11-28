from obs.clis.base import Base
from obs.libs.utils import orchestration, log_utils, cli_utils, prompt, ncurses, yaml_utils
from tabulate import tabulate

import os

class Create(Base):
    '''
    Usage:
        create [-i] [-f PATH]
        create [-t TEMPLATE] [-i]
        create user

    Options:
        -h --help                           Print usage
        -f PATH --file=PATH                 Set neo-obs manifest file
        -t TEMPLATE --template TEMPLATE     Create obs.yml, TEMPLATE is ENUM(user)
        -i --interactive                    Interactive form with ncurses mode

    Commands:
        user

    Tips!
        obs create -t user         create cloudian user
    
    Run 'obs create COMMAND --help' for more information on a command.
    '''

    def execute(self):
        set_file = self.args["--file"]
        default_file = orchestration.check_manifest_file()

        if set_file:
            if os.path.exists(set_file):
                default_file = set_file
            else:
                log_utils.log_err("{} file is not exists!".format(set_file))
                exit()

        if not default_file:
            log_utils.log_err("Can't find obs.yml manifest file!")
            q_stack = cli_utils.question(
                "Do you want to generate obs.yml manifest? ")

            if q_stack:
                if self.args["--interactive"]:
                    print(ncurses.init())
                else:
                    print(prompt.init())

                q_deploy = cli_utils.question("Continue to deploy? ")
                if q_deploy:
                    default_file = "obs.yml"
                else:
                    exit()
            else:
                exit()
        else:
            q_deploy = cli_utils.question("Continue to deploy? ")
            if q_deploy:
                default_file = "obs.yml"
            else:
                exit()

        deploy_init = yaml_utils.file_parser(default_file)
        try:
            orchestration.do_create(deploy_init)
        except Exception as e:
            log_utils.log_err("Deploying Stack failed...")
            exit()

        stack = list(deploy_init.keys())[0]
        stack_name = list(deploy_init[stack])[0]
        parameters = deploy_init[stack][stack_name]['parameters']
        project_list = list()
        data = {}
        for key in parameters:
            data[key] = parameters[key]

        project_list.append(data)
            
        if len(project_list) > 0:
            print(tabulate(project_list, headers='keys', tablefmt="grid"))