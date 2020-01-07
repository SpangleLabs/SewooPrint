from abc import ABC
from enum import Enum


def _try_encode(text):
    """Tries to encode string to bytes, unless it is already bytes."""
    if isinstance(text, bytes):
        return text
    try:
        text_encode = str(text).encode().replace(b'\xc2\xa3', b'\x9c')
        return text_encode
    except AttributeError:
        return text


def _center_text(text):
    """Centres text on the page."""
    spacing_left = (TextDocument.MAX_LINE_LEN - len(text)) // 2
    spacing_right = TextDocument.MAX_LINE_LEN - len(text) - spacing_left
    centre_text = ' ' * spacing_left + text + ' ' * spacing_right
    return centre_text


class Document(ABC):

    def __init__(self):
        self.encoded = b""
        self.has_cut = False

    def get_encoded(self):
        return self.encoded

    def cut(self):
        self.encoded += b'\n\n\n\n\n\n\x1d\x56\x01\n'
        self.has_cut = True
        return self

    def cut_if_uncut(self):
        if not self.has_cut:
            self.cut()
        return self


class TextDocument(Document):
    MAX_LINE_LEN = 42

    def __init__(self):
        super().__init__()

    def add_line_wrapped_text(self, text):
        """
        Formats text to be printed over multiple lines, breaking at spaces.
        """
        text_lines = []
        for input_line in text.split("\n"):
            line = ""
            for word in input_line.split():
                temp = line + " " + word
                temp = temp.strip()
                if len(temp) > self.MAX_LINE_LEN:
                    text_lines.append(line)
                    line = word
                else:
                    line = temp
            text_lines.append(line)
        self.encoded += _try_encode("\n".join(text_lines))
        return self

    def nl(self):
        self.encoded += b"\n"
        return self

    def add_text(self, text):
        self.encoded += _try_encode(text)
        return self

    def add_bold_text(self, text):
        """Makes a set string bold."""
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x21\x08' + text_encode + b'\x1b\x21\x00'
        return self

    def add_bold_centered_text(self, text):
        centered_text = _center_text(text)
        return self.add_bold_text(centered_text)

    def add_invert_colours_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1d\x42\x01' + text_encode + b'\x1d\x42\x00'
        return self

    def add_underlined_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x2d\x01' + text_encode + b'\x1b\x2d\x00'
        return self

    def add_title(self, text):
        """Formats a given string as a title."""
        self.add_invert_colours_text(_center_text(text))
        return self

    def add_text_with_control_code(self, text, control_code):
        self.encoded += b'\x1b\x21' + chr(control_code).encode() + text.encode() + b'\x1b\x21\x00\n'
        return self

    def add_text_rotated_sideways(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x56\x01' + text_encode + b'\x1b\x56\x00'
        return self

    def add_upside_down_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x7b\x01' + text_encode + b'\x1b\x7b\x00'
        return self

    def add_stretched_text(self, text, amount=2):
        text_encode = _try_encode(text)
        amount = min(amount, 8)
        self.encoded += b'\x1d\x21' + chr(amount - 1).encode() + text_encode + b'\x1d\x21\x00'
        return self

    def add_tiny_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x21\x01' + text_encode + b'\x1b\x21\x00'
        return self

    def add_tiny_bold_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x21\x09' + text_encode + b'\x1b\x21\x00'
        return self

    def add_dashed_line(self):
        self.encoded += _try_encode("-" * TextDocument.MAX_LINE_LEN)
        return self

    def add_left_right_text(
            self, left_text, right_text, width=None,
            left_func=False, right_func=False
    ):
        if width is None:
            width = TextDocument.MAX_LINE_LEN
        spacing = width - len(left_text + right_text)
        if not left_func:
            left_func = self.add_text
        if not right_func:
            right_func = self.add_text
        left_func(left_text)
        self.add_text(" " * spacing)
        right_func(right_text)
        self.nl()
        return self

    def add_price(self, price):
        text = "%.2f" % price
        text_encode = b'\x9c' + _try_encode(text)
        self.encoded += text_encode
        return self

    def add_number(self, number):
        text = str(number)
        if "." in text:
            text = text.rstrip("0.")
        text_encode = _try_encode(text)
        self.encoded += text_encode
        return self

    def add_columns(self, column_spec, column_text):
        first = True
        for (spec, text) in zip(column_spec.columns, column_text):
            if not first:
                self.add_text(" ")
            first = False
            add_func = self.add_text
            if isinstance(text, tuple):
                add_func = text[1]
                text = text[0]
            if spec.align == ColumnAlign.left:
                text = text[:spec.width].ljust(spec.width)
                add_func(text)
            else:
                text = text[-spec.width:].rjust(spec.width)
                add_func(text)
        self.nl()


class ColumnsSpec:

    def __init__(self, columns):
        fill_columns = [x for x in columns if x.width is None]
        if len(fill_columns) > 1:
            raise ValueError("Can't have more than 1 column width set to None")
        if len(fill_columns) == 1:
            fixed_width_total = \
                sum([x.width for x in columns if x.width is not None]) + len(columns) - 1
            remaining_width = TextDocument.MAX_LINE_LEN - fixed_width_total
            fill_columns[0].width = remaining_width
        self.columns = columns


class ConcatDocument(Document):

    def __init__(self, documents):
        super().__init__()
        self.encoded = b"".join(document.encoded for document in documents)


class ColumnAlign(Enum):
    left = 1
    right = 2


class ColumnSpec:

    def __init__(self, width, align):
        self.width = width
        self.align = align
