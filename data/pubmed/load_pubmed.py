import csv
from datetime import date, datetime
import os
from pprint import pprint
import sys

import pubmed_parser as pp


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article
from db_api.database import global_init, session_scope


def main(psql=False):
    global_init()
    input_file_path = "pubmed20n0477.xml.gz"

    article_dicts = pp.parse_medline_xml(
        input_file_path, year_info_only=False, author_list=True, reference_list=True
    )

    # with session_scope as sess:
    #     pass

    # TODO make references a self-reference? https://docs.sqlalchemy.org/en/13/orm/self_referential.html
    # TODO model tags in DB?
    # TODO handle delete citations
    # TODO make sure newest is always used first
    pass


if __name__ == "__main__":
    main()
