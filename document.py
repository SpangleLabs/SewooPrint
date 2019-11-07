from abc import ABC


def _try_encode(text):
    """Tries to encode string to bytes, unless it is already bytes."""
    try:
        text_encode = text.encode().replace(b'\xc2\xa3', b'\x9c')
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
        line = ""
        for word in text.split():
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

    def add_text_rotated_sideays(self, text):
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
