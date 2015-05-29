'''
Created on 29 May 2015

@author: dr-spangle
'''

class Formatting(object):
    '''
    classdocs
    '''

    @staticmethod
    def multiLine(text):
        '''
        Formats text to be printed over multiple lines, breaking at spaces.
        '''
        maxLen = 42
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