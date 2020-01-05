import json

import flask
from flask import request, abort

from printer_repo import PrinterRepo
from print_requests import TechSupportOathRequest, NotMyBusinessRequest, HAL9000WarningRequest, RawTextRequest, \
    ChoresBoardRequest, WifiQRCodeRequest

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
        ChoresBoardRequest(), WifiQRCodeRequest()
    ]
    printer = PrinterRepo().default_printer()
    for req in requests:
        if req.matches_input(doc):
            print(f"Printing {req.name}")
            req.print(printer)
    return f"Unknown document {doc}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8903)
