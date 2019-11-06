def _try_encode(text):
    """Tries to encode string to bytes, unless it is already bytes."""
    try:
        text_encode = text.encode().replace(b'\xc2\xa3', b'\x9c')
        return text_encode
    except AttributeError:
        return text


def _center_text(text):
    """Centres text on the page."""
    spacing_left = (Document.MAX_LINE_LEN - len(text)) // 2
    spacing_right = Document.MAX_LINE_LEN - len(text) - spacing_left
    centre_text = ' ' * spacing_left + text + ' ' * spacing_right
    return centre_text


class Document:
    MAX_LINE_LEN = 42

    def __init__(self):
        self.encoded = b""

    def add_multi_line(self, text):
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

    def add_invert_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1d\x42\x01' + text_encode + b'\x1d\x42\x00'
        return self

    def add_underlined_text(self, text):
        text_encode = _try_encode(text)
        self.encoded += b'\x1b\x2d\x01' + text_encode + b'\x1b\x2d\x00'
        return self

    def add_title(self, text):
        """Formats a given string as a title."""
        self.add_invert_text(_center_text(text))
        return self

    def add_text_with_control_code(self, text, control_code):
        self.encoded += b'\x1b\x21' + chr(control_code).encode() + text.encode() + b'\x1b\x21\x00\n'
        return self
