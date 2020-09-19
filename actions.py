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
        :param start_unix_time
        :param end_unix_time
        :param action_completed
        :param description
        first two parameters are used to find out how long did the action take.the result is added to action body as field "took"
        parameter "action_completed" is used to trace actions later and for Non-repudiation
        parameter "description" is used for later understanding of the reason on done actions
    5) action_history
        :param start_timestamp
        :param size default 10
        this function shows the history of actions we ran. if "start_timestamp" is not set, will start from index creation time and fetch them
"""

import os
import datetime
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import *
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from socket import error


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
    action_required_options = frozenset([])

    def __init__(self, aggr_values=None, *args):
        valid = True if (args and len(args) and isinstance(args[0], dict)) else False
        tmp_args = args[0] if valid else {}
        self.method = tmp_args.get("method")
        self.adhoc_command = tmp_args.get("adhoc_command")
        self.inventory = tmp_args.get("inventory")
        self.group = tmp_args.get("group")
        self.playbooks = tmp_args.get("playbooks")
        self.replace_args_in_template = tmp_args.get("replace_args_in_template") if tmp_args.get("replace_args_in_template") else False
        self.replace_variable = tmp_args.get("replace_variable")
        self.aggr_values = aggr_values

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

    def write_results(self, start_unix_time, end_unix_time, action_completed, description):
        if self.method == "ad_hoc":
            body = {"type": "ansible",
                    "method": self.method,
                    "command": self.adhoc_command,
                    "group": self.group,
                    "inventory": self.inventory,
                    "@timestamp": datetime.datetime.utcnow().isoformat(),
                    "action_completed": action_completed,
                    "description": description,
                    "took": end_unix_time - start_unix_time}
        elif self.method == "playbook":
            body = {"type": "ansible",
                    "method": self.method,
                    "playbooks": self.playbooks,
                    "@timestamp": datetime.datetime.utcnow().isoformat(),
                    "action_completed": action_completed,
                    "description": description,
                    "took": end_unix_time - start_unix_time}

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
    action_required_options = frozenset(["smtp_host", "smtp_port", "from_addr", "to_addr", "title"])

    def __init__(self, *args):
        valid = True if (args and len(args) and isinstance(args[0], dict)) else False
        tmp_args = args[0] if valid else {}
        self.to_addr = tmp_args.get("to_addr")
        self.host = tmp_args.get("smtp_host")
        self.port = tmp_args.get("smtp_port")
        self.use_ssl = tmp_args.get("use_ssl")
        self.username = tmp_args.get("username")
        self.password = tmp_args.get("password")
        self.from_addr = tmp_args.get("from_addr")
        self.title = tmp_args.get("title")
        self.cert_file = tmp_args.get("cert_file")
        self.key_file = tmp_args.get("key_file")

    def action_checkup(self):
        """
        required options are [smtp_host, smtp_port, from_addr, to_addr]
        :return err_content, err_free
        """
        results = dict({"valid_username": True, "valid_password": True, "valid_use_ssl": True})
        results.update({"valid_smtp_host": True if (self.host and isinstance(self.host, str)) else False})
        results.update({"valid_smtp_port": True if (self.port and str(self.port).isnumeric()) else False})
        results.update({"valid_from_addr": True if (self.from_addr and isinstance(self.from_addr, str)) else False})
        results.update({"valid_to_addr": True if (self.to_addr and isinstance(self.to_addr, str)) else False})
        if self.use_ssl:
            results.update({"valid_use_ssl": True if (self.use_ssl and str(self.use_ssl).lower() in ["true", "false"]) else False})
        if self.cert_file:
            results.update({"valid_cert_file": True if (self.cert_file and os.path.isfile(self.cert_file)) else False})

        if self.key_file:
            results.update({"valid_key_file": True if (self.key_file and os.path.isfile(self.key_file)) else False})

        if self.username:
            results.update({"valid_username": True if isinstance(self.username, str) else False})
        if self.password:
            results.update({"valid_password": True if isinstance(self.password, str) else False})
        if self.title:
            results.update({"valid_title": True if isinstance(self.title, str) else False})

        mapping = {
            "valid_smtp_host": self.host,
            "valid_smtp_port": self.port,
            "valid_use_ssl": self.use_ssl,
            "valid_username": self.username,
            "valid_password": self.password,
            "valid_from_addr": self.from_addr,
            "valid_to_addr": self.to_addr,
            "valid_title": self.title,
            "valid_key_file": self.key_file,
            "valid_cert_file": self.cert_file
        }
        for key in results:
            if not results[key]:
                return "Error on field \"{}\" => value \"{}\" not acceptable.".format(key[6:], mapping.get(key)), False
        return "", True

    def run_action(self):
        body = "HESABI TRIGGER"
        email_msg = MIMEText(body, _charset='UTF-8')
        email_msg['Subject'] = self.title
        email_msg['To'] = self.to_addr
        email_msg['From'] = self.from_addr
        email_msg['Date'] = formatdate()
        try:
            if self.use_ssl:
                if self.port:
                    self.smtp = SMTP_SSL(self.host, self.port, keyfile=self.key_file, certfile=self.cert_file)
                else:
                    self.smtp = SMTP_SSL(self.host, keyfile=self.key_file, certfile=self.cert_file)
            else:
                if self.port:
                    self.smtp = SMTP(self.host, self.port)
                else:
                    self.smtp = SMTP(self.host)
                self.smtp.ehlo()
                if self.smtp.has_extn('STARTTLS'):
                    self.smtp.starttls(keyfile=self.key_file, certfile=self.cert_file)
            if self.username and self.password:
                self.smtp.login(self.username, self.password)
        except (SMTPException, error) as e:
            return "Error connecting to SMTP host: {}".format(e), False
        except SMTPAuthenticationError as e:
            return "SMTP username/password rejected: {}".format(e), False
        self.smtp.sendmail(self.from_addr, self.to_addr, email_msg.as_string())
        self.smtp.quit()
        return "", True

    def write_results(self, start_unix_time, end_unix_time, action_completed, description):
        body = {"type": "email",
                "from_email": self.from_addr,
                "dest_email": self.to_addr,
                "smtp server": self.host+":"+self.port,
                "@timestamp": datetime.datetime.utcnow().isoformat(),
                "action_completed": action_completed,
                "description": description,
                "took": end_unix_time - start_unix_time}

    def action_history(self):
        pass


class Command:
    action_required_options = frozenset(["command"])

    def __init__(self, *args):
        valid = True if (args and len(args) and isinstance(args[0], dict)) else False
        tmp_args = args[0] if valid else {}
        self.command = tmp_args.get("command")

    def action_checkup(self):
        if not isinstance(self.command, list):
            return "field \"command\" should be of type list.", False
        return "", True

    def run_action(self):
        status = os.system(command=self.command)
        message = "Problems while running command \"{}\"".format(self.command) if status else ""
        return message, status

    def write_results(self, start_unix_time, end_unix_time, action_completed, description):
        body = {"type": "command",
                "command": self.command,
                "@timestamp": datetime.datetime.utcnow().isoformat(),
                "action_completed": action_completed,
                "description": description,
                "took": end_unix_time - start_unix_time}

    def action_history(self):
        pass


class Debug:
    action_required_options = frozenset([])

    def __init__(self):
        self.debug = True

    def action_checkup(self):
        return "", True

    def run_action(self):
        return "", True

    def write_results(self):
        pass

    def action_history(self):
        pass