# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:27:08 2017

@author: Isik
"""
import Reader_Writer as RW
import random as r

CONST_CHUNK_SIZE = 1024
CONST_NUM_BITS_ASCII = 8

class ASCII_Binary(RW.Reader_Writer):
    """ This class exists to convert text to binary, and binary to text
    
    Extends:
        Reader_Writer
    """

    def __init__(self):
        """ Default Constructor """
        pass
    
            
    def a_to_strbin(self,
                    InputFileName = "DEFAULT.txt",
                    OutputFileName = "DEFAULT.txt"
                    ):
        """ Converts an ascii file to its binary representation 
        
        NOTES: The CheckBit is always set to ZERO
        """

        self.open_files(InputFileName, OutputFileName)        
        
        while True:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
            OutputBuffer = []
            'End Condition: If we read in the empty string, we\'re done'
            if InputBuffer == "":
                break
            for char in InputBuffer:
                ASCII_ORDINAL = ord(char)
                BINARY_ASCII = '{:b}'.format(ASCII_ORDINAL)
                PADDED_BINARY_ASCII = BINARY_ASCII.zfill(CONST_NUM_BITS_ASCII)
                
                OutputBuffer.append(PADDED_BINARY_ASCII)
            OutputString = ''.join(OutputBuffer)
            self.ofs.write(OutputString)
        
        self.close_files()
    
    def strbin_to_a(self,
                    InputFileName  = "DEFAULT.txt",
                    OutputFileName = "DEFAULT.txt"
                    ):
        """ Converts a binary file to an ASCII representation """
        ASCII_COUNT = 0
        BinaryASCII = []

        self.open_files(InputFileName, OutputFileName)        
        
        while True:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
            OutputBuffer = []
            'End Condition: If we read in the empty string, we\'re done'
            if InputBuffer == "":
                break
            for char in InputBuffer:
                """
                ASCII_COUNT counts towards the number of bits in an ASCII
                Binary number (CONST_NUM_BITS_ASCII). Then it converts those
                bits into a string, converts that string to a number, converts
                that number to an ASCII character and adds it onto the 
                output buffer.
                """
                ASCII_COUNT += 1
                BinaryASCII.append(char)
                if ASCII_COUNT >= CONST_NUM_BITS_ASCII:
                    ASCII_COUNT = 0
                    
                    BinaryASCII = ''.join(BinaryASCII)
                    ASCII_ORDINAL = int(BinaryASCII, 2)
                    char = chr(ASCII_ORDINAL)
                    OutputBuffer.append(char)
                    
                    BinaryASCII = []
            OutputString = ''.join(OutputBuffer)
            self.ofs.write(OutputString)
            
        self.close_files()
        
    def a_to_bytes(self,
                 InputFileName  = "DEFAULT.txt",
                 OutputFileName = "DEFAULT.txt"
                 ):
        """ Converts an ascii file to a binary file """  
        
        self.open_files(InputFileName, OutputFileName,
                        WriteFormat = 'wb')
        
        while True:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
            OutputBuffer = []
            
            'End Condition: If we read in the empty string, we\'re done'
            if InputBuffer == "":
                break
            
            for char in InputBuffer:
                ASCII_ORDINAL = ord(char)
                OutputBuffer.append(ASCII_ORDINAL)
                
            OutputByteArray = bytearray(OutputBuffer)
            self.ofs.write(OutputByteArray)
            
        self.close_files()     
    
    def bytes_to_a(self,
                   InputFileName  = "DEFAULT.txt",
                   OutputFileName = "DEFAULT.txt"
                   ):
        """ Converts a binary file to an ascii file """
        DefaultByteArray = bytearray(CONST_CHUNK_SIZE)        
        
        self.open_files(InputFileName, OutputFileName,
                        ReadFormat = 'rb')
        
        while True:
            InputBuffer = DefaultByteArray.copy()
            self.ifs.readinto(InputBuffer)
            
            'End Condition: If we see our default array, we\re done'
            if InputBuffer == DefaultByteArray:
                break     
            
            OutputString = InputBuffer.decode()
            self.ofs.write(OutputString)
            
        self.close_files()        
        
        
    def bytes_to_strbin(self,
                   InputFileName  = "DEFAULT.txt",
                   OutputFileName = "DEFAULT.txt"
                   ):
        """ Converts a binary file to an strbin file """
        DefaultByteArray = bytearray(CONST_CHUNK_SIZE)        
        
        self.open_files(InputFileName, OutputFileName,
                        ReadFormat = 'rb')
        
        while True:
            InputBuffer = DefaultByteArray.copy()
            self.ifs.readinto(InputBuffer)
            
            'End Condition: If we see our default array, we\re done'
            if InputBuffer == DefaultByteArray:
                break     
            
            OutputString = ''.join(['{:b}'.format(i).zfill(8) for i in InputBuffer])
            self.ofs.write(OutputString)
            
        self.close_files()    
    
    def strbin_to_bytes(self,
                        InputFileName   = "DEFAULT.txt",
                        OutputFileName  = "DEFAULT.txt"
                        ):
        """ 
        Converts a file that's pretending to be in binary (such as the output
        of atoi) into an actual bytearray file.
        """
        ASCII_COUNT = 0
        BinaryASCII = []

        self.open_files(InputFileName, OutputFileName,
                        WriteFormat = 'wb')        
        
        while True:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
            OutputBuffer = []
            'End Condition: If we read in the empty string, we\'re done'
            if InputBuffer == "":
                break
            for char in InputBuffer:
                """
                ASCII_COUNT counts towards the number of bits in an ASCII
                Binary number (CONST_NUM_BITS_ASCII). Then it converts those
                bits into a string, converts that string to a number, converts
                that number to an ASCII character and adds it onto the 
                output buffer.
                """
                ASCII_COUNT += 1
                BinaryASCII.append(char)
                if ASCII_COUNT >= CONST_NUM_BITS_ASCII:
                    ASCII_COUNT = 0
                    
                    BinaryASCII = ''.join(BinaryASCII)
                    ASCII_ORDINAL = int(BinaryASCII, 2)
                    OutputBuffer.append(ASCII_ORDINAL)
                    
                    BinaryASCII = []
            
            OutputByteArray = bytearray(OutputBuffer)
            self.ofs.write(OutputByteArray)
            
        self.close_files()
        
    def write_random_strbin(self, OutputFileName = "DEFAULT.txt", NumBits = 0):
        """ Writes ascii 1's and 0's, randomly, to output. """
        self.set_ofs(OutputFileName)
        
        while NumBits > CONST_CHUNK_SIZE:
            RandBuffer = '{:b}'.format(r.getrandbits(CONST_CHUNK_SIZE))
            self.ofs.write(RandBuffer)
            NumBits -= CONST_CHUNK_SIZE
        RandBuffer = '{:b}'.format(r.getrandbits(NumBits))
        self.ofs.write(RandBuffer)
        self.ofs.close()
                















