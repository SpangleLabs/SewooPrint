import json
import re
from collections import defaultdict

import flask
from flask import request, abort

from document_web import ShoppingListDocument
from printer_repo import PrinterRepo
from print_requests import TechSupportOathRequest, NotMyBusinessRequest, HAL9000WarningRequest, RawTextRequest, \
    ChoresBoardRequest, WifiQRCodeRequest, SnuppsWishlistRequest, MenuRequest

app = flask.Flask(__name__)

with open("config.json", "r") as f:
    CONFIG = json.load(f)


@app.route("/")
def hello_world():
    return "Hello, this is the printer server."


@app.route("/", methods=["POST"])
def print_doc():
    data = request.json
    if 'key' not in data or data['key'] != CONFIG['web_key']:
        abort(401)
        return
    doc = data['document'].strip().lower()
    print(f"Print requested for document: {doc}")
    if doc.startswith("the "):
        doc = doc[4:]
    if doc.startswith("my "):
        doc = doc[3:]
    requests = [
        TechSupportOathRequest(), NotMyBusinessRequest(), HAL9000WarningRequest(), RawTextRequest(),
        ChoresBoardRequest(), WifiQRCodeRequest(), SnuppsWishlistRequest()
    ]
    requests.append(MenuRequest(requests))
    printer = PrinterRepo().default_printer()
    for req in requests:
        if req.matches_input(doc):
            print(f"Printing {req.name}")
            req.print(printer)
    return f"Unknown document {doc}"


@app.route("/shopping_list")
def shopping_list_form():
    return """
<html>
<head>
<title>Shopping list form</title>
</head>
<body>
Please enter your shopping list below. Items on each line, comments in brackets, and shop categories as markdown header's, 
starting with #
<form method="post" action="/shopping_list">
<textarea name="shopping_list" rows="30" cols="50">
</textarea>
<input type="submit" value="Print!" />
</form>
</html>
"""


@app.route("/shopping_list", methods=["POST"])
def process_shopping_list():
    text = request.form["shopping_list"]
    comment_regex = re.compile(r"\(([^)]+)\)$", re.IGNORECASE)
    shops = defaultdict(list)
    current_shop = ShoppingListDocument.DEFAULT_NAME
    for line in text.split("\n"):
        line_clean = line.strip()
        if not line_clean:
            continue
        if line_clean.startswith("#"):
            current_shop = line[1:]
            continue
        brackets_match = comment_regex.search(line_clean)
        if brackets_match:
            brackets_text = brackets_match.group(1)
            item_name = line_clean[:-len(brackets_match.group(0))].strip()
            item = {
                "name": item_name,
                "comment": brackets_text
            }
        else:
            item = {
                "name": line_clean
            }
        shops[current_shop].append(item)
    printer = PrinterRepo().default_printer()
    doc = ShoppingListDocument(shops)
    printer.print_document(doc)
    return "Printing shopping list now: <pre>" + json.dumps(shops, indent=2) + "</pre>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8903)
