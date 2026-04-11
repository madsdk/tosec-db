from __future__ import annotations

import os
import re
import sqlite3
from typing import Protocol

from .dbschema import Game, Gameversion, Platform, Rom


class Backend(Protocol):
    def initialize(self) -> None: ...
    def insert_platform(self, platform: Platform) -> int: ...
    def insert_game(self, game: Game) -> int: ...
    def insert_gameversion(self, gv: Gameversion) -> int: ...
    def insert_rom(self, rom: Rom) -> int: ...
    def finalize(self) -> None: ...


def _read_schema_sql() -> str:
    schema_path = os.path.join(os.path.dirname(__file__), "dbschema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        return f.read()


class SQLiteBackend:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None

    def initialize(self) -> None:
        self._conn = sqlite3.connect(self._db_path)
        ddl = _read_schema_sql()
        ddl = re.sub(
            r"serial primary key",
            "integer primary key autoincrement",
            ddl,
            flags=re.IGNORECASE,
        )
        self._conn.executescript(ddl)

    def _cursor(self) -> sqlite3.Cursor:
        assert self._conn is not None
        return self._conn.cursor()

    def insert_platform(self, platform: Platform) -> int:
        cur = self._cursor()
        cur.execute(
            "INSERT INTO platform (name, short_name, format) VALUES (?, ?, ?)",
            (platform.name, platform.short_name, platform.format),
        )
        return cur.lastrowid  # type: ignore[return-value]

    def insert_game(self, game: Game) -> int:
        cur = self._cursor()
        cur.execute(
            "INSERT INTO game (name, date, publisher) VALUES (?, ?, ?)",
            (game.name, game.date, game.publisher),
        )
        return cur.lastrowid  # type: ignore[return-value]

    def insert_gameversion(self, gv: Gameversion) -> int:
        cur = self._cursor()
        cur.execute(
            """INSERT INTO gameversion (
                name, demo, system, video, country, language, dev_status,
                media, copyright, cracked, fixed, hacked, modified, pirated,
                trained, translated, overdumped, underdumped, virus, baddump,
                alternate, verified, platform_id, game_id, rom_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                gv.name,
                gv.demo,
                gv.system,
                gv.video,
                gv.country,
                gv.language,
                gv.dev_status,
                gv.media,
                gv.copyright,
                gv.cracked,
                gv.fixed,
                gv.hacked,
                gv.modified,
                gv.pirated,
                gv.trained,
                gv.translated,
                gv.overdumped,
                gv.underdumped,
                gv.virus,
                gv.baddump,
                gv.alternate,
                gv.verified,
                gv.platform_id,
                gv.game_id,
                gv.rom_count,
            ),
        )
        return cur.lastrowid  # type: ignore[return-value]

    def insert_rom(self, rom: Rom) -> int:
        cur = self._cursor()
        cur.execute(
            "INSERT INTO rom (name, gameversion_id, size, crc32, md5, sha1) VALUES (?, ?, ?, ?, ?, ?)",
            (rom.name, rom.gameversion_id, rom.size, rom.crc32, rom.md5, rom.sha1),
        )
        return cur.lastrowid  # type: ignore[return-value]

    def finalize(self) -> None:
        if self._conn is not None:
            self._conn.commit()
            self._conn.close()


class PostgreSQLBackend:
    def __init__(self, host: str, port: int, user: str, password: str, dbname: str):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._dbname = dbname
        self._conn = None

    def initialize(self) -> None:
        try:
            import psycopg
        except ImportError:
            raise RuntimeError(
                "psycopg is required for PostgreSQL support. "
                "Install it with: pip install 'tosecdb[postgresql]'"
            )
        self._conn = psycopg.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            dbname=self._dbname,
        )
        ddl = _read_schema_sql()
        self._conn.execute(ddl)

    def _execute_returning(self, query: str, params: tuple) -> int:
        assert self._conn is not None
        cur = self._conn.execute(query, params)
        row = cur.fetchone()
        assert row is not None
        return row[0]

    def insert_platform(self, platform: Platform) -> int:
        return self._execute_returning(
            "INSERT INTO platform (name, short_name, format) VALUES (%s, %s, %s) RETURNING id",
            (platform.name, platform.short_name, platform.format),
        )

    def insert_game(self, game: Game) -> int:
        return self._execute_returning(
            "INSERT INTO game (name, date, publisher) VALUES (%s, %s, %s) RETURNING id",
            (game.name, game.date, game.publisher),
        )

    def insert_gameversion(self, gv: Gameversion) -> int:
        return self._execute_returning(
            """INSERT INTO gameversion (
                name, demo, system, video, country, language, dev_status,
                media, copyright, cracked, fixed, hacked, modified, pirated,
                trained, translated, overdumped, underdumped, virus, baddump,
                alternate, verified, platform_id, game_id, rom_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id""",
            (
                gv.name,
                gv.demo,
                gv.system,
                gv.video,
                gv.country,
                gv.language,
                gv.dev_status,
                gv.media,
                gv.copyright,
                gv.cracked,
                gv.fixed,
                gv.hacked,
                gv.modified,
                gv.pirated,
                gv.trained,
                gv.translated,
                gv.overdumped,
                gv.underdumped,
                gv.virus,
                gv.baddump,
                gv.alternate,
                gv.verified,
                gv.platform_id,
                gv.game_id,
                gv.rom_count,
            ),
        )

    def insert_rom(self, rom: Rom) -> int:
        return self._execute_returning(
            "INSERT INTO rom (name, gameversion_id, size, crc32, md5, sha1) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (rom.name, rom.gameversion_id, rom.size, rom.crc32, rom.md5, rom.sha1),
        )

    def finalize(self) -> None:
        if self._conn is not None:
            self._conn.commit()
            self._conn.close()
