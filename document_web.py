import json
from typing import List, Dict, Optional

import isodate
import requests

from document import TextDocument


class ChoresBoardDocument(TextDocument):

    def __init__(self):
        super().__init__()
        with open("config.json", "r") as f:
            config = json.load(f)
        dailys_url = config['dailys_url']
        chores_url = f"{dailys_url}/views/chores_board.json"
        self.chores_data = requests.get(chores_url).json()
        self.add_title("Chores board")
        self.add_bold_text("Date: ").add_text(self.chores_data['today']).nl()
        for category, chores_list in self.chores_data['chores'].items():
            self._add_category(category, chores_list)

    def _add_category(self, category: str, chores_list: List[Dict[str, Optional[str]]]):
        self.add_bold_centered_text(category.capitalize()).nl()
        for chore in chores_list:
            self._add_chore(chore)

    def _add_chore(self, chore: Dict[str, Optional[str]]):
        self.add_bold_text(chore['display_name']).nl()
        # Add latest done date, invert if over two months
        self.add_bold_text("Last done: ")
        if chore['latest_done'] is None:
            self.add_invert_colours_text("None").nl()
        else:
            days = isodate.parse_date(self.chores_data['today']) - isodate.parse_date(chore['latest_done'])
            if days.days > 60 and chore['recommended_period'] is None:
                self.add_invert_colours_text(chore['latest_done']).nl()
            else:
                self.add_text(chore['latest_done']).nl()
        # Add next date, invert if overdue
        if chore['recommended_period'] is not None:
            self.add_bold_text("Next date: ")
            if chore['is_overdue']:
                self.add_invert_colours_text(chore['next_date']).nl()
            else:
                self.add_text(chore['next_date']).nl()
        # Spacing line
        self.nl()


class SnuppsShelfDocument(TextDocument):

    def __init__(self, shelf_data, extra_spacing = False):
        super().__init__()
        self.add_title(shelf_data["name"])
        for item in shelf_data["items"]:
            self.add_text("__").add_text(item["title"]).nl()
            if extra_spacing:
                self.nl()


class ShoppingListDocument(TextDocument):
    DEFAULT_NAME = "default"

    def __init__(self, shops):
        super().__init__()
        self.add_title("Shopping list")
        for shop_name, items in shops.items():
            if shop_name != self.DEFAULT_NAME:
                self.nl()
                self.add_bold_centered_text(shop_name)
            for item in items:
                self.add_text("__").add_text(item["name"]).nl()
                if "comment" in item:
                    self.add_text("- (").add_text(item["comment"]).add_text(")").nl()
