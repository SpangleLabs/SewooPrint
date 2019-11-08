import win32print

from document import TextDocument


class PrinterRepo:

    def default_printer(self):
        return win32print.GetDefaultPrinter()

    def list_printers(self):
        printer_list = [item[2] for item in win32print.EnumPrinters(2)]
        black_list = ['Fax', 'Send To OneNote 2013', 'Microsoft XPS Document Writer']
        for item in black_list:
            if item in printer_list:
                printer_list.remove(item)
        return printer_list

    def print_document(self, document):
        raw_data = document.cut_if_uncut().get_encoded()
        printer = win32print.OpenPrinter(self.default_printer())
        win32print.StartDocPrinter(printer, 1, ('CASHDRAWERPRINT', None, None))
        win32print.WritePrinter(printer, raw_data)
        win32print.EndDocPrinter(printer)
        win32print.ClosePrinter(printer)

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

    def test_print(self):
        document = TextDocument().add_text("normal text").nl() \
            .add_bold_text("bold text").nl()\
            .add_invert_colours_text("invert text").nl()\
            .add_underlined_text("underline").nl()
        for num in range(256):
            document.add_text_with_control_code("test #"+str(num), num).nl()
        document.add_text("normal")
        self.print_document(document)

    def print_order(self, company_name, order_data, printer):
        raw_data = PrinterRepo.title(company_name) + b'\n'
        date_format = str(order_data['Open_Date'].day).zfill(2) + '/' + str(
            order_data['Open_Date'].month).zfill(2) + ' ' + str(order_data['Open_Date'].hour).zfill(
            2) + ':' + str(order_data['Open_Date'].minute).zfill(2)
        raw_data += PrinterRepo.bold('Order placed:') + b' ' + date_format.encode() + b'\n'
        hour_print = order_data['DeliveryTime']['Hour']
        if order_data['DeliveryTime']['Meridiem'] == 'PM':
            hour_print = str(int(order_data['DeliveryTime']['Hour']) + 12)
        if order_data['DeliveryTime']['Hour'] == 'ASAP':
            raw_data += PrinterRepo.bold('Time wanted:') + b' ' + hour_print.encode() + b'\n'
        else:
            raw_data += PrinterRepo.bold('Time wanted:') + b' ' + (
                    hour_print + ':' + order_data['DeliveryTime']['Minute']).encode() + b'\n'
        raw_data += PrinterRepo.bold('Customer: ' + order_data['Customer']) + b'\n'
        raw_data += PrinterRepo.bold('Number:') + b' ' + (
            order_data['CustomerData']['Number']).encode() + b'\n'
        raw_data += ('  ' + order_data['CustomerData']['Street']).encode() + b'\n'
        raw_data += ('  ' + order_data['CustomerData']['City']).encode() + b'\n'
        raw_data += ('  ' + order_data['CustomerData']['Postcode']).encode() + b'\n\n'
        if order_data['Notes'] != '':
            raw_data += PrinterRepo.bold('Notes:') + b'\n'
            for line in order_data['Notes'].split('\n'):
                raw_data += b'  ' + line.encode() + b'\n'
            raw_data += b'\n'
        if order_data['Driver'] is not False:
            raw_data += PrinterRepo.bold('Driver:') + b' ' + order_data['Driver'].encode() + b'\n'
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
                'func': PrinterRepo.bold
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
