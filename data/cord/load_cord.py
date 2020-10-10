import csv
import os
import sys
from datetime import date, datetime
from pathlib import Path

import boto3
import typer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.database import global_init, session_scope
from db_api.models import Document


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
            document = Document()
            cord_id = "CORD:" + row["cord_uid"]
            # CORD contains duplicated UIDs, skip these
            if cord_id in ids_added:
                continue
            else:
                ids_added.add(cord_id)
            document.id = cord_id
            document.version = "v1"
            document.source = "CORD"
            document.journal = row.get("journal", "")
            document.document_type = "preprint"
            document.title = row.get("title", "")
            publish_date = row.get("publish_time", "")
            publish_date_parsed = None
            try:
                publish_date_parsed = date.fromisoformat(publish_date)
                document.publication_date = publish_date_parsed
            except ValueError:
                document.publication_date = ""
            document.update_date = date.today()
            document.modified_date = datetime.now()
            document.urls = [x.strip() for x in row.get("url", "").split(";")]
            pmid = row["pubmed_id"]
            try:
                document.pmid = int(pmid)
            except ValueError:
                document.pmid = 0
            document.doi = row.get("doi", "")
            document.arxiv_id = row.get("arxiv_id", "")
            document.summary = row.get("abstract", "")
            document.license = row.get("license", "")
            document.full_text = ""
            document.authors = [x.strip() for x in row["authors"].split(";")]
            document.affiliations = []
            document.language = ""
            document.keywords = []
            document.in_citations = []
            document.out_citations = []
            document.tags = []
            other_ids = []
            if "pmcid" in row and row["pmcid"].strip() != "":
                pmcid = row["pmcid"]
                if not pmcid.startswith("PMC"):
                    pmcid = "PMC" + pmcid
                other_ids.append(pmcid)
            if "who_covidence_id" in row and row["who_covidence_id"].strip() != "":
                other_ids.append("WHO" + row["who_covidence_id"])
            if "s2_id" in row and row["s2_id"].strip() != "":
                other_ids.append("S2" + row["s2_id"])
            document.other_ids = sorted(other_ids)
            if (
                publish_date_parsed
                and datetime.combine(publish_date_parsed, datetime.min.time())
                > start_date
            ):
                if s3:
                    fname = f"{document.id}.tsv"
                    with open(fname, "w") as f:
                        f.write(document.id)
                        f.write(os.linesep)
                        f.write(document.title)
                        f.write(os.linesep)
                        f.write(document.summary)
                    s3_client.upload_file(fname, "kendra-kbase-ajs-aws", fname)
                    os.remove(fname)
                if psql:
                    sess.add(document)


if __name__ == "__main__":
    typer.run(main)
