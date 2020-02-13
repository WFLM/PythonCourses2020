#!/usr/bin/env python3


from typing import Tuple
import json
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod


class InputFilesParserError(Exception):
    pass


@dataclass
class Student:
    __slots__ = ("student_id", "name")
    student_id: int
    name: str


@dataclass
class Room:
    __slots__ = ("room_id", "name", "students")
    room_id: int
    name: str
    students: list


class FileParser(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, students_filename: str, rooms_filename: str) -> None:
        pass

    @abstractmethod
    def get_rooms(self) -> Tuple[Room, ...]:
        pass


class JSONParser(FileParser):
    """
    This class parses JSON-file and returns the tuple of Room-objects.
    Files can be read once (during initialization). If data in the files is changed, a new parser object should be made.
    """
    @staticmethod
    def _get_data_using_filename(filename: str) -> dict:
        """
        This staticmethod wraps json.load function.
        The main purpose is handling exceptions related to file-opening (wrong permission etc.)
        and JSON loading (corrupted file).
        """
        try:
            with open(file=filename, mode="r") as file_handler:
                return json.load(file_handler)
        except json.JSONDecodeError as err:
            raise InputFilesParserError(f"Input file '{filename}' is corrupted. {err}")

    def __init__(self, students_filename: str, rooms_filename: str) -> None:
        self._students_data: dict = self._get_data_using_filename(students_filename)
        self._rooms_data: dict = self._get_data_using_filename(rooms_filename)
        self._rooms_objects: dict = {}

    def _parse_rooms_data(self) -> None:
        """The method is used to parse "self._rooms_data", and fill the "self._rooms_objects" with empty rooms."""
        for room_data in self._rooms_data:
            room_object = Room(room_id=room_data["id"], name=room_data["name"], students=[])
            self._rooms_objects[room_data["id"]] = room_object

    def _parse_students_data(self) -> None:
        """
        The method is used to parse "self._students data",
        and fill Room objects from the "self._rooms_objects" dict with students.
        """
        for student_data in self._students_data:
            student_object = Student(student_id=student_data["id"], name=student_data["name"])
            self._rooms_objects[student_data["room"]].students.append(student_object)

    def get_rooms(self) -> Tuple[Room, ...]:
        """Get a tuple of Room-objects which contains Student-objects."""
        if not self._rooms_objects:
            try:
                self._parse_rooms_data()
                self._parse_students_data()
            except KeyError:
                raise InputFilesParserError("Input JSON data has the wrong form. For example, a student could be "
                                            "forced to register in the nonexistent room.")

        return tuple(self._rooms_objects[key] for key in sorted(self._rooms_objects))


parsers_for_input_files = {"json": JSONParser}
