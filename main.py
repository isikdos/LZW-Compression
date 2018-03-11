# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:58:41 2017

@author: Isik
"""

import ASCII_Binary as AB
import Lempel_Ziv_Welch as LZW

IO = AB.ASCII_Binary()
LZW1 = LZW.lzw("ASCII")

LZW1.compress("Shakespeare.txt","CompressedFromASCII_Shakespeare.txt")
IO.strbin_to_bytes("CompressedFromASCII_Shakespeare.txt","CompressedFromASCII_ConvertedToBytes_Shakespeare.txt")
LZW1.decompress("CompressedFromASCII_Shakespeare.txt","OriginalShakespeare.txt")

LZW1 = LZW.lzw("strbin")
IO.a_to_strbin("Shakespeare.txt","Converted_To_strbin_Shakespeare.txt")
LZW1.compress("Converted_To_strbin_Shakespeare.txt", "CompressedFromStrBin_Shakespeare.txt")
IO.strbin_to_bytes("CompressedFromStrBin_Shakespeare.txt","CompressedFromStrBin_ConvertedToBytes_Shakespeare.txt")
LZW1.decompress("CompressedFromStrBin_Shakespeare.txt","RevertedToOriginalStrBin_Shakespeare.txt")
IO.strbin_to_a("RevertedToOriginalStrBin_Shakespeare.txt","OriginalShakespeare2.txt")