def source_handler(source):
    return "", True


def sources_handler(hesabi_name, hesabi_body):
    for source in hesabi_body.get("sources"):
        result, state = source_handler(source)
        if not state:
            return result, state
    return "", True


def pipe_type_handler(hesabi, matches):
    pass


def action_handler(hesabi, matches):
    pass
