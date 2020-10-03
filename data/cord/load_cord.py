import csv
import os
import sys
from datetime import date, datetime
from pathlib import Path
from pprint import pprint

import boto3
import typer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.database import global_init, session_scope
from db_api.models import Article


def main(
    cord_metadata_file: Path,
    start_date: datetime = "1900-01-01",
    s3: bool = False,
    psql: bool = True,
):
    global_init()
    s3_client = boto3.client("s3")
    with open(cord_metadata_file, newline="") as csvfile, session_scope() as sess:
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
            article.doi = row.get("doi", "")
            article.summary = row.get("abstract", "")
            article.full_text = ""
            article.authors = [x.strip() for x in row["authors"].split(";")]
            article.affiliations = []
            article.language = ""
            article.keywords = []
            article.references = []
            article.tags = []
            if (
                publish_date_parsed
                and datetime.combine(publish_date_parsed, datetime.min.time())
                > start_date
            ):
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
    typer.run(main)
