# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 15:29:18 2022

@author: ual-laptop
"""

''' convert a signed or unsigned int to twos complement'''
def f(n):
    nbits = n.bit_length() + 1
    return f"{n & ((1 << nbits) - 1):0{nbits}b}"

''' convert a signed or unsigned int to twos complement and pad'''
def convert2binary(n, numBits):
    truncNum = f(n)
    numBits2pad = numBits - (n.bit_length() + 1)
    if n < 0:
        bits2pad = '1'*numBits2pad
    else:
        bits2pad = '0'*numBits2pad
    return bits2pad + truncNum
        
        
    
    
x = f(-2)
x = convert2binary(-2, 8) #returns 11111110
x = convert2binary(2, 8)