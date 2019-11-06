from abc import ABC, abstractmethod
import win32print


class Printer(ABC):

    @abstractmethod
    def print_document(self, document):
        pass


class WindowsPrinter(Printer):

    def __init__(self):
        self.win_printer = win32print.GetDefaultPrinter()

    def print_document(self, document):
        raw_data = document.cut_if_uncut().encoded
        printer = win32print.OpenPrinter(self.win_printer)
        win32print.StartDocPrinter(printer, 1, ('CASHDRAWERPRINT', None, None))
        win32print.WritePrinter(printer, raw_data)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)
