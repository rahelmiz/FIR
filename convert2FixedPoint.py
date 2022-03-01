#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 18:55:01 2022

@author: rahelmizrahi
"""

data = [str(i) for i in range(-10,10)]
for d in data: 
    if d[0]=='-':
        print("s_axis_fir_tdata <= -16'd{};#2;\n".format(d[1:].strip()))
    else:
        print("s_axis_fir_tdata <= 16'd{};#2;\n".format(d.strip()))

data = [i for i in range(11,21)]
data.append(-2)
hexData = ["0x{:X}".format(i).split('x')[-1] for i in data]


