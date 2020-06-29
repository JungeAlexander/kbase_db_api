import csv
from datetime import date, datetime
import os
from pprint import pprint
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article
from db_api.database import global_init, session_scope


def main():
    # TODO work with one example file
    # TODO make references a self-reference? https://docs.sqlalchemy.org/en/13/orm/self_referential.html
    # TODO model tags in DB?
    # TODO handle delete citations
    pass


if __name__ == "__main__":
    main()
