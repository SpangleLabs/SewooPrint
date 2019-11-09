import glob

from printer import Printer


class LinuxPrinter(Printer):

    def print_document(self, document):
        raw_data = document.cut_if_uncut().encoded
        linux_printer = glob.glob("/dev/usb/lp*")[0]
        with open(linux_printer, "wb") as f:
            f.write(raw_data)
