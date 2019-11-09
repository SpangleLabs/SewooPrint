import glob
import subprocess

from printer import Printer


class LinuxPrinter(Printer):

    def print_document(self, document):
        raw_data = document.cut_if_uncut().encoded
        linux_printer = glob.glob("/dev/usb/lp*")[0]
        lpr = subprocess.Popen(linux_printer, stdin=subprocess.PIPE)
        lpr.stdin.write(raw_data)
