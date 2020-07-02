from datetime import date, datetime
import logging
import os
import sys

import pubmed_parser as pp


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from db_api.models import Article
from db_api.database import global_init, session_scope


logging.basicConfig(level=logging.INFO)


def main(psql=True):
    input_file_path = "data/pubmed/pubmed20n0340.xml.gz"

    logging.info(f"Processing articles from {input_file_path}.")
    article_dicts = pp.parse_medline_xml(
        input_file_path, year_info_only=False, author_list=False, reference_list=True
    )
    logging.info(f"Loaded articles from {input_file_path}.")

    global_init()
    with session_scope() as sess:
        for ad in article_dicts:
            logging.info(f"Processing article {ad['pmid']}.")
            article = Article()
            article.id = "PMID:" + ad["pmid"]
            article.version = "v1"
            article.source = "PubMed"
            article.journal = ad["journal"]
            article.article_type = "postprint"
            article.title = ad["title"]
            pubdate = ad["pubdate"]
            pubdate_dashes = pubdate.count("-")
            if pubdate_dashes == 2:  # format of parsed pubdate is YYYY-MM-DD
                article.publication_date = date.fromisoformat(pubdate)
            elif pubdate_dashes == 1:  # format of parsed pubdate is YYYY-MM
                article.publication_date = date.fromisoformat(pubdate + "-01")
            else:  # format of parsed pubdate is YYYY
                article.publication_date = date.fromisoformat(pubdate + "-01-01")
            article.update_date = date.today()
            article.modified_date = datetime.now()
            article.link = "https://pubmed.ncbi.nlm.nih.gov/" + ad["pmid"]
            article.pmid = ad["pmid"]
            article.doi = ad["doi"]
            article.summary = ad["abstract"]
            article.full_text = ""
            article.authors = [x.strip() for x in ad["authors"].split(";") if x != ""]
            article.affiliations = [ad["affiliations"]]
            article.language = ""
            article.keywords = [x.strip() for x in ad["keywords"].split(";") if x != ""]
            article.references = ad["references"]
            article.tags = [
                x.strip()
                for k in ["mesh_terms", "publication_types", "chemical_list"]
                for x in ad[k].split(";")
                if x != ""
            ]
            if psql:
                sess.add(article)

    # TODO make references a self-reference? https://docs.sqlalchemy.org/en/13/orm/self_referential.html
    # TODO model tags in DB tables?
    # TODO handle delete citations
    # TODO make sure newest is always used first


if __name__ == "__main__":
    main()
