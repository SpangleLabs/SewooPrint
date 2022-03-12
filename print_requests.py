import json
from abc import ABC, abstractmethod
from typing import Dict

import requests

from document import TextDocument, ConcatDocument
from document_image import WifiQRCode
from document_web import ChoresBoardDocument, SnuppsShelfDocument, NotionViewDocument
from printer import Printer


class Request(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def matches_input(self, user_input: str) -> bool:
        pass

    @abstractmethod
    def print(self, printer: Printer):
        pass


class PartialRequest(Request, ABC):

    @abstractmethod
    def get_more_info(self):
        pass


class TechSupportOathRequest(Request):

    @property
    def name(self) -> str:
        return "Tech support oath"

    def matches_input(self, user_input: str) -> bool:
        return user_input in ['tech support oath', 'techsupportoath', 'oath']

    def print(self, printer: Printer):
        """
        Recites the tech support oath.
        Parody of the Night's Watch oath.
        """
        output = """\
User issues gather, and now my watch begins.
It shall not end until my death.
I shall take no wife (that I will ever see except on weekends),
hold no lands (because I don't make nearly enough),
father no children (because I will never be home anyway).
I shall receive no thanks and win no glory.
I shall live and die at my desk.
I am the antivirus in the darkness.
I am the coder on the walls.
I am the password reset that guards the logins of men.
I pledge my life and honor to the Help Desk's Watch,
for this night and all the nights to come."""
        document = TextDocument().add_title("Tech support oath")
        document.add_line_wrapped_text(output)
        printer.print_document(document)


class NotMyBusinessRequest(Request):

    @property
    def name(self) -> str:
        return "Not My Business"

    def matches_input(self, user_input: str) -> bool:
        return user_input in ['not my business', 'notmybusiness']

    def print(self, printer: Printer):
        """
        Outputs Niyi Osundere's "Not my business"
        """
        poem = """ \
They picked Akanni up one morning
Beat him soft like clay
And stuffed him down the belly
Of a waiting jeep.
What business of mine is it
So long they don't take the yam
From my savouring mouth?
        
They came one night
Booted the whole house awake
And dragged Danladi out,
Then off to a lengthy absence.
What business of mine is it
So long they don't take the yam
From my savouring mouth?

Chinwe went to work one day
Only to find her job was gone:
No query, no warning, no probe -
Just one neat sack for a stainless record.
What business of mine is it
So long they don't take the yam
From my savouring mouth?

And then one evening
As I sat down to eat my yam
A knock on the door froze my hungry hand.
The jeep was waiting on my bewildered lawn
Waiting, waiting in its usual silence."""
        document = TextDocument().add_title("Not My Business")
        document.add_title("by Niyi Osundere")
        document.add_line_wrapped_text(poem)
        printer.print_document(document)


class HAL9000WarningRequest(Request):

    @property
    def name(self) -> str:
        return "HAL9000 warning"

    def matches_input(self, user_input: str) -> bool:
        return user_input in ['hal9000 warning', 'hal warning', 'hal', 'hal9000', 'hal 9000', 'europa warning']

    def print(self, printer: Printer):
        """
        Outputs HAL9000's warning from the end of 2010:Odyssey Two
        """
        document = TextDocument()\
            .add_bold_centered_text("ALL THESE WORLDS ARE YOURS-EXCEPT EUROPA").nl()\
            .add_bold_centered_text("ATTEMPT NO LANDING THERE")
        printer.print_document(document)


class RawTextRequest(Request):

    def __init__(self):
        self.text = None

    @property
    def name(self) -> str:
        return "raw"

    def matches_input(self, user_input: str) -> bool:
        if user_input.startswith("raw"):
            self.text = user_input[3:].strip(" :")
            return True
        return False

    def print(self, printer: Printer):
        document = TextDocument().add_text(self.text)
        printer.print_document(document)


class ChoresBoardRequest(Request):

    @property
    def name(self) -> str:
        return "Chores board"

    def matches_input(self, user_input: str) -> bool:
        return user_input in ['chores board', 'chores', 'choresboard', 'chores list']

    def print(self, printer: Printer):
        chores_document = ChoresBoardDocument()
        printer.print_document(chores_document)


class WifiQRCodeRequest(Request):

    @property
    def name(self) -> str:
        return "WIFI QR code"

    def matches_input(self, user_input: str) -> bool:
        return user_input in ["wifi", "wifi qr code", "wifi code", "wifi password", "wifi info"]

    def print(self, printer: Printer):
        with open("config_wifi.json", "r") as f:
            config = json.load(f)
        if not isinstance(config, list):
            config = [config]
        for wifi_network in config:
            qr_document = WifiQRCode(
                wifi_network["SSID"],
                wifi_network["password"],
                auth_type=wifi_network["auth_type"]
            )
            printer.print_document(qr_document)


class MenuRequest(Request):

    def __init__(self, other_requests):
        self.all_request_names = [r.name for r in other_requests]
        self.all_request_names.append(self.name)

    @property
    def name(self) -> str:
        return "Menu"

    def matches_input(self, user_input: str) -> bool:
        return user_input in [
            "menu", "print menu", "list of requests", "possible print requests", "things i can print"
        ]

    def print(self, printer: Printer):
        doc = TextDocument().add_title("Print menu")
        for request_name in self.all_request_names:
            doc.add_text(request_name).nl()
        printer.print_document(doc)


class NotionWishlistRequest(Request):

    @property
    def name(self) -> str:
        return "Retro wishlists"

    def matches_input(self, user_input: str) -> bool:
        return user_input in [
            "notion", "notion wishlists", "notion wishlist", "nintendo wishlists", "nintendo wishlist",
            "retro wishlists", "retro wishlist"
        ]

    def print(self, printer: Printer):
        with open("config_notion.json", "r") as f:
            config = json.load(f)
        database_docs = []
        for database_conf in config["databases"]:
            database_docs.append(self.notion_db_document(config['token'], database_conf))
        notion_doc = ConcatDocument(database_docs)
        printer.print_document(notion_doc)

    def notion_db_document(self, token: str, db_conf: Dict) -> NotionViewDocument:
        database = requests.get(
            f"https://api.notion.com/v1/databases/{db_conf['id']}",
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": "2022-02-22"
            }
        ).json()
        title = database["title"][0]["text"]["content"]
        post_data = {}
        if "filter" in db_conf:
            post_data["filter"] = db_conf["filter"]
        cards_data = requests.post(
            f"https://api.notion.com/v1/databases/{db_conf['id']}/query",
            headers={
                "Authorization": f"Bearer {token}",
                "Notion-Version": "2022-02-22"
            },
            json=post_data
        ).json()
        card_names = []
        for card in cards_data["results"]:
            line = card["properties"]["Name"]["title"][0]["text"]["content"]
            if "append_property" in db_conf:
                if card["properties"][db_conf["append_property"]]["type"] == "multi_select":
                    values = ", ".join(x["name"] for x in card["properties"][db_conf["append_property"]]["multi_select"])
                    if values:
                        line += f" ({values})"
            card_names.append(line)
        return NotionViewDocument(title, card_names, extra_spacing=True)
