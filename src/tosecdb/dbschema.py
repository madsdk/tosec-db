from dataclasses import dataclass


@dataclass
class Platform:
    id: int
    name: str
    short_name: str
    format: str


@dataclass
class Game:
    id: int
    name: str
    date: str
    publisher: str


@dataclass
class Gameversion:
    id: int
    name: str
    demo: bool
    platform_id: int
    rom_count: int
    game_id: int
    system: str | None = None
    video: str | None = None
    country: str | None = None
    language: str | None = None
    dev_status: str | None = None
    media: str | None = None
    copyright: str | None = None
    cracked: bool = False
    fixed: bool = False
    hacked: bool = False
    modified: bool = False
    pirated: bool = False
    trained: bool = False
    translated: bool = False
    overdumped: bool = False
    underdumped: bool = False
    virus: bool = False
    baddump: bool = False
    alternate: bool = False
    verified: bool = False


@dataclass
class Rom:
    id: int
    name: str
    gameversion_id: int
    size: int
    crc32: str
    md5: str
    sha1: str
