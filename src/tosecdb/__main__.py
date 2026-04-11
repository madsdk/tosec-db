import argparse

from .backends import PostgreSQLBackend, SQLiteBackend
from .importer import import_datfile


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tosecdb",
        description="Import TOSEC datfiles into a database.",
    )
    parser.add_argument("datfiles", nargs="+", help="Path(s) to TOSEC .dat file(s) to import")
    parser.add_argument(
        "--db-type",
        required=True,
        choices=["sqlite", "postgresql"],
        help="Database backend to use",
    )

    # SQLite options
    parser.add_argument(
        "--db-path", help="Path to SQLite database file (required for sqlite)"
    )

    # PostgreSQL options
    parser.add_argument("--host", help="PostgreSQL host (required for postgresql)")
    parser.add_argument(
        "--port", type=int, default=5432, help="PostgreSQL port (default: 5432)"
    )
    parser.add_argument("--user", help="PostgreSQL user (required for postgresql)")
    parser.add_argument("--password", default="", help="PostgreSQL password")
    parser.add_argument(
        "--dbname", help="PostgreSQL database name (required for postgresql)"
    )

    args = parser.parse_args()

    if args.db_type == "sqlite":
        if not args.db_path:
            parser.error("--db-path is required when using --db-type sqlite")
        backend = SQLiteBackend(args.db_path)
    elif args.db_type == "postgresql":
        missing = []
        if not args.host:
            missing.append("--host")
        if not args.user:
            missing.append("--user")
        if not args.dbname:
            missing.append("--dbname")
        if missing:
            parser.error(
                f"{', '.join(missing)} required when using --db-type postgresql"
            )
        backend = PostgreSQLBackend(
            host=args.host,
            port=args.port,
            user=args.user,
            password=args.password,
            dbname=args.dbname,
        )

    backend.initialize()  # type: ignore[union-attr]
    for datfile in args.datfiles:
        import_datfile(datfile, backend)  # type: ignore[possibly-undefined]
    backend.finalize()  # type: ignore[union-attr]


if __name__ == "__main__":
    main()
