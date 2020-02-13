#!/usr/bin/env python3


import cli_parser
import input_files_parser
import output_file_constructor


INPUT_FORMAT = "json"


def main():
    try:
        students_filename, rooms_filename, output_file_format = cli_parser.parse_command_line_args()

        FileParser = input_files_parser.parsers_for_input_files[INPUT_FORMAT]
        parser_object = FileParser(students_filename=students_filename,
                                   rooms_filename=rooms_filename)

        rooms_objects = parser_object.get_rooms()

        FileConstructor = output_file_constructor.format_handlers[output_file_format]
        file_constructor = FileConstructor(rooms_objects)
        file_constructor.construct_file()

    except (cli_parser.ArgumentParserError,
            input_files_parser.InputFilesParserError,
            OSError) as err:
        print(f"{type(err).__name__}: {err}")  # it's an optional thing and used to cut traceback for the user
        exit(2)

    else:
        print("Output file has been created.")


if __name__ == "__main__":
    main()
