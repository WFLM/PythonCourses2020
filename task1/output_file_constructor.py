#!/usr/bin/env python3


from typing import Tuple
from abc import ABCMeta, abstractmethod
import json
from lxml import etree  # this cython module "lxml" is used because "xml" cannot make pretty-printed files

from input_files_parser import Room, Student


class OutputFileConstructorError(Exception):
    pass


class DataFileConstructor(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, rooms_object: Tuple[Room, ...]) -> None:
        pass

    @abstractmethod
    def construct_file(self, output_file_path: str) -> None:
        pass


class RoomStudentEncode(json.JSONEncoder):
    """This class is used for encoding Room and Student objects to JSON."""
    def default(self, o):
        if isinstance(o, Room):
            return {"id": o.room_id, "name": o.name, "students": o.students}
        elif isinstance(o, Student):
            return {"id": o.student_id, "name": o.name}
        else:
            super().default(self, o)  # it must raise exception


class JSONConstructor(DataFileConstructor):
    def __init__(self, rooms_objects: Tuple[Room, ...]) -> None:
        self._rooms_objects = rooms_objects

    def construct_file(self, output_file_path: str = "output.json") -> None:
        with open(file=output_file_path, mode="w") as json_output_fh:
            json.dump(obj=self._rooms_objects,
                      fp=json_output_fh,
                      cls=RoomStudentEncode,
                      sort_keys=True,
                      indent=4
                      )


class XMLConstructor(DataFileConstructor):
    def __init__(self, rooms_objects: Tuple[Room, ...]) -> None:
        self._rooms_objects = rooms_objects

    def _make_xml_root(self) -> etree._ElementTree:  # because of the etree.ElementTree is a cython function
        root_xml = etree.Element("rooms")

        for room_object in self._rooms_objects:
            room_xml = etree.Element("room")
            root_xml.append(room_xml)

            room_id_xml = etree.SubElement(room_xml, "id")
            room_id_xml.text = str(room_object.room_id)

            room_name_xml = etree.SubElement(room_xml, "name")
            room_name_xml.text = room_object.name

            students_xml = etree.SubElement(room_xml, "students")

            for student_object in room_object.students:
                student_xml = etree.SubElement(students_xml, "student")

                student_id_xml = etree.SubElement(student_xml, "id")
                student_id_xml.text = str(student_object.student_id)

                student_name_xml = etree.SubElement(student_xml, "name")
                student_name_xml.text = student_object.name

        tree = etree.ElementTree(root_xml)
        return tree

    def construct_file(self, output_file_path: str = "output.xml") -> None:
        tree = self._make_xml_root()
        tree.write(output_file_path, encoding="utf-8", pretty_print=True)


format_handlers = {"json": JSONConstructor, "xml": XMLConstructor}
