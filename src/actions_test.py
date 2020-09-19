"""
this module belongs to actions module unittests
here i try to test 4 conditions on fields:
    if a key is not defined at all                  ->  _none
    if a key is defined but has empty value         ->  _empty
    if a key is defined but has some errors         ->  _err
    if a key is defined and is ok                   ->  _ok
and also a test for missing files specified with    ->  _missing
"""

import unittest
import actions


class MyTestCase(unittest.TestCase):
    def test_ansible_checkup(self):
        instance_method_none = actions.Ansible("name", "body", {"adhoc_command": "test", "inventory": "test", "group": "test"}, [("test", "test2"), ])
        instance_method_empty = actions.Ansible("name", "body", {"method": "", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_method_err = actions.Ansible("name", "body", {"method": "test", "adhoc_command": "-m ping", "inventory": "/etc/ansible/hosts", "group": "servers", "playbooks": ""}, [("test", "test2"), ])
        instance_method_ok = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""}, [("test", "test2"), ])

        self.assertTupleEqual(instance_method_none.action_checkup(), ("method should be one of [\"ad_hoc\", \"playbook\"]", False))
        self.assertTupleEqual(instance_method_empty.action_checkup(), ("method should be one of [\"ad_hoc\", \"playbook\"]", False))
        self.assertTupleEqual(instance_method_err.action_checkup(), ("method should be one of [\"ad_hoc\", \"playbook\"]", False))
        answer, state = instance_method_ok.action_checkup()
        self.assertTupleEqual((answer, state), ("", True))

        instance_adhoc_command_none = actions.Ansible("name", "body", {"method": "ad_hoc", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""}, [("test", "test2"), ])
        instance_adhoc_command_empty = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""}, [("test", "test2"), ])
        instance_adhoc_command_err = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": ["test1", "test2"], "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""}, [("test", "test2"), ])
        instance_adhoc_command_ok = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""}, [("test", "test2"), ])

        self.assertTupleEqual(instance_adhoc_command_none.action_checkup(), ("Field \"adhoc_command\" is required.", False))
        self.assertTupleEqual(instance_adhoc_command_empty.action_checkup(), ("Field \"adhoc_command\" is required.", False))
        self.assertTupleEqual(instance_adhoc_command_err.action_checkup(), ("Field \"adhoc_command\" is of type string.", False))
        answer, state = instance_adhoc_command_ok.action_checkup()
        self.assertTupleEqual((answer, state), ("", True))

        instance_playbooks_none = actions.Ansible("name", "body", {"method": "playbook", "adhoc_command": "", "inventory": "", "group": ""}, [("test", "test2"), ])
        instance_playbooks_empty = actions.Ansible("name", "body", {"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_playbooks_err = actions.Ansible("name", "body", {"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": "test"}, [("test", "test2"), ])
        instance_playbooks_missing = actions.Ansible("name", "body", {"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ["/file/not/found", "/test/test2"]}, [("test", "test2"), ])
        instance_playbooks_ok = actions.Ansible("name", "body", {"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ["/home/navid/PycharmProjects/has/playbooks/pb1.yaml"]}, [("test", "test2"), ])

        self.assertTupleEqual(instance_playbooks_none.action_checkup(), ("Field \"playbooks\" is required.", False))
        self.assertTupleEqual(instance_playbooks_empty.action_checkup(), ("Field \"playbooks\" is required.", False))
        self.assertTupleEqual(instance_playbooks_err.action_checkup(), ("playbooks should be of type list.", False))
        self.assertTupleEqual(instance_playbooks_missing.action_checkup(), ("Missing Playbooks Files Are :\n/file/not/found\n/test/test2", False))
        answer, state = instance_playbooks_ok.action_checkup()
        self.assertTupleEqual((answer, state), ("", True))

        instance_inventory_none = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_inventory_empty = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_inventory_err = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": ["test"], "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_inventory_missing = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/file/not/found", "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_inventory_ok = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/home/navid/PycharmProjects/has/inventory", "group": "", "playbooks": ""}, [("test", "test2"), ])

        self.assertTupleEqual(instance_inventory_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_inventory_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_inventory_err.action_checkup(), ("Inventory should be of type string.", False))
        self.assertTupleEqual(instance_inventory_missing.action_checkup(), ("No Such file or directory /file/not/found.", False))
        self.assertTupleEqual(instance_inventory_ok.action_checkup(), ("", True))

        instance_group_none = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "playbooks": ""}, [("test", "test2"), ])
        instance_group_empty = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "", "playbooks": ""}, [("test", "test2"), ])
        instance_group_err = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": ["test"], "playbooks": ""}, [("test", "test2"), ])
        instance_group_missing = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "cloud", "playbooks": ""}, [("test", "test2"), ])
        instance_group_ok = actions.Ansible("name", "body", {"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "all", "playbooks": ""}, [("test", "test2"), ])

        self.assertTupleEqual(instance_group_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_group_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_group_err.action_checkup(), ("Group should be of type string.", False))
        self.assertTupleEqual(instance_group_missing.action_checkup(), ("Group \"cloud\" is not valid", False))
        self.assertTupleEqual(instance_group_ok.action_checkup(), ("", True))

    def test_email_checkup(self):
        instance_from_addr_none = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": ""}, [("test", "test2"), ])
        instance_from_addr_empty = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": ""}, [("test", "test2"), ])
        instance_from_addr_err = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": ["test"]}, [("test", "test2"), ])
        instance_from_addr_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_from_addr_none.action_checkup(), ("Error on field \"from_addr\" => value \"None\" not acceptable.", False))
        self.assertTupleEqual(instance_from_addr_empty.action_checkup(), ("Error on field \"from_addr\" => value \"\" not acceptable.", False))
        self.assertTupleEqual(instance_from_addr_err.action_checkup(), ("Error on field \"from_addr\" => value \"[\'test\']\" not acceptable.", False))
        self.assertTupleEqual(instance_from_addr_ok.action_checkup(), ("", True))

        instance_to_addr_none = actions.Email("name", "body", {"smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_to_addr_empty = actions.Email("name", "body", {"to_addr": "", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_to_addr_err = actions.Email("name", "body", {"to_addr": ["test@gmail.com"], "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_to_addr_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_to_addr_none.action_checkup(), ("Error on field \"to_addr\" => value \"None\" not acceptable.", False))
        self.assertTupleEqual(instance_to_addr_empty.action_checkup(), ("Error on field \"to_addr\" => value \"\" not acceptable.", False))
        self.assertTupleEqual(instance_to_addr_err.action_checkup(), ("Error on field \"to_addr\" => value \"[\'test@gmail.com\']\" not acceptable.", False))
        self.assertTupleEqual(instance_to_addr_ok.action_checkup(), ("", True))

        instance_smtp_host_none = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_smtp_host_empty = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_smtp_host_err = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": ["127.0.0.1"], "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_smtp_host_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_smtp_host_none.action_checkup(), ("Error on field \"smtp_host\" => value \"None\" not acceptable.", False))
        self.assertTupleEqual(instance_smtp_host_empty.action_checkup(), ("Error on field \"smtp_host\" => value \"\" not acceptable.", False))
        self.assertTupleEqual(instance_smtp_host_err.action_checkup(), ("Error on field \"smtp_host\" => value \"[\'127.0.0.1\']\" not acceptable.", False))
        self.assertTupleEqual(instance_smtp_host_ok.action_checkup(), ("", True))

        instance_smtp_port_none = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_smtp_port_empty = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_smtp_port_err = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": ["25"], "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_smtp_port_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_smtp_port_none.action_checkup(), ("Error on field \"smtp_port\" => value \"None\" not acceptable.", False))
        self.assertTupleEqual(instance_smtp_port_empty.action_checkup(), ("Error on field \"smtp_port\" => value \"\" not acceptable.", False))
        self.assertTupleEqual(instance_smtp_port_err.action_checkup(), ("Error on field \"smtp_port\" => value \"[\'25\']\" not acceptable.", False))
        self.assertTupleEqual(instance_smtp_port_ok.action_checkup(), ("", True))

        instance_use_ssl_none = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_use_ssl_empty = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_use_ssl_err = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "test", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_use_ssl_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "true", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_use_ssl_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_use_ssl_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_use_ssl_err.action_checkup(), ("Error on field \"use_ssl\" => value \"test\" not acceptable.", False))
        self.assertTupleEqual(instance_use_ssl_ok.action_checkup(), ("", True))

        instance_password_none = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_password_empty = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_password_err = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": ["password"], "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_password_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_password_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_password_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_password_err.action_checkup(), ("Error on field \"password\" => value \"[\'password\']\" not acceptable.", False))
        self.assertTupleEqual(instance_password_ok.action_checkup(), ("", True))

        instance_username_none = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_username_empty = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_username_err = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": ["username"], "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])
        instance_username_ok = actions.Email("name", "body", {"to_addr": "test@gmail.com", "smtp_host": "127.0.0.1", "smtp_port": "25", "use_ssl": "", "username": "", "password": "", "from_addr": "from@gmail.com"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_username_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_username_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_username_err.action_checkup(), ("Error on field \"username\" => value \"[\'username\']\" not acceptable.", False))
        self.assertTupleEqual(instance_username_ok.action_checkup(), ("", True))

    def test_command_checkup(self):
        instance_command_none = actions.Command("name", "body", {}, [("test", "test2"), ])
        instance_command_empty = actions.Command("name", "body", {"command": ""}, [("test", "test2"), ])
        instance_command_err = actions.Command("name", "body", {"command": ["test"]}, [("test", "test2"), ])
        instance_command_ok = actions.Command("name", "body", {"command": "ls"}, [("test", "test2"), ])

        self.assertTupleEqual(instance_command_none.action_checkup(), ("field \"command\" should be of type str.", False))
        self.assertTupleEqual(instance_command_empty.action_checkup(), ("field \"command\" should not be empty.", False))
        self.assertTupleEqual(instance_command_err.action_checkup(), ("field \"command\" should be of type str.", False))
        self.assertTupleEqual(instance_command_ok.action_checkup(), ("", True))


if __name__ == '__main__':
    unittest.main()
