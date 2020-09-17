import os
from staticconf.loaders import yaml_loader


def load_config(config_path):
    if os.path.isfile(config_path):
        return "No such file {}".format(config_path), False
    try:
        content = yaml_loader(config_path)
        return content
    except:
        return "Could not load file {}".format(config_path), False


def load_hesabi_body(hesabi_path):
    if not os.path.isfile(hesabi_path):
        return "No such file {}".format(hesabi_path), False
    try:
        return yaml_loader(hesabi_path)
    except:
        return "Could not load file {}".format(hesabi_path), False


def load_hesabi_bodies(hesabies_path):
    if not os.path.isdir(hesabies_path):
        return "No such directory {}".format(hesabies_path), False
    hesabi_bodies = dict()
    for hesabi_path in os.listdir(hesabies_path):
        try:
            tmp_content = load_hesabi_body(os.path.join(hesabies_path, hesabi_path))
            hesabi_bodies.update({hesabi_path: tmp_content})
        except:
            print("could not load hesabi {}".format(hesabi_path))
    return hesabi_bodies, True
