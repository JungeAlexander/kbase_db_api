import csv
from datetime import date, datetime
import os
from pprint import pprint
import sys

import boto3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article
from db_api.database import global_init, session_scope


def main(start_date, s3=False, psql=True):
    global_init()
    s3_client = boto3.client('s3')
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
            article.journal = row.get("journal", "")
            article.article_type = "preprint"
            article.title = row.get("title", "")
            publish_date = row.get("publish_time", "")
            publish_date_parsed = None
            try:
                publish_date_parsed = date.fromisoformat(publish_date)
                article.publication_date = publish_date_parsed
            except ValueError:
                article.publication_date = ""
            article.update_date = date.today()
            article.modified_date = datetime.now()
            article.link = row.get("url", "")
            pmid = row["pubmed_id"]
            try:
                article.pmid = int(pmid)
            except ValueError:
                article.pmid = 0
            article.doid = row.get("doi", "")
            article.summary = row.get("abstract", "")
            article.full_text = ""
            article.authors = [x.strip() for x in row["authors"].split(";")]
            article.affiliations = []
            article.language = ""
            article.keywords = []
            article.references = []
            if publish_date_parsed and publish_date_parsed > start_date:
                if s3:
                    fname = f"{article.id}.tsv"
                    with open(fname, "w") as f:
                        f.write(article.id)
                        f.write(os.linesep)
                        f.write(article.title)
                        f.write(os.linesep)
                        f.write(article.summary)
                    s3_client.upload_file(fname, "kendra-kbase-ajs-aws", fname)
                    os.remove(fname)
                if psql:
                    sess.add(article)


if __name__ == "__main__":
    main(start_date=date.fromisoformat("2020-01-01"))
