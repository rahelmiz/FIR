#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:18:45 2022

@author: rahelmizrahi
"""
import pprint as pp
def _genVar(varName, numVars, enumFormat = None):
    # example call: Acc = _genVar("acc", 166, "A"); 
    #               Tap = _genVar("tap", 168)
    if enumFormat == None:
        varNames = []
        for i in range(0,numVars):
            varNames.append("{}{}".format(varName, i))
        return varNames
    if enumFormat== "A":
        varNames = []
        varNames.append("acc01")
        varNames.append("acc012")
        for i in range(2,numVars-2):
            varNames.append("{}{}_{}".format(varName, i, i+1))
        return varNames

class GenFIRCode:
    def __init__(self, numTaps, bitWidth = None):
        self.numTaps = numTaps
        self.varNames = ["acc", "tap", "buff"]
        self.Adders = _genVar("acc", numTaps, "A")
        self.Accums = _genVar("acc", numTaps )
        self.Taps = _genVar("tap", numTaps)
        self.Buffs = _genVar("buff", numTaps)
        self.coeffs = self._getCoeffs() #the tap values
        if bitWidth == None:
            self.bitWidth = 16
        else: self.bitWidth= bitWidth
        


    def _getCoeffs(self):
        with open("coeffs.txt", "r") as f: #was lazy and hardcded a path
            coeffs = f.readlines() #produces list of lines
        return coeffs
    def writeAssignTaps(self):
        with open("tapAssign.txt", "w+") as f: 
            for i in range(0,self.numTaps):
                c = self.coeffs[i].strip()
                text = "assign tap{} = {}'h{};\n".format(i,self.bitWidth, c) #the squiglies are analogies to %type
                #for each squiggly, you need an item inside .format( ). 
                f.write(text)  
                
    def genDeclaration(self, netType, bitWidth, varName, numVars, enumFormat= None, signed = True):
        #returns a string of the form 
        #reg [bitWidth:0] varNames[0], ..., varNames[n]
        varNames = _genVar(varName, numVars, enumFormat)
        if signed == False:
            s= "{} [{}:0] ".format(netType, bitWidth-1)
        else:
            s = "{} signed [{}:0] ".format(netType, bitWidth-1)
        for idx, val in enumerate(varNames):
            if idx== len(varNames) - 1:
                s+= (val + ";")
            else:
                s+= (val + ", ")
        return s

    def genMultAccumStage(self):
        code = "";
        code += "buff0 <= s_axis_fir_tdata;\nacc0 <= tap0 * buff0;\n"
        code += "\n"
        
        i = 1
        code+="{} <= {};\n".format(self.Buffs[i], self.Buffs[i-1])
        code+="{} <= {} * {};\n".format(self.Accums[i], self.Taps[i], self.Buffs[i])
        code+="{} <= {} + {};\n".format(self.Adders[i-1], self.Accums[i-1], self.Accums[i])
        code += "\n"
        for i in range(2, self.numTaps):
            print(i)
            if i == self.numTaps - 2:
                print("i=13")
            if i == self.numTaps-1:
                code+="{} <= {};\n".format(self.Buffs[i], self.Buffs[i-1])
                code+="{} <= {} * {};\n".format(self.Accums[i], self.Taps[i], self.Buffs[i])
                code+="m_axis_fir_tdata <= {} + {};\n".format(self.Adders[i-2], self.Accums[i])
                break
            code+="{} <= {};\n".format(self.Buffs[i], self.Buffs[i-1])
            code+="{} <= {} * {};\n".format(self.Accums[i], self.Taps[i], self.Buffs[i])
            code+="{} <= {} + {};\n".format(self.Adders[i-1], self.Adders[i-2], self.Accums[i])
            code += "\n"
        return code
     
    def writeMultAccumCode(self, outPath = None):
        code = self.genMultAccumStage()
        with open("multAccumCode.txt", "w+") as f:
            f.write(code)
    def writeDeclarations(self):
        
        code = self.genDeclaration("reg", self.bitWidth , "buff", self.numTaps)  + "\n\n"
        code += self.genDeclaration("wire", self.bitWidth , "tap", self.numTaps) + "\n\n"
        code += self.genDeclaration("reg", (self.bitWidth*2) , "acc", self.numTaps) + "\n\n"
        code += self.genDeclaration("reg", (self.bitWidth*2) , "acc", self.numTaps, enumFormat= "A")+ "\n\n"
        with open("declarations.txt", "w+") as f:
            f.write(code)
    
      
if __name__ == "__main__":
    F = GenFIRCode(168)
    #print(F.Taps)
    F.writeMultAccumCode()
    F.writeDeclarations()
    F.writeAssignTaps()
    
    
'''
  Taps = genDeclaration("wire", 16, "tap", 168)
  Buffs = genDeclaration("reg", 16, "buff", 168, signed = True)
'''
  