"""
in this module we will parse two kind of files that are too important for us
1) config file
    name of this config file is passed to us in controller with "-c" or "--config"
    this file contains:
        :param:str hesabies_path(required)  =>  absolute path to directory that contains hesabi files
        :param:list sources(required)       =>  a list of sources to read from with their details
        :param:list actions(required)       =>  a list of actions with their details
        :param:list pipe_type(required)     =>  a list with only one element, specifies the pipeline type to find out if actions should get triggered or not
2) hesabi files
each hesabi is a yaml file with contents of
"""
import os
from staticconf.loader import yaml_loader
import hesabi_verification


def load_config(config_path):
    if not os.path.isfile(config_path):
        return "No such file {}".format(config_path), False
    try:
        content = yaml_loader(config_path)
        return content, True
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
    if not hesabies_path:
        return "hesabies_path should have a value", False
    if not os.path.isdir(hesabies_path):
        return "No such directory {}".format(hesabies_path), False
    hesabi_bodies = dict()
    for hesabi_path in os.listdir(hesabies_path):
        try:
            tmp_content = load_hesabi_body(os.path.join(hesabies_path, hesabi_path))
            hesabi_bodies.update({hesabi_path: tmp_content})
        except:
            return "could not load hesabi {}".format(hesabi_path), False
    return hesabi_bodies, True


def verify_hesabi(hesabi_content, hesabi_path):
    instance_verify = hesabi_verification.Verify(hesabi_body=hesabi_content, hesabi_path=hesabi_path)
    return instance_verify.verifier()

