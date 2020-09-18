import has_sources
import actions
import pipe_types
import os


sources_mapping = {
    "ElasticSearch": has_sources.ElasticSearch,
    "Zabbix": has_sources.Zabbix,
    "Prometheus": has_sources.Prometheus
}

class Verify:
    def __init__(self, hesabi_body, hesabi_path):
        self.body = hesabi_body
        self.path = hesabi_path

    def verifier(self):
        if not self.body:
            return "Empty body for hesabi \"{}\"".format(self.path), False
        result, state = self.basic_verify()
        if not state:
            return result, state
        result, state = self.advanced_verify()
        if not state:
            return result, state
        return "", True

    def basic_verify_sources(self):
        if "sources" not in self.body:
            return "\"sources\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("sources"), list):
            return "\"sources\" is of type {} while should be list, in hesabi {}".format(type(self.body.get("sources")), self.path)
        return "", True

    def basic_verify_actions(self):
        if "actions" not in self.body:
            return "\"actions\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("actions"), list):
            return "\"actions\" is of type {} while should be list, in hesabi {}".format(type(self.body.get("actions")), self.path)
        return "", True

    def basic_verify_pipe_type(self):
        if "pipe_type" not in self.body:
            return "\"pipe_type\" not found in hesabi \"{}\"".format(self.path), False
        if not isinstance(self.body.get("pipe_type"), list):
            return "\"pipe_type\" is of type {} while should be list, in hesabi {}".format(type(self.body.get("pipe_type")), self.path)
        if not len(self.body.get("pipe_type")) == 1:
            return "\"pipe_type\" should be of length 1 in hesabi \"{}\"".format(self.path)
        return "", True

    def basic_verify(self):
        result_sources, valid_sources = self.basic_verify_sources()
        if not valid_sources:
            return result_sources, valid_sources
        result_pipe_type, valid_pipe_type = self.basic_verify_pipe_type()
        if not valid_pipe_type:
            return result_pipe_type, valid_pipe_type
        result_actions, valid_actions = self.basic_verify_actions()
        if not valid_actions:
            return result_actions, valid_actions
        if valid_sources and valid_pipe_type and valid_actions:
            return "", True

    def advanced_verify(self):
        result_sources, valid_sources = self.advanced_verify_sources()
        if not valid_sources:
            return result_sources, valid_sources
        result_pipe_type, valid_pipe_type = self.advanced_verify_pipe_type()
        if not valid_pipe_type:
            return result_pipe_type, valid_pipe_type
        result_actions, valid_actions = self.advanced_verify_actions()
        if not valid_actions:
            return result_actions, valid_actions
        if valid_sources and valid_pipe_type and valid_actions:
            return "", True

    def advanced_verify_sources(self):
        for source in self.body.get("sources"):
            if not "source" in source:
                return "source field not found in sources of hesabi \"{}\"".format(self.path), False
            if not source.get("source") in sources_mapping.keys():
                return "Unknown Source \"{}\" used in hesabi \"{}\"".format(source.get("source"), self.path), False
            for field in sources_mapping.get(source.get("source")).required_options:
                if field not in source:
                    return "field \"{}\" is required and not specified in hesabi \"{}\"".format(field, self.path), False
        return "", True

    def advanced_verify_actions(self):
        return "", True

    def advanced_verify_pipe_type(self):
        return "", True
