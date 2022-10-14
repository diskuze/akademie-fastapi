import os.path

from sqlalchemy import create_mock_engine

from diskuze.models import Base

DUMP_FILE = os.path.join(os.path.dirname(__file__),  "db.sql")


def metadata_dump(sql, *multiparams, **params):
    with open(DUMP_FILE, "a") as dump_file:
        compiled = sql.compile(dialect=engine.dialect)
        dump_file.write("{};\n\n".format(str(compiled).strip()))


if __name__ == '__main__':
    if os.path.exists(DUMP_FILE):
        os.remove(DUMP_FILE)

    engine = create_mock_engine('mysql://', executor=metadata_dump)
    Base.metadata.create_all(engine)

    print(f"Generated create schema script to {DUMP_FILE}")
