# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:03:15 2022

@author: ual-laptop
"""

string = "1111111111111111111110001101001000000110"
string = "10" 
import re

import numpy as np
import matplotlib.pyplot as plt
outputBin = "0011001100110010"
want = "1100"
simOutput = "0000111001110011"
def rescale(coeffs):
    coeffs_new = []
    for coe in coeffs:
        if coe > 32767:
            coe -=65536
        coeffs_new.append(coe)
    return coeffs_new

with open ("coeffs.txt", "r") as f:
    coeffsHex = f.readlines()

coeffs = [int(i, 16)  for i in coeffsHex]

coeffs = rescale(coeffs)

with open("coeffsDecimal.txt", "w+") as f:
    for coe in coeffs:
        f.write(str(coe))
        f.write("\n")
plt.plot(coeffs)

with open('coeffsDecimal.txt') as f:
    coeffs = f.readlines()
coeffs = [int(coe) for coe in coeffs]
plt.plot(coeffs)