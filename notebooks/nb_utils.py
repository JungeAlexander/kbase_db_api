from requests import api
import spacy
from spacy import displacy

import requests


def get_matches(
    doc_json, match_source, document_section="title", api_url="http://127.0.0.1:8000"
):
    start_end_labels = []
    for ent in doc_json["entities"]:
        if ent["document_section"] != document_section or ent["source"] != match_source:
            continue
        # print(ent)
        ent_req = requests.get(f"{api_url}/entities/{ent['entity_id']}")
        ent_json = ent_req.json()
        start = ent["start_char"]
        end = ent["end_char"]
        label = ent_json["entity_type"]
        start_end_labels.append([start, end, label])
        start_end_labels = sorted(start_end_labels, key=lambda x: x[0])
    return start_end_labels


def display_matches(text, labels, title):
    colors = {
        "DISEASE": "linear-gradient(90deg, #999999, #cccccc)",
        "GGP": "linear-gradient(90deg, #9999ff, #9999bb)",
    }
    options = {"ents": ["DISEASE", "GGP"], "colors": colors}
    ex = [
        {
            "text": text,
            "ents": [{"start": x[0], "end": x[1], "label": x[2]} for x in labels],
            "title": title,
        }
    ]
    html = displacy.render(ex, style="ent", manual=True, options=options)
    return html
