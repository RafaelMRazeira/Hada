import os
import argparse


DEFAULT_LOG_DIR = os.path.dirname(os.path.realpath(__file__))

TASK = {"create_dataset"}


def main():
    """HAbeas Data Autism CLI

    Usage:
        hada-cli  COMMAND [ARGS...] [options]

    Commands:
        create_dataset   Initiate a dataset cli for a specific task.

    Options:
        -h, --help     Show this screen.

    """
    parser = argparse.ArgumentParser(description="Hada CLI.")
    parser.add_argument("--task", type=str, help="Task")
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)


if __name__ == "__main__":
    main()
