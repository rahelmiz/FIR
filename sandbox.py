# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:03:15 2022

@author: ual-laptop
"""

string = "1111111111111111111110001101001000000110"
string = "10" 
def _prettyFormatBinaryString( string, inputBase, length ):
    assert length % 4 == 0, "length of string must be a mult. of 4"
    prettyBinaryString = ""
    if inputBase == 2:
        
        for i in range(0,(len(string)),4):
            prettyBinaryString += string[i:i+4] + " "
        return prettyBinaryString
    else:
        DecValue = int(string, inputBase)
        BinaryString = bin(DecValue if DecValue>0 else DecValue+(1<<length))
        BinaryString = BinaryString[2:]
        
        print(len(BinaryString))
        for i in range(0,(len(BinaryString)),4):
            prettyBinaryString += BinaryString[i:i+4] + " "
        print(BinaryString)
        return prettyBinaryString
        
        

x= _prettyFormatBinaryString("-8", 10, 8)