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


@dataclass
class TOSECDatfile:
    header_name: str
    header_version: str
    games: Generator[TOSECXMLGame, None, None]


class TOSECParser(xml.sax.ContentHandler):
    def __init__(self):
        self._games = deque()
        self._current_game = None
        self._collecting_description = False
        self._in_header = False
        self._collecting_header_name = False
        self._collecting_header_version = False
        self.header_name = ""
        self.header_version = ""

    def startElement(self, name: str, attrs: AttributesImpl) -> None:
        if name == "header":
            self._in_header = True
        elif name == "game":
            self._current_game = {
                "name": attrs.getValue("name"),
                "description": "",
                "roms": [],
            }
        elif self._in_header and name == "name":
            self._collecting_header_name = True
        elif self._in_header and name == "version":
            self._collecting_header_version = True
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
        if name == "header":
            self._in_header = False
        elif name == "name" and self._collecting_header_name:
            self._collecting_header_name = False
        elif name == "version" and self._collecting_header_version:
            self._collecting_header_version = False
        elif name == "game":
            self._games.append(TOSECXMLGame(**self._current_game))
            self._current_game = None
        elif name == "description":
            self._collecting_description = False

    def characters(self, content: str) -> None:
        if self._collecting_header_name:
            self.header_name += content
        elif self._collecting_header_version:
            self.header_version += content
        elif self._collecting_description:
            self._current_game["description"] += content  # type: ignore


def _parse_tosec_filehandle(datfile) -> TOSECDatfile:
    parser = TOSECParser()
    xml.sax.parse(datfile, parser)

    def _games_generator() -> Generator[TOSECXMLGame, None, None]:
        while parser._games:
            yield parser._games.popleft()

    return TOSECDatfile(
        header_name=parser.header_name,
        header_version=parser.header_version,
        games=_games_generator(),
    )


def parse_tosec_data(tosec_data: str) -> TOSECDatfile:
    fh = StringIO(tosec_data)
    return _parse_tosec_filehandle(fh)


def parse_tosec_file(filename: str) -> TOSECDatfile:
    with open(filename, "r", encoding="utf-8") as f:
        return _parse_tosec_filehandle(f)
