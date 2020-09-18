import sources
import actions
import pipe_types
import os


class Verify:
    def __init__(self, hesabi_body, hesabi_path):
        self.body = hesabi_body
        self.path = hesabi_path

    def verifier(self):
        if not self.body:
            return "Empty body for hesabi \"{}\"".format(self.path), False
        result, state = self.basic_verify()

    def basic_verify_source(self):
        if "sources" not in self.body:
            return "\"sources\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("sources"), list):
            return "\"sources\" is of type {} while should be list, in hesabi {}".format(type(self.body.get("sources")), self.path)
        return "", False

    def basic_verify_hesabies_path(self):
        if "hesabies_path" not in self.body:
            return "\"hesabies_path\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("hesabies_path"), str):
            return "\"hesabies_path\" is of type {} while should be string, in hesabi {}".format(type(self.body.get("hesabies_path")), self.path)
        if not os.path.isdir(self.body.get("hesabies_path")):
            return "No such directory \"{}\" defined in hesabi \"{}\".".format(hesabies_path, self.path)
        return "", False

    def basic_verify_actions(self):
        if "actions" not in self.body:
            return "\"actions\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("actions"), list):
            return "\"actions\" is of type {} while should be list, in hesabi {}".format(type(self.body.get("actions")), self.path)
        return "", False

    def basic_verify_pipe_types(self):
        if "pipe_type" not in self.body:
            return "\"pipe_type\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("pipe_type"), list):
            return "\"pipe_type\" is of type {} while should be list, in hesabi {}".format(type(self.body.get("pipe_type")), self.path)
        if not len(self.body.get("pipe_type")) == 1:
            return "\"pipe_type\" should be of length 1 in hesabi \"{}\"".format(self.path)
        return "", False

    def basic_verify(self):
        result_source, valid_source = self.basic_verify_source()
        if not valid_source:
            return result_source, valid_source
        result_path, valid_path = self.basic_verify_hesabies_path()
        if not valid_path:
            return result_path, valid_path
        result_pipe_type, valid_pipe_type = self.basic_verify_pipe_types()
        if not valid_pipe_type:
            return result_pipe_type, valid_pipe_type
        result_actions, valid_actions = self.basic_verify_actions()
        if not valid_actions:
            return result_actions, valid_actions
        if valid_source and valid_path and valid_pipe_type and valid_actions:
            return True
        return False

    def detail_verify_sources(self):
        pass

    def detail_verify_actions(self):
        pass

    def detail_verify_pipe_type(self):
        pass