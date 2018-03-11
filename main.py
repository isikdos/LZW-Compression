# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:58:41 2017

@author: Isik
"""

import ASCII_Binary as AB
import Lempel_Ziv_Welch as LZW
import Burrows_Wheeler as BW
import Move_To_Front as MTF

def isEqual(InputFileName1, InputFileName2):
    file1 = open(InputFileName1)
    file2 = open(InputFileName2)
    i = 0
    for line1 in file1:
        i += 1
        line2 = file2.readline()
        if line1 != line2:
            print(i)
            print("FUCK")
    
    file2 = open(InputFileName1)
    file1 = open(InputFileName2)
    i = 0
    for line1 in file1:
        i += 1
        line2 = file2.readline()
        if line1 != line2:
            print(i)
            print("FUCK")


IO = AB.ASCII_Binary()
LZW1 = LZW.lzw("strbin")
MTF = MTF.Move_To_Front()

BWT2048 = BW.Burrows_Wheeler(2048, chr(0))
BWT1024 = BW.Burrows_Wheeler(1024, chr(0))
BWT512 = BW.Burrows_Wheeler(512, chr(0))
BWT256 = BW.Burrows_Wheeler(256, chr(0))
BWT128 = BW.Burrows_Wheeler(128, chr(0))
BWT64 = BW.Burrows_Wheeler(64, chr(0))

"""
#BWT64.transform("shakespeare.txt", "shakespearebwt2048.txt")
#BWT64.inverse_transform("shakespearebwt2048.txt", "original.txt"
BWT2048.transform("shakespeare.txt","shakespearebwt.txt")
MTF.transform("shakespearebwt.txt","shakespearemtf.txt")
IO.bytes_to_strbin("shakespearemtf.txt","shakespearemtf_text.txt")
LZW1.compress("shakespearemtf_text.txt","compressed.txt")
"""
IO.a_to_strbin("shakespeare.txt","out.txt")
LZW1.compress("out.txt","abc")

"""
print(0)
BWT2048.transform("shakespeare.txt", "shakespearebwt2048.txt")
print(1)
BWT1024.transform("shakespeare.txt", "shakespearebwt1024.txt")
print(1.1)
BWT512.transform("shakespeare.txt", "shakespearebwt512.txt")
print(1.2)
BWT256.transform("shakespeare.txt", "shakespearebwt256.txt")
print(1.3)
BWT128.transform("shakespeare.txt", "shakespearebwt128.txt")
print(2)
BWTMTF128 = MTF.transform("shakespearebwt128.txt", "shakespearebwtmtf128.txt")
print(2.1)
BWTMTF256 = MTF.transform("shakespearebwt128.txt", "shakespearebwtmtf256.txt")
print(2.2)
BWTMTF512 = MTF.transform("shakespearebwt128.txt", "shakespearebwtmtf512.txt")
print(2.3)
BWTMTF1024 = MTF.transform("shakespearebwt128.txt", "shakespearebwtmtf1024.txt")
print(2.4)
BWTMTF2048 = MTF.transform("shakespearebwt128.txt", "shakespearebwtmtf2048.txt")

print(3)
LZW1.compress("shakespearebwt2048.txt", "shakespearebwt_compressed2048.txt")
print(3.1)
LZW1.compress("shakespearebwt1024.txt", "shakespearebwt_compressed1024.txt")
print(3.2)
LZW1.compress("shakespearebwt512.txt", "shakespearebwt_compressed512.txt")
print(3.3)
LZW1.compress("shakespearebwt256.txt", "shakespearebwt_compressed256.txt")
print(3.4)
LZW1.compress("shakespearebwt128.txt", "shakespearebwt_compressed128.txt")

print(4)
LZW1.compress("shakespearebwtmtf2048.txt", "shakespearebwtmtf_compressed2048.txt")
print(4.1)
LZW1.compress("shakespearebwtmtf1024.txt", "shakespearebwtmtf_compressed1024.txt")
print(4.2)
LZW1.compress("shakespearebwtmtf512.txt", "shakespearebwtmtf_compressed512.txt")
print(4.3)
LZW1.compress("shakespearebwtmtf256.txt", "shakespearebwtmtf_compressed256.txt")
print(4.4)
LZW1.compress("shakespearebwtmtf128.txt", "shakespearebwtmtf_compressed128.txt")

print(5)
MTF.transform("shakespeare.txt","shakespearemtf.txt")
print(6.1)
LZW1.compress("shakespeare.txt","shakespeare_compressed.txt")
print(6.2)
LZW1.compress("shakespearemtf.txt","shakespearemtf_compressed.txt")



"""

