#!/usr/bin/env python3


import json
from dataclasses import dataclass


class JSONParserError(Exception):
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


class JSONParser:
    def __init__(self, students_filename, rooms_filename):
        with open(file=students_filename, mode="r") as students_fh:
            self._students_data = json.load(students_fh)

        with open(file=rooms_filename, mode="r") as rooms_fh:
            self._rooms_data = json.load(rooms_fh)

        self._rooms_objects = {}

    def _parse_students_data(self):
        for room_data in self._rooms_data:
            room_object = Room(room_id=room_data["id"], name=room_data["name"], students=[])
            self._rooms_objects[room_data["id"]] = room_object

    def _parse_rooms_data(self):
        for student_data in self._students_data:
            student_object = Student(student_id=student_data["id"], name=student_data["name"])
            self._rooms_objects[student_data["room"]].students.append(student_object)

    def parse(self):
        self._rooms_objects.clear()
        self._parse_students_data()

        try:
            self._parse_rooms_data()
        except KeyError as err:
            raise JSONParserError(f"Student is forced to register in nonexistent room (room id is {err})")

        return tuple(self._rooms_objects[key] for key in sorted(self._rooms_objects))
