"""
Actions classes are defined in this module. so there is a specific format to use to add other actions if feature
each class has at least five functions. theses functions are accessed from "Controller" module to
get called independent of action type.these functions are:
    1) __init__
        this function initializes the instance of action.
        :param *args: so accepts a dictionary and this dictionary is accessible in a set data type
    2) action_checkup
        a simple checkup for rule to make sure all required options are provided
        :returns (str, state): if state is False, it means there was an error, so the error content is the returned string.
                               this helps users to find out the exact point of fail and what can they do to fix it.
    3) run_action
        this function runs after checking actions up. used to run the action with given options
    4) write_results
        this function writes the action's options and result into elasticsearch so we will findout if an email could not be sent and we can try to send it later
    5) action_history
        :param start_timestamp
        :param size default 10
        this function shows the history of actions we ran. if "start_timestamp" is not set, will start from index creation time and fetch them
"""

import os
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager


def lost_file_finder(files, exist_only=True, file_only=False):
    lost_files = list()
    for file in files:
        if file_only:
            if not os.path.isfile(file):
                lost_files.append(file)
        elif exist_only:
            if not os.path.exists(file):
                lost_files.append(file)
    return lost_files


def find_inventories_group_hosts(inventory, group):
    try:
        data_loader = DataLoader()
        inventory = InventoryManager(loader=data_loader, sources=[inventory])
        return inventory.get_groups_dict()[group], True
    except KeyError:
        return [], False


class Ansible:
    def __init__(self, *args):
        valid = True if (args and len(args) and isinstance(args[0], dict)) else False
        tmp_args = args[0] if valid else {}
        self.method = tmp_args.get("method")
        self.adhoc_command = tmp_args.get("adhoc_command")
        self.inventory = tmp_args.get("inventory")
        self.group = tmp_args.get("group")
        self.playbooks = tmp_args.get("playbooks")

    def action_checkup(self):
        if self.method == "ad_hoc":
            """
                field "group" is optional so we only check the type if it is defined
                field "inventory" is optional so we only check the type if it is defined
                field "adhoc_command" is required so we make sure it is defined and is of type string
            """
            if self.inventory:
                if not isinstance(self.inventory, str):
                    return "Inventory should be of type string.", False
                if not os.path.isfile(self.inventory):
                    return "No Such file or directory {}.".format(self.inventory), False

            if self.group:
                if not isinstance(self.group, str):
                    return "Group should be of type string.", False
                hosts, state = find_inventories_group_hosts(self.inventory if self.inventory else "/etc/ansible/hosts", group=self.group)
                if not state:
                    return "Group \"{}\" is not valid".format(self.group), False

            if self.adhoc_command:
                if not isinstance(self.adhoc_command, str):
                    return "Field \"adhoc_command\" is of type string.", False
            else:
                return "Field \"adhoc_command\" is required.", False
            return "", True
        elif self.method == "playbook":
            if self.playbooks:
                if not isinstance(self.playbooks, list):
                    return "playbooks should be of type list.", False
                missing_playbooks = lost_file_finder(self.playbooks)
                if missing_playbooks:
                    return "Missing Playbooks Files Are :\n"+"\n".join(missing_playbooks), False
            else:
                return "Field \"playbooks\" is required.", False
            return "", True
        else:
            return "method should be one of [\"ad_hoc\", \"playbook\"]", False

    def run_action(self):
        if self.method == "ad_hoc":
            self.ad_hoc_action()
        elif self.method == "playbook":
            self.playbook_action()

    def write_results(self):
        pass

    def action_history(self):
        pass

    def ad_hoc_action(self):
        string_template = ""
        if self.group:
            string_template += "{} ".format(self.group)

        if self.inventory:
            string_template += "-i {}".format(self.inventory)

    def playbook_action(self):
        for playbook in self.playbooks:
            print("Executing Playbook {}".format(playbook))
            result = os.system("ansible-playbook {}".format(playbook))
            print("Exited with errors") if result else print("Finished Successfully")


class Email:
    def __init__(self, emails):
        self.emails = emails

    def action_checkup(self):
        pass

    def run_action(self):
        pass

    def write_results(self):
        pass

    def action_history(self):
        pass


class Command:
    def __init__(self, command):
        self.command = command

    def action_checkup(self):
        pass

    def run_action(self):
        pass

    def write_results(self):
        pass

    def action_history(self):
        pass

