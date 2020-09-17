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
    def test_ansible(self):
        instance_method_none = actions.Ansible({"adhoc_command": "test", "inventory": "test", "group": "test"})
        instance_method_empty = actions.Ansible({"method": "", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ""})
        instance_method_err = actions.Ansible({"method": "test", "adhoc_command": "-m ping", "inventory": "/etc/ansible/hosts", "group": "servers", "playbooks": ""})
        # instance_method_ok = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""})

        self.assertTupleEqual(instance_method_none.action_checkup(), ("method should be one of [\"ad_hoc\", \"playbook\"]", False))
        self.assertTupleEqual(instance_method_empty.action_checkup(), ("method should be one of [\"ad_hoc\", \"playbook\"]", False))
        self.assertTupleEqual(instance_method_err.action_checkup(), ("method should be one of [\"ad_hoc\", \"playbook\"]", False))
        # answer, state = instance_method_ok.action_checkup()
        # self.assertTrue(state)
        # self.assertEqual(answer, "")

        instance_adhoc_command_none = actions.Ansible({"method": "ad_hoc", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""})
        instance_adhoc_command_empty = actions.Ansible({"method": "ad_hoc", "adhoc_command": "", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""})
        instance_adhoc_command_err = actions.Ansible({"method": "ad_hoc", "adhoc_command": ["test1", "test2"], "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""})
        # instance_adhoc_command_ok = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/etc/ansible/hosts", "group": "all", "playbooks": ""})

        self.assertTupleEqual(instance_adhoc_command_none.action_checkup(), ("Field \"adhoc_command\" is required.", False))
        self.assertTupleEqual(instance_adhoc_command_empty.action_checkup(), ("Field \"adhoc_command\" is required.", False))
        self.assertTupleEqual(instance_adhoc_command_err.action_checkup(), ("Field \"adhoc_command\" is of type string.", False))
        # answer, state = instance_adhoc_command_ok.action_checkup()
        # self.assertTupleEqual((answer, state), ("", True))

        instance_playbooks_none = actions.Ansible({"method": "playbook", "adhoc_command": "", "inventory": "", "group": ""})
        instance_playbooks_empty = actions.Ansible({"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ""})
        instance_playbooks_err = actions.Ansible({"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": "test"})
        instance_playbooks_missing = actions.Ansible({"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ["/file/not/found", "/test/test2"]})
        # instance_playbooks_ok = actions.Ansible({"method": "playbook", "adhoc_command": "", "inventory": "", "group": "", "playbooks": ["/home/navid/PycharmProjects/has/playbooks/test.yaml"]})

        self.assertTupleEqual(instance_playbooks_none.action_checkup(), ("Field \"playbooks\" is required.", False))
        self.assertTupleEqual(instance_playbooks_empty.action_checkup(), ("Field \"playbooks\" is required.", False))
        self.assertTupleEqual(instance_playbooks_err.action_checkup(), ("playbooks should be of type list.", False))
        self.assertTupleEqual(instance_playbooks_missing.action_checkup(), ("Missing Playbooks Files Are :\n/file/not/found\n/test/test2", False))
        # answer, state = instance_playbooks_ok.action_checkup()
        # self.assertTupleEqual((answer, state), ("", True))

        instance_inventory_none = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "group": "", "playbooks": ""})
        instance_inventory_empty = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "", "playbooks": ""})
        instance_inventory_err = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": ["test"], "group": "", "playbooks": ""})
        instance_inventory_missing = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/file/not/found", "group": "", "playbooks": ""})
        instance_inventory_ok = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "/home/navid/PycharmProjects/has/inventory", "group": "", "playbooks": ""})

        self.assertTupleEqual(instance_inventory_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_inventory_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_inventory_err.action_checkup(), ("Inventory should be of type string.", False))
        self.assertTupleEqual(instance_inventory_missing.action_checkup(), ("No Such file or directory /file/not/found.", False))
        self.assertTupleEqual(instance_inventory_ok.action_checkup(), ("", True))

        instance_group_none = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "playbooks": ""})
        instance_group_empty = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "", "playbooks": ""})
        instance_group_err = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": ["test"], "playbooks": ""})
        instance_group_missing = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "cloud", "playbooks": ""})
        instance_group_ok = actions.Ansible({"method": "ad_hoc", "adhoc_command": "-m ping", "inventory": "", "group": "all", "playbooks": ""})

        self.assertTupleEqual(instance_group_none.action_checkup(), ("", True))
        self.assertTupleEqual(instance_group_empty.action_checkup(), ("", True))
        self.assertTupleEqual(instance_group_err.action_checkup(), ("Group should be of type string.", False))
        self.assertTupleEqual(instance_group_missing.action_checkup(), ("Group \"cloud\" is not valid", False))
        self.assertTupleEqual(instance_group_ok.action_checkup(), ("", True))


if __name__ == '__main__':
    unittest.main()
