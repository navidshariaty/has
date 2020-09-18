import argparse
import hesabs
import has_view


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("-c", "--config", dest="config", required=True, help="path to config file.(in case of multiple config files, last one will get ahead of the rest.)")
    return args.parse_args()


def main():
    args = parse_args()
    config_content, state = hesabs.load_config(args.config)
    has_view.View(config_content, state, only_view_on_errors=True)
    if not state:
        exit(1)
    print(config_content)


if __name__ == '__main__':
    main()
