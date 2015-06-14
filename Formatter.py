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
        'Tries to encode string to bytes, unless it\'s already bytes.'
        try:
            textEncode = text.encode()
            return textEncode
        except AttributeError:
            return text

    def bold(self,text):
        'Makes a set string bold.'
        textEncode = self.tryEncode(text)
        return b'\x1b\x21\x08' + textEncode + b'\x1b\x21\x00'
    
    def title(self,text):
        'Formats a given string as a title.'
        textEncode = self.tryEncode(text)
        spacingLeft = (self.mMaxLen-len(text))//2
        spacingRight = self.mMaxLen-len(text)-spacingLeft
        return b'\x1d\x42\x01' + b' '*spacingLeft + textEncode + b' '*spacingRight + b'\x1d\x42\x00\n'
