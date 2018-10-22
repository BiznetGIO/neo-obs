import coloredlogs
import logging
import getpass

def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)

def question(word):
    answer = False
    while answer not in ["y", "n"]:
        answer = input("{} [y/n]? ".format(word)).lower().strip()

    if answer == "y":
        answer = True
    else:
        answer = False
    return answer


def get_log(title=None):
    return input(title)


def get_pass(title=None):
    return getpass.getpass(title)
