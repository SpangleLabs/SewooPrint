import json

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
        chores_data = requests.get(chores_url).json()
        self.add_title("Chores board")
        self.add_bold_text("Date: ").add_text(chores_data['today']).nl()
        for category in chores_data['chores']:
            self.add_bold_centered_text(category).nl()
            for chore in chores_data['chores'][category]:
                self.add_bold_text(chore['display_name']).nl()
                # Add latest done date, invert if over two months
                self.add_bold_text("Last done: ")
                if chore['latest_done'] is None:
                    self.add_invert_colours_text("-")
                else:
                    days = isodate.parse_date(chores_data['today']) - isodate.parse_date(chore['latest_done'])
                    if days.days > 60 and chore['recommended_period'] is None:
                        self.add_invert_colours_text(chore['latest_done']).nl()
                    else:
                        self.add_text(chore['latest_done']).nl()
                # Add next date, invert if overdue
                self.add_bold_text("Next date: ")
                if chore['is_overdue']:
                    self.add_invert_colours_text(chore['next_date']).nl()
                else:
                    self.add_text(chore['next_date']).nl()
                self.nl()
