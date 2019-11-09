import win32print

from printer import Printer


class WindowsPrinter(Printer):

    def print_document(self, document):
        raw_data = document.cut_if_uncut().encoded
        win_printer = win32print.GetDefaultPrinter()
        printer = win32print.OpenPrinter(win_printer)
        win32print.StartDocPrinter(printer, 1, ('CASHDRAWERPRINT', None, None))
        win32print.WritePrinter(printer, raw_data)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)

    def list_printers(self):
        printer_list = [item[2] for item in win32print.EnumPrinters(2)]
        black_list = ['Fax', 'Send To OneNote 2013', 'Microsoft XPS Document Writer']
        for item in black_list:
            if item in printer_list:
                printer_list.remove(item)
        return printer_list
