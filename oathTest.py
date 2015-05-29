import Formatting
import Input
import Printer

text = Input.Input.techSupportOath()
formatText = Formatting.Formatting.multiLine(text)
eFormatText = formatText.encode()
Printer.Printer.print_raw(eFormatText)
