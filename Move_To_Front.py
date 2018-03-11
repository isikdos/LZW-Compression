# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 00:13:45 2017

@author: Isik
"""
import Reader_Writer as RW

symboltable = [chr(i) for i in range(128)]

class Move_To_Front( RW.Reader_Writer ):

    def __init__(self, CHUNK_SIZE = 1024):
        self.CHUNK_SIZE = CHUNK_SIZE

    def transform(self, InputFileName, OutputFileName):
        
        sequence, pad = [], symboltable[::]     
        
        self.open_files(InputFileName, OutputFileName, WriteFormat = 'wb')        
        while True:
            sequence = []
            strng = self.ifs.read(self.CHUNK_SIZE)

            if strng == "":
                break

            for char in strng:
                indx = pad.index(char)
                sequence.append(indx)
                pad = [pad.pop(indx)] + pad
            
            mtf_data = bytearray(sequence)
                
            self.ofs.write(mtf_data)
            
        self.close_files()

    def inverse_transform(self, InputFileName, OutputFileName):
        
        chars, pad = [], symboltable[::]
        
        self.open_files(InputFileName, OutputFileName, ReadFormat = 'rb')              
        for sequence in iter((lambda:self.ifs.read(self.CHUNK_SIZE)),b''):
            chars = []

            for indx in sequence:
                char = pad[indx]
                print(ord(char))
                chars.append(char)
                pad = [pad.pop(indx)] + pad
            
            mtf_data = ''.join(chars)

            self.ofs.write(mtf_data)

        self.close_files()
        
        