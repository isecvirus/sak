# kmz ($VERSION)

"""
Copyright (c) virus, All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import hashlib
import random
from typing import NoReturn
from zipfile import ZipFile, ZIP_DEFLATED

VERSION = "1.1.0"

class Point(dict):
    def set_name(self, name: float) -> None:
        self['name'] = name

    def get_name(self) -> str:
        return self['name']

    def set_x(self, x: float) -> None:
        self['x'] = x

    def get_x(self) -> float:
        return self['x']

    def set_y(self, y: float) -> None:
        self['y'] = y

    def get_y(self) -> float:
        return self['y']

    def set_z(self, z: float) -> None:
        self['z'] = z

    def get_z(self) -> float:
        return self['z']

class KMZ:
    def __init__(self, filename: str):
        self.filename: str = filename
        self.points: {str: Point} = {}

    def add_point(self, x: float, y: float, z: float = 0.0, name: str = "") -> NoReturn:
        """
        Add a new point
        :param x: x coordinates
        :param y: y coordinates
        :param z: z coordinates
        :param name: The pin name
        :return:
        """

        id: str = self.generate_id()
        data: Point = Point({"name": name, "x": x, "y": y, "z": z})

        if not data in self.points.values():
            self.points[id] = data

    def get_points(self) -> dict:
        """
        Get a dict of all points
        :return:
        """

        return self.points

    def get_kml(self) -> str:
        """
        Get the raw (Key-hole Markup Language) content
        :return:
        """

        # add opening header
        data: str = (
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            f"<kml project=\"kmz\" author=\"virus\" version=\"{VERSION}\">"
            "<Document>"
        )

        for point in self.points:
            name: str = str(self.points[point].get_name())
            x: float = float(self.points[point].get_x())
            y: float = float(self.points[point].get_y())
            z: float = float(self.points[point].get_z())

            # add point to data
            data += (f"<Placemark id=\"{point}\">"
                         f"<name>{name}</name>"
                         f"<Point>"
                            f"<coordinates>{x},{y},{z}</coordinates>"
                         f"</Point>"
                     f"</Placemark>")

        # add closing footer
        data += "</Document></kml>"

        return data

    def get_point(self, id: str) -> Point:
        """
        Get a certain point
        :param id:
        :return:
        """

        if id in self.points:
            return self.points[id]

    def save(self, datafile: str, encoding: str = "utf-8"):
        """
        Save the KMZ file
        :param datafile: the output file
        :param encoding: the encoding type
        :return:
        """

        with ZipFile(self.filename, "w", ZIP_DEFLATED) as data_file:
            data_file.writestr(
                datafile,
                self.get_kml().encode(
                    encoding=encoding,
                    errors="replace"
                )
            )

    @staticmethod
    def generate_id(bits: int = 128) -> str:
        """
        Generate a uniq id for each point
        :param bits: the size of the random id bytes
        :return:
        """

        rand_bits: int = random.getrandbits(bits)

        rand_id: str = hashlib.sha1(
            str(rand_bits).encode()
        ).hexdigest()[20:]

        id: str = "-".join(
            [
                rand_id[i:i + 4] for i in range(0, len(rand_id), 4)
            ]
        )
        return id
