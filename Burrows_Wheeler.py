# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 21:05:10 2017

@author: Isik
"""

import Reader_Writer as RW

class Burrows_Wheeler(RW.Reader_Writer):
    """ A quick and dirty implementation of the Burrows-Wheeler Transform
    
    Attributes:
        CHUNK_SIZE: The size of the data read in to be transformed at a time.
    """
    def __init__(self, CHUNK_SIZE, EOF):
        self.EOF = EOF
        self.CHUNK_SIZE = CHUNK_SIZE
        self.I_CHUNK_SIZE = CHUNK_SIZE + 1 # Because we add an self.EOF character
    
    def transform(self, InputFileName, OutputFileName):
        """Performs the BWT, one block at a time 
        
        Arguments:
            InputFileName
            OutputFileName
        
        Credit:  
        mrjbq7
        http://re-factor.blogspot.com/2015/04/burrows-wheeler-transform.html
        """

        self.open_files(InputFileName, OutputFileName)        
        while True:
            data = self.ifs.read(self.CHUNK_SIZE)

            if data == "":
                break
            
            data = data + self.EOF
            n = len(data)
            m = sorted(data[i:] + data[:i] for i in range(n))

            btw_data = ''.join(x[-1] for x in m)
            
            self.ofs.write(btw_data)
            
        self.close_files()
    
    def inverse_transform(self, InputFileName, OutputFileName):
        """Performs the Inverse BWT, one block at a time 
        
        Arguments:
            InputFileName
            OutputFileName
        
        Credit:  
        mrjbq7
        http://re-factor.blogspot.com/2015/04/burrows-wheeler-transform.html
        """

        self.open_files(InputFileName, OutputFileName)        
        
        while True:
            bwt_data = self.ifs.read(self.I_CHUNK_SIZE)
            
            if bwt_data == "":
                break
            
            n = len(bwt_data)
            m = [''] * n
            for _ in range(n):
                m = sorted(bwt_data[i] + m[i] for i in range(n))
            data =  [x for x in m if x.endswith(self.EOF)][0][:-1]
            
            self.ofs.write(data)
            
        self.close_files()

            