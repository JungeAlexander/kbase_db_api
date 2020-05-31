import csv
from datetime import date, datetime
import os
from pprint import pprint
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article
from db_api.database import global_init, session_scope


def main(start_date):
    global_init()
    with open("metadata.csv", newline="") as csvfile, session_scope() as sess:
        reader = csv.DictReader(csvfile)
        ids_added = set()
        for i, row in enumerate(reader):
            # pprint(row)
            article = Article()
            cord_id = "CORD:" + row["cord_uid"]
            # CORD contains duplicated UIDs, skip these
            if cord_id in ids_added:
                continue
            else:
                ids_added.add(cord_id)
            article.id = cord_id
            article.version = "v1"
            article.source = "CORD"
            article.title = row["title"]
            publish_date = row["publish_time"]
            publish_date_parsed = None
            try:
                publish_date_parsed = date.fromisoformat(publish_date)
                article.publication_date = publish_date_parsed
            except ValueError:
                pass
            article.update_date = date.today()
            article.modified_date = datetime.now()
            article.link = row["url"]
            pmid = row["pubmed_id"]
            try:
                article.pmid = int(pmid)
            except ValueError:
                pass
            article.doid = row["doi"]
            article.summary = row["abstract"]
            article.authors = [x.strip() for x in row["authors"].split(";")]
            if publish_date_parsed and publish_date_parsed > start_date:
                sess.add(article)


if __name__ == "__main__":
    main(start_date=date.fromisoformat("2020-01-01"))
