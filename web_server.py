import json

import flask
from flask import request, abort

from document_web import ChoresBoardDocument
from printer_repo import PrinterRepo

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
    doc = data['document'].strip()
    print(f"Print requested for document: {doc}")
    if doc.startswith("the "):
        doc = doc[4:]
    if doc.startswith("my "):
        doc = doc[3:]
    if doc in ['chores board', 'chores', 'choresboard', 'chores list']:
        printer = PrinterRepo().default_printer()
        chores_doc = ChoresBoardDocument()
        printer.print_document(chores_doc)
        return "Printed chores document"
    return f"Unknown document {doc}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8903)
