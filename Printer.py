import win32print


class Printer:
    mMaxLen = 42

    def default_printer(self):
        return win32print.GetDefaultPrinter()

    def list_printers(self):
        printer_list = [item[2] for item in win32print.EnumPrinters(2)]
        black_list = ['Fax', 'Send To OneNote 2013', 'Microsoft XPS Document Writer']
        for item in black_list:
            if item in printer_list:
                printer_list.remove(item)
        return printer_list

    def print_raw(self, raw_data):
        raw_data += b'\n\n\n\n\n\n\x1d\x56\x01' + b'\n'
        printer = win32print.OpenPrinter(self.default_printer())
        win32print.StartDocPrinter(printer, 1, ('CASHDRAWERPRINT', None, None))
        win32print.WritePrinter(printer, raw_data)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)

    def print_text(self, text):
        text_encode = text.encode().replace(b'\xc2\xa3', b'\x9c')
        self.print_raw(text_encode)
        return text_encode

    def invert(self, text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1d\x42\x01' + text + b'\x1d\x42\x00'

    def underline(self, text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x2d\x01' + text + b'\x1b\x2d\x00'

    def rotate90_degrees(self, text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x56\x01' + text + b'\x1b\x56\x00'

    def upside_down(self, text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x7b\x01' + text + b'\x1b\x7b\x00'

    def stretch(self, text, amount=2):
        try:
            text = text.encode()
        except AttributeError:
            pass
        amount = min(amount, 8)
        return b'\x1d\x21' + chr(amount - 1).encode() + text + b'\x1d\x21\x00'

    def tiny_text(self, text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x21\x01' + text + b'\x1b\x21\x00'

    def tiny_text_bold(self, text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x21\x09' + text + b'\x1b\x21\x00'

    def amount_string(self, amount):
        return b'\x9c' + ("%.2f" % amount).encode()

    def num_string(self, num):
        return str(num).rstrip('0').rstrip('.').encode() if '.' in str(num) else str(num).encode()

    def left_right(self, left_text, right_text, width, bold=None):
        if bold is None:
            bold = []
        try:
            left_text = left_text.encode()
        except AttributeError:
            pass
        try:
            right_text = right_text.encode()
        except AttributeError:
            pass
        spacing = width - len(left_text + right_text)
        if 'left' in bold:
            left_text = Printer.bold(left_text)
        if 'right' in bold:
            right_text = Printer.bold(right_text)
        return left_text + b' ' * spacing + right_text

    def right(self, text, width, bold=False):
        try:
            text = text.encode()
        except AttributeError:
            pass
        spacing = width - len(text)
        if bold:
            text = Printer.bold(text)
        return b' ' * spacing + text

    def dash_line(self):
        return ('-' * 42).encode()

    def columns(self, column_spec, column_data, gap=' ', spacer=' '):
        if len(column_spec) != len(column_data):
            return False
        if len([col for col in column_spec if col['width'] == 'fill']) > 1:
            return False
        if len(spacer) != 1:
            return False
        spacer = spacer.encode()
        gap = gap.encode()
        column_specc = []
        for col in column_spec:
            if col['width'] == 'fill':
                rest_of_width = sum(
                    [col['width'] for col in column_spec if col['width'] != 'fill']) + (
                                          len(gap) * (len(column_spec) - 1))
                print(rest_of_width)
                col['width'] = 42 - rest_of_width
            column_specc.append(col)
        column_spec = column_specc
        total_width = sum([col['width'] for col in column_spec]) + (len(gap) * (len(column_spec) - 1))
        if total_width > 42:
            return False
        column_out = []
        for (col_spec, col_data) in zip(column_spec, column_data):
            try:
                col_data['text'] = col_data['text'].encode()
            except AttributeError:
                pass
            if col_spec['align'] == 'left':
                col_out = col_data['text'][:col_spec['width']]
                colwidth = len(col_out)
                if 'func' in col_data:
                    col_out = col_data['func'](col_out)
                col_out = col_out + spacer * (col_spec['width'] - colwidth)
            else:
                col_out = col_data['text'][::-1][:col_spec['width']][::-1]
                colwidth = len(col_out)
                if 'func' in col_data:
                    col_out = col_data['func'](col_out)
                col_out = spacer * (col_spec['width'] - colwidth) + col_out
            column_out.append(col_out)
        return gap.join(column_out) + b'\n'

    def test_print(self):
        raw_data = 'normal text'.encode() + b'\n'
        raw_data += Printer.bold('bold text') + b'\n'
        raw_data += self.invert('invert text') + b'\n'
        raw_data += self.underline('underline') + b'\n'
        for num in range(256):
            raw_data += b'\x1b\x21' + chr(num).encode() + (
                        'test #' + str(num)).encode() + b'\x1b\x21\x00\n'
        raw_data += 'normal'.encode() + b'\n'  # normal?
        self.print_raw(raw_data)

    def print_order(self, company_name, order_data, printer):
        raw_data = Printer.title(company_name) + b'\n'
        date_format = str(order_data['Open_Date'].day).zfill(2) + '/' + str(
            order_data['Open_Date'].month).zfill(2) + ' ' + str(order_data['Open_Date'].hour).zfill(
            2) + ':' + str(order_data['Open_Date'].minute).zfill(2)
        raw_data += Printer.bold('Order placed:') + b' ' + date_format.encode() + b'\n'
        hour_print = order_data['DeliveryTime']['Hour']
        if order_data['DeliveryTime']['Meridiem'] == 'PM':
            hour_print = str(int(order_data['DeliveryTime']['Hour']) + 12)
        if order_data['DeliveryTime']['Hour'] == 'ASAP':
            raw_data += Printer.bold('Time wanted:') + b' ' + hour_print.encode() + b'\n'
        else:
            raw_data += Printer.bold('Time wanted:') + b' ' + (
                    hour_print + ':' + order_data['DeliveryTime']['Minute']).encode() + b'\n'
        raw_data += Printer.bold('Customer: ' + order_data['Customer']) + b'\n'
        raw_data += Printer.bold('Number:') + b' ' + (
            order_data['CustomerData']['Number']).encode() + b'\n'
        raw_data += ('  ' + order_data['CustomerData']['Street']).encode() + b'\n'
        raw_data += ('  ' + order_data['CustomerData']['City']).encode() + b'\n'
        raw_data += ('  ' + order_data['CustomerData']['Postcode']).encode() + b'\n\n'
        if order_data['Notes'] != '':
            raw_data += Printer.bold('Notes:') + b'\n'
            for line in order_data['Notes'].split('\n'):
                raw_data += b'  ' + line.encode() + b'\n'
            raw_data += b'\n'
        if order_data['Driver'] is not False:
            raw_data += Printer.bold('Driver:') + b' ' + order_data['Driver'].encode() + b'\n'
        #        rawdata += printer.leftright('Items:','Price:',37,['left','right']) + b'\n'
        delivery_items = []
        column_spec = [{'width': 3, 'align': 'right'}, {'width': 'fill', 'align': 'left'},
                      {'width': 6, 'align': 'right'}, {'width': 6, 'align': 'right'}]
        raw_data += b'\n' + self.columns(
            column_spec,
            [{'text': 'Qty'}, {'text': 'Item'}, {'text': 'Price'}, {'text': 'Total'}]
        )
        raw_data += self.dash_line()
        for item in order_data['Items']:
            if item['Category'][:8] == 'Delivery':
                delivery_items.append(item)
                continue
            col_amount = {'text': self.num_string(item['Amount'])}
            col_item = {'text': item['Name']}
            col_unit_price = {'text': self.amount_string(item['Price'])}
            col_total_price = {
                'text': self.amount_string(float(item['Price']) * item['Amount']),
                'func': Printer.bold
            }
            raw_data += self.columns(
                column_spec,
                [col_amount, col_item, col_unit_price, col_total_price]
            )
            if item['Additional_Text'] != '':
                raw_data += b'      ' + item['Additional_Text'].encode() + b'\n'
        #            if(item['Additional_Text']!=''):
        #                if(item['Amount']!=1):
        #                    rawdata += printer.leftright(item['Name'],printer.amountstring(item['Price']),37) + b' ' + printer.numstring(item['Amount']) + b'\n'
        #                    rawdata += printer.leftright(b'  '+item['Additional_Text'].encode(),printer.amountstring(float(item['Price'])*item['Amount']),37,['right']) + b'\n'
        #                else:
        #                    rawdata += printer.leftright(item['Name'],printer.amountstring(item['Price']),37,['right']) + b'\n'
        #                    rawdata += b'  ' + item['Additional_Text'].encode() + b'\n'
        #            else:
        #                if(item['Amount']!=1):
        #                    rawdata += printer.leftright(item['Name'],printer.amountstring(item['Price']),37) + b' ' + printer.numstring(item['Amount']) + b'\n'
        #                    rawdata += printer.leftright('',printer.amountstring(float(item['Price'])*item['Amount']),37,['right']) + b'\n'
        #                else:
        #                    rawdata += printer.leftright(item['Name'],printer.amountstring(item['Price']),37,['right']) + b'\n'
        if len(delivery_items) != 0:
            raw_data += self.dash_line()
        for item in delivery_items:
            raw_data += self.left_right(
                item['Name'], self.amount_string(item['Price']), 42,
                ['right']) + b'\n'
            if item['Additional_Text'] != '':
                raw_data += b'  ' + item['Additional_Text'].encode() + b'\n'
        raw_data += self.dash_line()
        raw_data += self.right(
            'Total: '.encode() + self.amount_string(order_data['Total']), 42,
            True
        )
        raw_data += b'\n\n\n\n\n\n\x1d\x56\x01' + b'\n'
        printer = win32print.OpenPrinter(printer)
        win32print.StartDocPrinter(printer, 1, ('CASHDRAWERPRINT', None, None))
        win32print.WritePrinter(printer, raw_data)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)
        return bytes
