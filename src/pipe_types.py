"""
this module describes response on queries on sources to determine if an action is needed or not
classes have one common function
    1) needs_action
        this function processes the matches and
"""


class Any:
    """
    in case of any match, an action should get triggered
    """
    types_required_options = frozenset([])

    def __init__(self, matches, *args):
        self.matches = matches

    def needs_action(self):
        if self.matches:
            return True
        return False


class Frequency:
    """
    :param matches
    :param threshold
    :param action_on_equals
    if number of matched events is above a threshold , an action should get triggered
    """
    types_required_options = frozenset(["threshold"])

    def __init__(self, matches, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        threshold = tmp_args.get("threshold")
        action_on_equals = tmp_args.get("action_on_equals") if tmp_args.get("action_on_equals") else False
        self.action_on_equals = action_on_equals
        self.matches = matches
        self.threshold = int(threshold) if isinstance(threshold, str) else threshold
        if self.action_on_equals:
            self.threshold -= 1

    def needs_action(self):
        if self.matches > self.threshold:
            return True
        return False


class Flatline:
    """
    :param matches
    :param floor
    :param action_on_equals
    if number of matched events is below a threshold , an action should get triggered
    """
    types_required_options = frozenset(["floor"])

    def __init__(self, matches, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        floor = tmp_args.get("floor")
        action_on_equals = tmp_args.get("action_on_equals") if tmp_args.get("action_on_equals") else False
        self.action_on_equals = action_on_equals
        self.matches = matches
        self.floor = int(floor) if isinstance(floor, str) else floor
        if self.action_on_equals:
            self.floor += 1

    def needs_action(self):
        if self.matches < self.floor:
            return True
        return False


class Range:
    """
    :param
    if number of matched events is not between two threshold(min_threshold, max_threshold) , an action should get triggered
    """
    types_required_options = frozenset(["min_threshold", "max_threshold"])

    def __init__(self, matches, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        min_threshold = tmp_args.get("min_threshold")
        max_threshold = tmp_args.get("max_threshold")
        action_on_equals = tmp_args.get("action_on_equals") if tmp_args.get("action_on_equals") else False
        self.min_threshold = int(min_threshold) if isinstance(min_threshold, str) else min_threshold
        self.max_threshold = int(max_threshold) if isinstance(max_threshold, str) else max_threshold
        self.action_on_equals = action_on_equals
        self.matches = matches
        if self.action_on_equals:
            self.min_threshold -= 1
            self.max_threshold += 1

    def needs_action(self):
        if self.min_threshold < self.matches < self.max_threshold:
            return True
        return False


class HistoricalRange:
    """
    this class will compare two time windows and compare them
    for example if you query between 10:00-12:00 =>  ref window(8:00-10:00) and cur window(10:00-12:00)
    if the number of matches had a huge growth or reduce in cur window than ref window , an action should get triggered
    this class is not working for now because the time window is not supported yet but you can specify it manually
    """
    types_required_options = frozenset(["reference_window_matches", "current_window_matches", "compare_height", "compare_type"])

    def __init__(self, *args):
        valid = True if args and len(args) else False
        tmp_args = args[0] if valid else {}
        reference_window_matches = tmp_args.get("reference_window_matches")
        current_window_matches = tmp_args.get("current_window_matches")
        compare_height = tmp_args.get("compare_height")
        compare_type = tmp_args.get("compare_type")
        action_on_equals = tmp_args.get("action_on_equals") if tmp_args.get("action_on_equals") else False
        self.compare_type = compare_type
        self.compare_height = int(compare_height) if isinstance(compare_height, str) else compare_height
        self.ref_match = reference_window_matches
        self.cur_match = current_window_matches
        self.cur_match_length = self.cur_match
        self.ref_match_length = self.ref_match
        self.action_on_equals = action_on_equals

    def needs_action(self):
        met_up_condition, met_down_condition = False, False
        if self.action_on_equals and self.cur_match >= self.ref_match * self.compare_height:
            met_up_condition = True
        elif self.cur_match > self.ref_match * self.compare_height:
            met_up_condition = True
        if self.action_on_equals and self.cur_match * self.compare_height <= self.ref_match:
            met_down_condition = True
        elif self.cur_match * self.compare_height < self.ref_match:
            met_down_condition = True
        if self.compare_type == "up":
            if met_up_condition:
                return True
        elif self.compare_type == "down":
            if met_down_condition:
                return True
        elif self.compare_type == "both":
            if met_down_condition or met_up_condition:
                return True
        return False
