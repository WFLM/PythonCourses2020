#!/usr/bin/env python3


import argparse
import sys


class ArgumentParserError(Exception):
    pass


class __ArgumentParser(argparse.ArgumentParser):
    """
    Overrides original exception-type to exception-type with human-readable error explanation.
    Write "ERROR: <message>" in stdout. Then return exit code 2.
    """
    def error(self, message):
        raise ArgumentParserError(message)


def parse():
    """Parse args from the CLI and return a tuple: (students: str, room: str, format: str)."""
    parser = __ArgumentParser(prog="rooms_accounting", description="Rooms accounting script.",
                              usage="rooms_accounting [-h] -s STUDENTS -r ROOM [-f FORMAT]")

    if len(sys.argv) == 1:
        parser.print_usage()
        parser.exit()

    parser.add_argument("-s", "--students",
                        metavar="STUDENTS",
                        type=str,
                        action="store",
                        dest="students_filename",
                        required=True,
                        help="input json file with students"
                        )

    parser.add_argument("-r", "--rooms",
                        metavar="ROOMS",
                        type=str,
                        action="store",
                        dest="rooms_filename",
                        required=True,
                        help="input json file with rooms"
                        )

    parser.add_argument("-f", "--format",
                        metavar="FORMAT",
                        type=str,
                        action="store",
                        dest="output_file_format",
                        required=False,
                        default="json",
                        help="output file format (json or xml; default = json)",
                        choices=("json", "xml")
                        )

    args = parser.parse_args()
    return args.students_filename, args.rooms_filename, args.output_file_format


if __name__ == "__main__":
    print("It is the CLI parsing module for rooms_accounting script.")
    try:
        students_filename, rooms_filename, output_file_format = parse()
    except ArgumentParserError as err:
        print(err)
    else:
        print("Output variables:\n"
              f"students_filename: {students_filename}\n"
              f"rooms_filename: {rooms_filename}\n"
              f"output_file_format: {output_file_format}")
