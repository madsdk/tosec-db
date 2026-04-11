"""
Functions for parsing TOSEC names. This includes functions for parsing the various fields in the TOSEC naming convention,
such as demo types, system types, video standards, country codes, language codes, development status, media
types, copyright status, and dump flags. These functions are used to validate the various fields in the TOSEC naming convention,
and to extract the relevant information from the TOSEC name.
"""

import re
from dataclasses import dataclass


from .definitions import (
    tosec_demo,
    tosec_system,
    tosec_video,
    tosec_country,
    tosec_language,
    tosec_dev_status,
    tosec_media,
    tosec_copyright,
)


@dataclass
class TOSECInfo:
    name: str
    date: str
    publisher: str
    demo: bool = False
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


class TosecParserError(Exception):
    pass


def parse_tosec_name(tosec_name: str) -> TOSECInfo:
    """
    Parses a TOSEC name and returns a TOSECInfo object containing the relevant information.
    The TOSEC name is expected to follow the TOSEC naming convention, an exception will be
    raised if the name does not follow the convention.

    Expected format: Title version (demo) (Date)(Publisher)(System)(Video)(Country)(Language)(Copyright)(Devstatus)(Media Type)(Media Label)[cr][f][h][m][p][t][tr][o][u][v][b][a][!][more info]
    """
    # Search for the date, anything before that is the full name and possibly a demo tag.
    date_regexp = re.compile(
        r"\(((19|20)[x0-9][x0-9](\-[x0-9][x0-9](\-[x0-9][x0-9])?)?)\)"
    )
    m = date_regexp.search(tosec_name)
    if m is None:
        raise TosecParserError(
            'Invalid TOSEC name "{}" found. Cannot find date.'.format(tosec_name)
        )
    name = tosec_name[: m.start()]
    if len(name) == 0:
        raise TosecParserError(
            'Invalid TOSEC name "{}" found. Title is empty.'.format(tosec_name)
        )

    name = name.strip()
    date = m.group(1)

    # Remove any demo tags from the title.
    is_demo = False
    for demo_tag in [f"({s})" for s in tosec_demo]:
        if name.lower().endswith(demo_tag):
            name = name[: -len(demo_tag)].strip()
            is_demo = True
            break

    # The next token is the publisher.
    rest = tosec_name[m.end() :]
    if len(rest) == 0 or rest[0] != "(":
        raise TosecParserError(
            'Invalid TOSEC name "{}" found. No publisher found.'.format(tosec_name)
        )
    i = rest.find(")")
    if i == -1:
        raise TosecParserError(
            'Invalid TOSEC name "{}" found. No publisher found.'.format(tosec_name)
        )
    publisher = rest[1:i]
    info = TOSECInfo(name=name, date=date, publisher=publisher, demo=is_demo)

    # The rest are optional. Start by grabbing any tokens within parenteses.
    rest = rest[i + 1 :]
    token_regexp = re.compile(r"\(([^\(\)]+)\)")
    m = token_regexp.match(rest)
    while m is not None:
        for group in m.groups():
            # System
            if group in tosec_system:
                info.system = group
            # Video
            if group in tosec_video:
                info.video = group
            # Country
            tokens = group.split("-")
            all_countries = True
            for token in tokens:
                if token not in tosec_country:
                    all_countries = False
            if all_countries:
                info.country = group
            # Language
            tokens = group.split("-")
            all_languages = True
            for token in tokens:
                if token not in tosec_language:
                    all_languages = False
            if all_languages:
                info.language = group
            # Development status
            if group in tosec_dev_status:
                info.dev_status = group
            # Media
            if group[:4] in tosec_media:
                info.media = group
            # Copyright
            if group in tosec_copyright:
                info.copyright = group
        rest = rest[m.end() :]
        m = token_regexp.match(rest)

    # Read dump info flags.
    token_regexp = re.compile(r"\[([^\[\]]+)\]")
    m = token_regexp.match(rest)
    while m is not None:
        for group in m.groups():
            if group.startswith("cr"):
                info.cracked = True
            elif group.startswith("f"):
                info.fixed = True
            elif group.startswith("h"):
                info.hacked = True
            elif group.startswith("m"):
                info.modified = True
            elif group.startswith("p"):
                info.pirated = True
            elif group.startswith("tr"):
                info.translated = True
            elif group.startswith("t"):
                info.trained = True
            elif group.startswith("o"):
                info.overdumped = True
            elif group.startswith("u"):
                info.underdumped = True
            elif group.startswith("v"):
                info.virus = True
            elif group.startswith("b"):
                info.baddump = True
            elif group.startswith("a"):
                info.alternate = True
            elif group.startswith("!"):
                info.verified = True

        rest = rest[m.end() :]
        m = token_regexp.match(rest)

    return info
