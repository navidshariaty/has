from hesabi_verification import sources_mapping, pipe_types_mapping, actions_mapping


def source_handler(source):
    """
    this function loads one specific source from hesabi body , has a filter and queries db dependent on type and fetches the matching results
    :param source: json loaded body of hesabi
    :return: fetches matches that meet the filters and True
    """
    source_instance = sources_mapping.get(source.get("source"))(source)
    conn = source_instance.get_connection()
    query = source_instance.get_query(None, None, source)
    matches = source_instance.get_result(conn, query, source)
    return matches, True


def sources_handler(hesabi_name, hesabi_body):
    """
    calls function "source_handler" multiple times for each source on hesabi body. also makes an statistics from all sources dependent on their names
    :param hesabi_name:
    :param hesabi_body:
    :return:
    """
    statistics = dict()
    all_matches = 0
    for source in hesabi_body.get("sources"):
        result, state = source_handler(source)
        if not state:
            return statistics, result, state
        statistics.update({source.get("name"): result})
        all_matches += result
    return statistics, all_matches, True


def pipe_type_handler(hesabi_name, hesabi_body, matches):
    pipe_type_body = hesabi_body.get("pipe_type")[0]
    pipe_type_instance = pipe_types_mapping.get(pipe_type_body.get("type"))(matches, pipe_type_body)
    state = pipe_type_instance.needs_action()
    return state


def action_handler(hesabi_name, hesabi_body, action_body, *args):
    agg_values = args[0] if args and args[0] else []
    instance_action = actions_mapping.get(action_body.get("action"))(hesabi_name, hesabi_body, action_body, agg_values)
    result, status = instance_action.action_checkup()
    if not status:
        return result, status
    result, status = instance_action.run_action()
    if not status:
        return result, status
    return "", True


def actions_handler(hesabi_name, hesabi_body, *args):
    for action in hesabi_body.get("actions"):
        result, state = action_handler(hesabi_name, hesabi_body, action, args)
        if not state:
            return result, state
    return "", True


def should_perform_aggr_query(hesabi_body):
    """
    this function specifies if we should go for agg field from sources or not
    :param hesabi_body:
    :return:
    """
    if "agg_field" in hesabi_body:
        return True
    return False


def aggr_field_handler(hesabi_name, hesabi_body):
    """
    this functinon handles the process of fetching agg_field from sources and also makes an statistics from each.calls "source_handler_aggr_field" multiple times on each source.
    :param hesabi_name:
    :param hesabi_body:
    :return:
    """
    # TODO : user should be able to define a pattern based on sources names : (e.g.   (name1 AND name2) OR name3)
    statistics = dict()
    operate_on_field = set()
    counter = 0
    agg_field_value = hesabi_body.get("agg_field")
    for source in hesabi_body.get("sources"):
        result, state = source_handler_aggr_field(source, agg_field_value)
        if not state:
            return statistics, result, state
        statistics.update({source.get("name"): result})
    if hesabi_body.get("sources_operator") == "or":
        for key in statistics.values():
            tmp_union = set(key)
            operate_on_field = operate_on_field.union(tmp_union)
    elif hesabi_body.get("sources_operator") == "and":
        for key in statistics.values():
            if counter == 0:
                operate_on_field = set(key)
                counter += 1
            else:
                tmp_inter = set(key)
                operate_on_field = operate_on_field.intersection(tmp_inter)
    return statistics, operate_on_field, True


def source_handler_aggr_field(source, agg_field):
    """
    handles the process of fetching data from source
    makes a connection and a query and uses them to fetch data with passed filters
    :param source: the hesabi body
    :param agg_field: the name of the field we perform aggregation on
    :return: the values of agg_field from matched events
    """
    source_instance = sources_mapping.get(source.get("source"))(source)
    conn = source_instance.get_connection()
    query = source_instance.get_query_aggr_field(None, None, agg_field, source)
    matches = source_instance.get_results_aggr_field(conn, query, source)
    return matches, True
