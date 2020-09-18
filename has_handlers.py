from hesabi_verification import sources_mapping, pipe_types_mapping


def source_handler(source):
    source_instance = sources_mapping.get(source.get("source"))(source)
    conn = source_instance.get_connection()
    query = source_instance.get_query(None, None, source)
    matches = source_instance.get_result(conn, query, source)
    return matches, True


def sources_handler(hesabi_name, hesabi_body):
    all_matches = []
    for source in hesabi_body.get("sources"):
        result, state = source_handler(source)
        if not state:
            return result, state
        all_matches.append(result)
    return all_matches, True


def pipe_type_handler(hesabi, matches):
    pipe_type_body = hesabi.get("pipe_type")[0]
    pipe_type_instance = pipe_types_mapping.get(pipe_type_body.get("type"))(pipe_type_body)


def action_handler(hesabi, matches):
    pass
