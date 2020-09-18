import argparse
import hesabs
import has_view
import sys
import logging
import has_handlers


logging_mapping = {
    "not_set": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}


def build_logger():
    return logging.Logger("HAS")


def handle_result_state(result, state, exit_on_errors=True):
    has_view.View(result, state, only_view_on_errors=True)
    if not state:
        if exit_on_errors:
            sys.exit()


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-c", "--config", dest="config", required=True, help="absolute path to config file.(in case of multiple config files, last one will get ahead of the rest.)")
    return args.parse_args()


def main():
    args = parse_args()
    config_content, state = hesabs.load_config(args.config)
    handle_result_state(result=config_content, state=state)
    logger = build_logger()
    logging.basicConfig(level=logging.DEBUG)
    logger_level = logging_mapping.get(config_content.get("logging_level")) if "logging_level" in config_content else logging.INFO
    logger.setLevel(logger_level)
    hesabies, state = hesabs.load_hesabi_bodies(config_content.get("hesabies_path"))
    logger.warning("[ * ] {} hesabies loaded.\n".format(len(hesabies)))
    handle_result_state(result=hesabies, state=state)
    for hesabi_path in hesabies:
        result, state = hesabs.verify_hesabi(hesabi_path=hesabi_path, hesabi_content=hesabies.get(hesabi_path))
        handle_result_state(result=result, state=state)
        logger.warning("hesabi \"{}\" verified.".format(hesabi_path))
    logger.warning("[ * ] all hesabies verified\n")
    for hesabi in hesabies:
        logger.warning("[  ] fetching data from sources of hesabi {}".format(hesabi))
        result, state = has_handlers.sources_handler(hesabi_name=hesabi, hesabi_body=hesabies.get(hesabi))
        handle_result_state(result=result, state=state)
        logger.warning("[ * ] Done fetching.\n")
        logger.warning("[  ] pipe_type processing started.")
        logger.warning("received a total number of \"{}\" matches.".format(result))
        result = has_handlers.pipe_type_handler(hesabi, hesabies.get(hesabi), result)
        handle_result_state("an action was not needed.", result, exit_on_errors=False)
        logger.warning("[ * ] pipe_type processing completed.")
        logger.warning("[  ] triggering actions started.")
        logger.warning("[ * ] actions triggered.")


if __name__ == '__main__':
    main()
