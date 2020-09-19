from hesabi_verification import sources_mapping, pipe_types_mapping


def source_handler(source):
    source_instance = sources_mapping.get(source.get("source"))(source)
    conn = source_instance.get_connection()
    query = source_instance.get_query(None, None, source)
    matches = source_instance.get_result(conn, query, source)
    return matches, True


def sources_handler(hesabi_name, hesabi_body):
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


def action_handler(hesabi, matches):
    pass


def actions_handler(hesabi, matches):
    return True


def should_perform_aggr_query(hesabi_body):
    if "agg_field" in hesabi_body:
        return True
    return False


def aggr_field_handler(hesabi_name, hesabi_body):
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
    source_instance = sources_mapping.get(source.get("source"))(source)
    conn = source_instance.get_connection()
    query = source_instance.get_query_aggr_field(None, None, agg_field, source)
    matches = source_instance.get_results_aggr_field(conn, query, source)
    return matches, True
