'''
Created on 29 May 2015

@author: dr-spangle
'''

class Formatter:
    '''
    classdocs
    '''
    mMaxLen = 42

    def multiLine(self,text):
        '''
        Formats text to be printed over multiple lines, breaking at spaces.
        '''
        maxLen = self.mMaxLen
        textLines = []
        line = ""
        for word in text.split():
            temp = line + " " + word
            temp = temp.strip()
            if(len(temp)>maxLen):
                textLines.append(line)
                line = word
            else:
                line = temp
        textLines.append(line)
        return "\n".join(textLines)

    def tryEncode(self,text):
        'Tries to encode string to bytes, unless it's already bytes.'
        try:
            bytes = text.encode()
            return bytes
        except AttributeError:
            return bytes

    def bold(self,text):
        'Makes a set string bold.'
        bytes = self.tryEncode(text)
        return b'\x1b\x21\x08' + bytes + b'\x1b\x21\x00'
