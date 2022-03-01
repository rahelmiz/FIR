# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
with open("coeffs.txt", "r") as f:
    
    coeffs = f.readlines() #produces list of lines

with open("tap_code.txt", "w+") as f: 
    for i in range(0,168):
        c = coeffs[i].strip()
        text = "tap{} = {};\n".format(i,c) #the squiglies are analogies to %type
        #for each squiggly, you need an item inside .format( ). 
        
        f.write(text)
        
   