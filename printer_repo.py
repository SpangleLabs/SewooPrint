import win32print

from document import TextDocument, ColumnsSpec, ColumnSpec, ColumnAlign


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
        doc = TextDocument().add_title(company_name).nl()
        # Order date
        order_date = order_data['Open_Date']
        date_format = "{:02d}/{:02d} {:02d}:{:02d}".format(
            order_date.day, order_date.month, order_date.hour, order_date.minute
        )
        doc.add_bold_text("Order placed: ").add_text(date_format).nl()
        # Delivery time
        delivery_time = order_data['DeliveryTime']
        pm = delivery_time['Hour'] != "ASAP" and delivery_time['Meridiem'] == "PM"
        delivery_hour = int(delivery_time['Hour']) + 12 if pm else delivery_time['Hour']
        doc.add_bold_text("Time wanted: ")
        if delivery_time['Hour'] == "ASAP":
            doc.add_text("ASAP").nl()
        else:
            doc.add_text("{:02d}:{:02d}".format(delivery_hour, delivery_time['Minute'])).nl()
        doc.add_bold_text("Customer: ").add_text(order_data['Customer']).nl()
        doc.add_bold_text("Number: ").add_text(order_data['CustomerData']['Number']).nl()
        doc.add_text("  {}".format(order_data['CustomerData']['Street'])).nl()
        doc.add_text("  {}".format(order_data['CustomerData']['City'])).nl()
        doc.add_text("  {}".format(order_data['CustomerData']['Postcode'])).nl()
        if order_data['Notes']:
            doc.add_bold_text("Notes:").nl()
            doc.add_line_wrapped_text(order_data['Notes']).nl()
        if order_data['Driver']:
            doc.add_bold_text("Driver: ").add_text(order_data['Driver']).nl()
        column_spec = ColumnsSpec([
            ColumnSpec(3, ColumnAlign.right),
            ColumnSpec(None, ColumnAlign.left),
            ColumnSpec(6, ColumnAlign.right),
            ColumnSpec(6, ColumnAlign.right)
        ])
        doc.nl()
        doc.add_columns(column_spec, ["Qty", "Item", "Price", "Total"])
        doc.add_dashed_line()
        delivery_items = []
        for item in order_data['Items']:
            if item['Category'][:8] == 'Delivery':
                delivery_items.append(item)
                continue
            doc.add_columns(
                column_spec,
                [
                    (item['Amount'], doc.add_number),
                    item['Name'],
                    (item['Price'], doc.add_price),
                    (float(item['Price']) * item['Amount'], doc.add_price)
                ]
            )
            if item['Additional_Text']:
                doc.add_text("      {}".format(item['Additional_Text'])).nl()
        if len(delivery_items) != 0:
            doc.add_dashed_line()
        for item in delivery_items:
            doc.add_left_right_text(item['Name'], item['Price'], right_func=doc.add_price)
            if item['Additional_Text'] != '':
                doc.add_text("      {}".format(item['Additional_Text'])).nl()
        doc.add_dashed_line()
        doc.add_left_right_text(
            "Total:", order_data['Total'], left_func=doc.add_bold_text, right_func=doc.add_price
        )
        self.print_document(doc)
