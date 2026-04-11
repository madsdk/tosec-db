"""
A generator that reads TOSEC data from a datfile and yields game info.
"""

from io import StringIO
import xml.sax
from collections import deque
from typing import Generator
from xml.sax.xmlreader import AttributesImpl
from dataclasses import dataclass


@dataclass
class TOSECXMLRom:
    name: str
    size: int
    crc: str
    md5: str
    sha1: str


@dataclass
class TOSECXMLGame:
    name: str
    description: str
    roms: list[TOSECXMLRom]


class TOSECParser(xml.sax.ContentHandler):
    def __init__(self):
        self._games = deque()
        self._current_game = None
        self._collecting_description = False

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if name == "game":
            self._current_game = {
                "name": attrs.getValue("name"),
                "description": "",
                "roms": [],
            }
        elif name == "description":
            if self._current_game is not None:
                self._collecting_description = True
        elif name == "rom":
            if self._current_game is not None:
                rom_data = {}

                try:
                    rom_data["name"] = attrs.getValue("name")
                except KeyError:
                    pass
                try:
                    rom_data["size"] = int(attrs.getValue("size"))
                except KeyError:
                    pass
                try:
                    rom_data["crc"] = attrs.getValue("crc")
                except KeyError:
                    pass
                try:
                    rom_data["md5"] = attrs.getValue("md5")
                except KeyError:
                    pass
                try:
                    rom_data["sha1"] = attrs.getValue("sha1")
                except KeyError:
                    pass

                try:
                    self._current_game["roms"].append(TOSECXMLRom(**rom_data))
                except TypeError:
                    pass

    def endElement(self, name: str) -> None:
        if name == "game":
            self._games.append(self._current_game)
            self._current_game = None
        elif name == "description":
            self._collecting_description = False

    def characters(self, content: str) -> None:
        if self._collecting_description:
            self._current_game["description"] += content  # type: ignore


def _parse_tosec_filehandle(datfile) -> Generator[TOSECXMLGame, None, None]:
    parser = TOSECParser()
    xml.sax.parse(datfile, parser)

    while parser._games:
        yield parser._games.popleft()


def parse_tosec_data(tosec_data: str) -> Generator[TOSECXMLGame, None, None]:
    fh = StringIO(tosec_data)
    return _parse_tosec_filehandle(fh)


def parse_tosec_file(filename: str) -> Generator[TOSECXMLGame, None, None]:
    with open(filename, "r", encoding="utf-8") as f:
        return _parse_tosec_filehandle(f)
