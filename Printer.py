import win32print

class Printer:
    mMaxLen = 42

    def defaultPrinter(self):
        return win32print.GetDefaultPrinter()

    def listPrinters(self):
        printerList = [item[2] for item in win32print.EnumPrinters(2)]
        blackList = ['Fax','Send To OneNote 2013','Microsoft XPS Document Writer']
        for item in blackList:
            if(item in printerList):
                printerList.remove(item)
        return printerList

    def printRaw(self,rawdata):
        rawdata += b'\n\n\n\n\n\n\x1d\x56\x01' + b'\n'
        printerin = win32print.OpenPrinter(self.defaultPrinter())
        win32print.StartDocPrinter(printerin,1,('CASHDRAWERPRINT',None,None))
        win32print.WritePrinter(printerin,rawdata)
        win32print.EndDocPrinter(printerin)
        win32print.ClosePrinter(printerin)

    def printText(self,text,printerin):
        textEncode = text.encode().replace(b'\xc2\xa3',b'\x9c')
        self.printRaw(textEncode)
        return textEncode

    def invert(self,text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1d\x42\x01' + text + b'\x1d\x42\x00'

    def underline(self,text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x2d\x01' + text + b'\x1b\x2d\x00'

    def rotate90Degrees(self,text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x56\x01' + text + b'\x1b\x56\x00'

    def upsideDown(self,text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x7b\x01' + text + b'\x1b\x7b\x00'

    def stretch(self,text,amount=2):
        try:
            text = text.encode()
        except AttributeError:
            pass
        amount = min(amount,8)
        return b'\x1d\x21' + chr(amount-1).encode() + text + b'\x1d\x21\x00'

    def tinyText(self,text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x21\x01' + text + b'\x1b\x21\x00'

    def tinyTextBold(self,text):
        try:
            text = text.encode()
        except AttributeError:
            pass
        return b'\x1b\x21\x09' + text + b'\x1b\x21\x00'

    def amountString(self,amount):
        return b'\x9c' + ("%.2f"%amount).encode()

    def numString(self,num):
        return (str(num).rstrip('0').rstrip('.').encode() if '.' in str(num) else str(num).encode())

    def leftRight(self,lefttext,righttext,width,bold=[]):
        try:
            lefttext = lefttext.encode()
        except AttributeError:
            pass
        try:
            righttext = righttext.encode()
        except AttributeError:
            pass
        spacing = width-len(lefttext+righttext)
        if('left' in bold):
            lefttext = Printer.bold(lefttext)
        if('right' in bold):
            righttext = Printer.bold(righttext)
        return lefttext + b' '*spacing + righttext

    def right(self,text,width,bold=False):
        try:
            text = text.encode()
        except AttributeError:
            pass
        spacing = width-len(text)
        if(bold):
            text = Printer.bold(text)
        return b' '*spacing + text

    def dashLine(self):
        return ('-'*42).encode()

    def columns(self,columnspec,columndata,gap=' ',spacer=' '):
        if(len(columnspec)!=len(columndata)):
            return False
        if(len([col for col in columnspec if col['width']=='fill'])>1):
            return False
        if(len(spacer)!=1):
            return False
        spacer = spacer.encode()
        gap = gap.encode()
        columnspecc = []
        for col in columnspec:
            if(col['width']=='fill'):
                restofwidth = sum([col['width'] for col in columnspec if col['width']!='fill'])+(len(gap)*(len(columnspec)-1))
                print(restofwidth)
                col['width'] = 42-restofwidth
            columnspecc.append(col)
        columnspec = columnspecc
        totalwidth = sum([col['width'] for col in columnspec])+(len(gap)*(len(columnspec)-1))
        if(totalwidth>42):
            return False
        columnout = []
        for (colspec,coldata) in zip(columnspec,columndata):
            try:
                coldata['text'] = coldata['text'].encode()
            except AttributeError:
                pass
            if(colspec['align']=='left'):
                colout = coldata['text'][:colspec['width']]
                colwidth = len(colout)
                if('func' in coldata):
                    colout = coldata['func'](colout)
                colout = colout+spacer*(colspec['width']-colwidth)
            else:
                colout = coldata['text'][::-1][:colspec['width']][::-1]
                colwidth = len(colout)
                if('func' in coldata):
                    colout = coldata['func'](colout)
                colout = spacer*(colspec['width']-colwidth)+colout
            columnout.append(colout)
        return gap.join(columnout) + b'\n'

    def testPrint(self):
        rawData = 'normal text'.encode() + b'\n'
        rawData += Printer.bold('bold text') + b'\n'
        rawData += Printer.invert('invert text') + b'\n'
        rawData += Printer.underline('underline') + b'\n'
        for num in range(256):
            rawData += b'\x1b\x21' + chr(num).encode() + ('test #'+str(num)).encode() + b'\x1b\x21\x00\n'
        rawData += 'normal'.encode() + b'\n' #normal?
        self.printRaw(rawData)

    def printOrder(self,companyname,orderdata,printerin):
        rawdata = Printer.title(companyname) + b'\n'
        dateformat = str(orderdata['Open_Date'].day).zfill(2)+'/'+str(orderdata['Open_Date'].month).zfill(2)+' '+str(orderdata['Open_Date'].hour).zfill(2)+':'+str(orderdata['Open_Date'].minute).zfill(2)
        rawdata += Printer.bold('Order placed:') + b' ' + dateformat.encode() + b'\n'
        hour_print = orderdata['DeliveryTime']['Hour']
        if(orderdata['DeliveryTime']['Meridiem']=='PM'):
            hour_print = str(int(orderdata['DeliveryTime']['Hour'])+12)
        if(orderdata['DeliveryTime']['Hour']=='ASAP'):
            rawdata += Printer.bold('Time wanted:') + b' ' + hour_print.encode() + b'\n'
        else:
            rawdata += Printer.bold('Time wanted:') + b' ' + (hour_print+':'+orderdata['DeliveryTime']['Minute']).encode() + b'\n'
        rawdata += Printer.bold('Customer: '+orderdata['Customer']) + b'\n'
        rawdata += Printer.bold('Number:') + b' ' + (orderdata['CustomerData']['Number']).encode() + b'\n'
        rawdata += ('  '+orderdata['CustomerData']['Street']).encode() + b'\n'
        rawdata += ('  '+orderdata['CustomerData']['City']).encode() + b'\n'
        rawdata += ('  '+orderdata['CustomerData']['Postcode']).encode() + b'\n\n'
        if(orderdata['Notes'] != ''):
            rawdata += Printer.bold('Notes:') + b'\n'
            for line in orderdata['Notes'].split('\n'):
                rawdata += b'  ' + line.encode() + b'\n'
            rawdata += b'\n'
        if(orderdata['Driver'] is not False):
            rawdata += Printer.bold('Driver:') + b' ' + orderdata['Driver'].encode() + b'\n'
#        rawdata += printer.leftright('Items:','Price:',37,['left','right']) + b'\n'
        deliveryitems = []
        columnspec = [{'width':3,'align':'right'},{'width':'fill','align':'left'},{'width':6,'align':'right'},{'width':6,'align':'right'}]
        rawdata += b'\n' + Printer.columns(columnspec,[{'text':'Qty'},{'text':'Item'},{'text':'Price'},{'text':'Total'}])
        rawdata += Printer.dashline()
        for item in orderdata['Items']:
            if(item['Category'][:8]=='Delivery'):
                deliveryitems.append(item)
                continue
            col_amount = {'text':Printer.numstring(item['Amount'])}
            col_item = {'text':item['Name']}
            col_unitprice = {'text':Printer.amountstring(item['Price'])}
            col_totprice = {'text':Printer.amountstring(float(item['Price'])*item['Amount']),'func':Printer.bold}
            rawdata += Printer.columns(columnspec,[col_amount,col_item,col_unitprice,col_totprice])
            if(item['Additional_Text']!=''):
                rawdata += b'      '+item['Additional_Text'].encode()+b'\n'
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
        if(len(deliveryitems)!=0):
            rawdata += Printer.dashline()
        for item in deliveryitems:
            rawdata += Printer.leftright(item['Name'],Printer.amountstring(item['Price']),42,['right']) + b'\n'
            if(item['Additional_Text']!=''):
                rawdata += b'  ' + item['Additional_Text'].encode() + b'\n'
        rawdata += Printer.dashline()
        rawdata += Printer.right('Total: '.encode()+Printer.amountstring(orderdata['Total']),42,True)
        rawdata += b'\n\n\n\n\n\n\x1d\x56\x01' + b'\n'
        printerin = win32print.OpenPrinter(printerin)
        win32print.StartDocPrinter(printerin,1,('CASHDRAWERPRINT',None,None))
        win32print.WritePrinter(printerin,rawdata)
        win32print.EndDocPrinter(printerin)
        win32print.ClosePrinter(printerin)
        return bytes

