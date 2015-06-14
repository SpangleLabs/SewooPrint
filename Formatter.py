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

