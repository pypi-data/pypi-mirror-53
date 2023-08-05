"""
@ Stefanie Fiedler 2019
@ Alexander Teubert 2019
Version vom 26.09.2019

for Hochschule Anhalt, University of Applied Sciences
in coorperation with axxeo GmbH
"""

def str2hex(string):
    if len(string)%2 == 0:
        myList = [ord(character) for character in (string+"\0"*2)]
        return myList

    else:
        myList = [ord(character) for character in (string+"\0")]
        return myList

def str2duohex(string):
    if len(string)%2 == 0:
        myList = [ord(character) for character in (string+"\0"*2)]
        data = []

        for count in range(len(myList)//2): data.append((myList[count*2]<<8)|myList[count*2+1])

        return data

    else:
        myList = [ord(character) for character in (string+"\0")]
        data = []

        for count in range(len(myList)//2): data.append((myList[count*2]<<8)|myList[count*2+1])

        return data

def duohex2str(hexlist):
    string = ""
    for duohex in hexlist: string += chr((duohex&0xff00)>>8) + chr(duohex&0xff)

    if hexlist[len(hexlist)-1] == 0x00: return string[:len(string)-2]
    else: return string[:len(string)-1]

def hex2str(hexlist):
    return "".join([chr(hexval) for hexval in hexlist])
