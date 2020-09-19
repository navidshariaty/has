import has_sources
import actions
import pipe_types
import os


sources_mapping = {
    "ElasticSearch": has_sources.ElasticSearch,
    "Zabbix": has_sources.Zabbix,
    "Prometheus": has_sources.Prometheus
}

pipe_types_mapping = {
    "any": pipe_types.Any,
    "frequency": pipe_types.Frequency,
    "flatline": pipe_types.Flatline,
    "range": pipe_types.Range,
    "historical_range": pipe_types.HistoricalRange
}

actions_mapping = {
    "email": actions.Email,
    "ansible": actions.Ansible,
    "command": actions.Command,
    "debug": actions.Debug
}


class Verify:
    def __init__(self, hesabi_body, hesabi_path):
        self.body = hesabi_body
        self.path = hesabi_path

    def verifier(self):
        if not self.body:
            return "Empty body for hesabi \"{}\"".format(self.path), False
        if not self.body.get("hesabi_uuid"):
            return "hesabi \"{}\" does not contain an uuid.".format(self.path), False
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
        all_names = []
        for source in self.body.get("sources"):
            if "name" not in source:
                return "source does not contain name in hesabi {}".format(self.path), False
            if isinstance(source.get("name"), str):
                if source.get("name") in all_names:
                    return "name \"{}\" already exists in hesabi {}".format(source.get("name"), self.path), False
                all_names.append(source.get("name"))
            else:
                return "name \"{}\" is of type {} while should be string in hesabi \"{}\"".format(source.get("name"), type(source.get("name")), self.path), False
            if "source" not in source:
                return "source field not found in sources of hesabi \"{}\"".format(self.path), False
            if source.get("source") not in sources_mapping.keys():
                return "Unknown Source \"{}\" used in hesabi \"{}\"".format(source.get("source"), self.path), False
            for field in sources_mapping.get(source.get("source")).required_options:
                if field not in source:
                    return "field \"{}\" is required and not specified in hesabi \"{}\" sources.".format(field, self.path), False
            if "agg_field" in source:
                if "agg_field" not in self.body:
                    return "field \"agg_field\" specified in source \"{}\" of hesabi \"{}\" but not in the body.".format(source.get("name"), self.path), False
            if "agg_field" in self.body:
                if "sources_operator" not in self.body:
                    return "agg_field is used but field \"sources_operator\" is not defined in hesabi body \"{}\"".format(self.path), False
                if self.body.get("sources_operator") not in ["and", "or"]:
                    return "field \"sources_operator\" should be [\"yes\",\"no\"], while is \"{}\" in hesabi body \"{}\"".format(self.body.get("sources_operator"), self.path), False
        return "", True

    def advanced_verify_actions(self):
        for action in self.body.get("actions"):
            if "action" not in action:
                return "action field not found in actions of hesabi \"{}\"".format(self.path), False
            if action.get("action") not in actions_mapping.keys():
                return "Unknown action \"{}\" used in hesabi \"{}\"".format(action.get("action"), self.path), False
            for field in actions_mapping.get(action.get("action")).action_required_options:
                if field not in action:
                    return "field \"{}\" is required and not specified in hesabi \"{}\" actions.".format(field, self.path), False
            if "use_aggr_values" in action:
                if "agg_field" not in self.body:
                    return "You can not use field \"use_aggr_values\" while field \"agg_field\" is not defined.", False
                elif str(action.get("use_aggr_values")) not in ["True", "False"]:
                    return "field \"use_aggr_values\" is boolean and only accepts [\"true\", \"false\"] but it's value is \"{}\" in hesabi \"{}\"".format(str(action.get("use_aggr_values")), self.path), False
        return "", True

    def advanced_verify_pipe_type(self):
        pipe_type_body = self.body.get("pipe_type")[0]
        if "pipe_type" not in self.body:
            return "pipe_type field not found in hesabi \"{}\"".format(self.path), False
        if pipe_type_body.get("type") not in pipe_types_mapping.keys():
            return "Unknown pipe_type \"{}\" used in hesabi \"{}\"".format(pipe_type_body.get("type"), self.path), False
        for field in pipe_types_mapping.get(pipe_type_body.get("type")).types_required_options:
            if field not in pipe_type_body:
                return "field \"{}\" is required and not specified in hesabi \"{}\" pipe_type.".format(field, self.path), False
        return "", True
