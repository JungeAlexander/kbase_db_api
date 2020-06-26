import csv
from datetime import date, datetime
import os
from pprint import pprint
import sys


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article
from db_api.database import global_init, session_scope


def main():
    pass


if __name__ == "__main__":
    main()
