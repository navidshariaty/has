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

    def __init__(self, matches):
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

    def __init__(self, matches, threshold, action_on_equals=False):
        self.action_on_equals = action_on_equals
        self.matches = matches
        self.threshold = int(threshold) if isinstance(threshold, str) else threshold
        if self.action_on_equals:
            self.threshold -= 1

    def needs_action(self):
        if len(self.matches) > self.threshold:
            return True
        return False


class Flatline:
    """
    :param matches
    :param floor
    :param action_on_equals
    if number of matched events is below a threshold , an action should get triggered
    """

    def __init__(self, matches, floor, action_on_equals=False):
        self.action_on_equals = action_on_equals
        self.matches = matches
        self.floor = int(floor) if isinstance(floor, str) else floor
        if self.action_on_equals:
            self.floor += 1

    def needs_action(self):
        if len(self.matches) < self.floor:
            return True
        return False


class Range:
    """
    :param
    if number of matched events is below a threshold , an action should get triggered
    """

    def __init__(self, matches, min_threshold, max_threshold, action_on_equals=False):
        self.min_threshold = int(min_threshold) if isinstance(min_threshold, str) else min_threshold
        self.max_threshold = int(max_threshold) if isinstance(max_threshold, str) else max_threshold
        self.action_on_equals = action_on_equals
        self.matches = matches
        if self.action_on_equals:
            self.min_threshold -= 1
            self.max_threshold += 1

    def needs_action(self):
        if self.min_threshold < len(self.matches) < self.max_threshold:
            return True
        return False


class HistoricalRange:
    def __init__(self, reference_window_matches, current_window_matches, compare_height, compare_type="both", action_on_equals=False):
        self.compare_type = compare_type
        self.compare_height = int(compare_height) if isinstance(compare_height, str) else compare_height
        self.ref_match = reference_window_matches
        self.cur_match = current_window_matches
        self.cur_match_length = len(self.cur_match)
        self.ref_match_length = len(self.ref_match)
        self.action_on_equals = action_on_equals

    def needs_action(self):
        met_up_condition, met_down_condition = False, False
        if self.action_on_equals and self.cur_match_length >= self.ref_match_length * self.compare_height:
            met_up_condition = True
        elif self.cur_match_length > self.ref_match_length * self.compare_height:
            met_up_condition = True
        if self.action_on_equals and self.cur_match_length * self.compare_height <= self.ref_match_length:
            met_down_condition = True
        elif self.cur_match_length * self.compare_height < self.ref_match_length:
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
