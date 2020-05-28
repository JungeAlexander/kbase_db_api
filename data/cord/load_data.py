import csv
from datetime import date, datetime
import os
from pprint import pprint
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article


def main():
    with open("metadata.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # pprint(row)
            article = Article()
            article.id = "CORD:" + row["cord_uid"]
            article.version = "v1"
            article.source = "CORD"
            article.title = row["title"]
            article.publication_date = date.fromisoformat(row["publish_time"])
            article.update_date = date.today()
            article.modified_date = date.now()
            article.link = row["url"]
            article.pmid = row["pubmed_id"]
            article.doid = row["doi"]
            article.summary = row["abstract"]
            article.authors = [x.strip() for x in row["authors"].split(";")]
            # TODO test for whole file
            # TODO load into database


if __name__ == "__main__":
    main()
