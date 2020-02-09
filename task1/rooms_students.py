#!/usr/bin/env python3


import cli_parser
import json_parser
import output_files_constructor as ofc


def main():
    try:
        students_filename, rooms_filename, output_file_format = cli_parser.parse()
        json_parser_object = json_parser.JSONParser(students_filename=students_filename, rooms_filename=rooms_filename)
        rooms_objects = json_parser_object.parse()

        FileConstructor = ofc.format_handlers[output_file_format]
        file_constructor = FileConstructor(rooms_objects)
        file_constructor.construct_file()

    except Exception as err:
        print(f"{type(err).__name__}: {err}")
        exit(2)

    else:
        print("Output file has been created.")


if __name__ == "__main__":
    main()
