from __future__ import annotations

import re
import sys

from .backends import Backend
from .dbschema import Game, Gameversion, Platform, Rom
from .shortnames import get_platform_short_name
from .tosec_parser import parse_tosec_file, parse_tosec_name
from .tosec_parser.name_parser import TosecParserError


def _parse_header_format(header_name: str) -> str:
    """Extract the format (e.g. 'D64', 'TAP') from the header name.

    TOSEC header names may contain a format in square brackets, e.g.
    'Commodore C16, C116 & Plus-4 - Games - [D64]'
    """
    m = re.search(r"\[([^\]]+)\]", header_name)
    if m:
        return m.group(1)
    return ""


def import_datfile(datfile_path: str, backend: Backend) -> None:
    datfile = parse_tosec_file(datfile_path)

    platform_name = f"{datfile.header_name} ({datfile.header_version})"
    short_name = get_platform_short_name(platform_name) or ""
    fmt = _parse_header_format(datfile.header_name)

    platform_id = backend.find_platform(platform_name)
    if platform_id is None:
        platform_id = backend.insert_platform(
            Platform(id=0, name=platform_name, short_name=short_name, format=fmt)
        )

    game_cache: dict[tuple[str, str, str], int] = {}
    game_count = 0
    skip_count = 0

    for xml_game in datfile.games:
        try:
            info = parse_tosec_name(xml_game.name)
        except TosecParserError as e:
            print(f"Skipping: {e}", file=sys.stderr)
            skip_count += 1
            continue

        game_key = (info.name, info.date, info.publisher)
        game_id = game_cache.get(game_key)
        if game_id is None:
            game_id = backend.find_game(info.name, info.date, info.publisher)
        if game_id is None:
            game_id = backend.insert_game(
                Game(id=0, name=info.name, date=info.date, publisher=info.publisher)
            )
        game_cache[game_key] = game_id

        gv_id = backend.insert_gameversion(
            Gameversion(
                id=0,
                name=xml_game.name,
                demo=info.demo,
                platform_id=platform_id,
                rom_count=len(xml_game.roms),
                game_id=game_id,
                system=info.system,
                video=info.video,
                country=info.country,
                language=info.language,
                dev_status=info.dev_status,
                media=info.media,
                copyright=info.copyright,
                cracked=info.cracked,
                fixed=info.fixed,
                hacked=info.hacked,
                modified=info.modified,
                pirated=info.pirated,
                trained=info.trained,
                translated=info.translated,
                overdumped=info.overdumped,
                underdumped=info.underdumped,
                virus=info.virus,
                baddump=info.baddump,
                alternate=info.alternate,
                verified=info.verified,
            )
        )

        for xml_rom in xml_game.roms:
            backend.insert_rom(
                Rom(
                    id=0,
                    name=xml_rom.name,
                    gameversion_id=gv_id,
                    size=xml_rom.size,
                    crc32=xml_rom.crc,
                    md5=xml_rom.md5,
                    sha1=xml_rom.sha1,
                )
            )

        game_count += 1

    print(f"Imported {game_count} game versions ({len(game_cache)} unique games).")
    if skip_count > 0:
        print(f"Skipped {skip_count} entries due to parse errors.", file=sys.stderr)
