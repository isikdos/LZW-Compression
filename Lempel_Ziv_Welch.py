# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:06:56 2017

@author: Isik
"""

import Reader_Writer as RW

from enum import Enum

CONST_CHUNK_SIZE = 1024
CONST_NUM_BITS_ASCII = 8

class lzw(RW.Reader_Writer):
    """ Lempel-Ziv-Welch compression & decompression. 
    
    Properties:
        FileFormat:
            An enumerator detailing various file formats. Currently supported:
                ASCII:  ASCII formatted text
                strbin: ASCII formatted binary 
                        
        file_format:    A string that is used to index the enumerator 
                        FileFormat.
        LZWDictionary:  A dictionary of values and indices used to keep track 
                        of the patterns found during a run of LZW compression 
                        or decompression.
        pattern:        The current pattern being matched against the 
                        LZWDictionary keys.
        incr_mem_ele:   A count of the number of input elements being held
                        in memory. Used for decoding.
        next_file_obj:  A variable that holds the next object after a found
                        decode pattern. Used for decoding.
        w:              Minimum number of bits required to represent 
                        largest LZW index.
    """

    class FileFormat(Enum):
        ASCII   = 1
        strbin  = 2
    
    def __init__(self, FileFormat = "ASCII"):
        """ Default constructor, sets self.file_format """
        self.file_format        = FileFormat
        self.LZWDictionary      = dict()
        self.pattern            = None
        
        LZWDictionaryLength     = len(self.LZWDictionary)
        self.w = self.calculate_w( LZWDictionaryLength )       
        
        self.incr_mem_ele       = 0
        self.next_file_obj      = ""
        
        self.num_bits_file_obj  = self.get_num_bits_file_obj()

    def compress(self,
                 InputFileName    = "DEFAULT.txt",
                 OutputFileName   = "DEFAULT.txt",
                 ):
        """ Compresses an input file using lzw and outputs to another file.
        
        Arguments:
            InputFileName:  The name of the file to be compressed
            OutputFileName: The name of the compressed file
        """
        
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -----------------------------------------------------------------------
        if self.FileFormat[FileFormat] == self.FileFormat["binary"]:
            BITS_IN_CHUNK = CONST_CHUNK_SIZE * CONST_NUM_BITS_ASCII
            DefaultByteArray = bytearray(BITS_IN_CHUNK)     
        -----------------------------------------------------------------------
        """
        self.LZWDictionary   = self.default_compression_LZWDictionary()
        self.pattern         = self.default_pattern()
        
        LZWDictionaryLength = len(self.LZWDictionary)
        self.w = self.calculate_w( LZWDictionaryLength )
        RF = self.set_ReadFormat()            
        self.open_files(InputFileName, OutputFileName,
                        ReadFormat = RF)
        
        
        OutputBuffer    = ""
        InputBuffer = self.set_InputBuffer()
        while True:
            PeekBuffer = self.set_InputBuffer()
            
            'End Condition: If we read in the empty string, we\'re done'
            if PeekBuffer == "":
                Output = self.lzw_encode(InputBuffer, OutputBuffer,
                                         EOF = True)
                self.ofs.write(Output)                                
                break
            """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
            -------------------------------------------------------------------
            elif PeekBuffer == DefaultByteArray:
                break     
            -------------------------------------------------------------------
            """
            Output = self.lzw_encode(InputBuffer, OutputBuffer)
            self.ofs.write(Output)
            InputBuffer = PeekBuffer
        self.close_files()           
        
    def lzw_encode(self, InputBuffer, OutputBuffer, EOF = False ):
        """ The MEAT of the Lempel-Ziv-Welch compression schema.
        
        LZWDictionary uses LZW Patterns as keys and their index as values.
        w keeps track of the necessary length of the key as it gets encoded.
        
        Arguments:
            InputBuffer: 
                A chunk of data read from the input file.
            OutputBuffer:
                A chunk of lzw encoded data.
            EOF:
                Signals if this is the last chunk of data.
        Return:
            OutputBuffer:
                An chunk of lzw encoded data.
        """
        
        
        for element in InputBuffer:
            LastPattern = self.pattern
            self.add_element_to_pattern( element )
       
            # If we see a new pattern
            if self.pattern not in self.LZWDictionary.keys():
                LenLZWDictionary = len(self.LZWDictionary)
                LZWIndex = '{:b}'.format(LenLZWDictionary)
                self.LZWDictionary[self.pattern] = LZWIndex   
                
                LastIndex = self.LZWDictionary[LastPattern]

                OutputBuffer = self.append_encode_OutputBuffer(OutputBuffer,
                                                        LastIndex, 
                                                        element
                                                        )
                                                        
                LenLZWDictionary = len(self.LZWDictionary)
                self.w = self.calculate_w( LenLZWDictionary )

                #Reset the pattern                
                self.pattern = self.default_pattern()
            
            # If our current pattern is as much data as we can take in
            elif len(self.pattern) >= CONST_CHUNK_SIZE:     
                """                
                Index = self.LZWDictionary[self.pattern]
                OutputBuffer = self.append_encode_OutputBuffer(OutputBuffer,
                                                        Index, 
                                                        element
                                                        )

                #Reset the pattern
                self.pattern = self.default_pattern()
                """
        # Our last encoding, if there is a message to encode.
        if EOF and (self.pattern != self.default_pattern()):
            Index = self.LZWDictionary[self.pattern]
            OutputBuffer = self.append_encode_OutputBuffer(OutputBuffer,
                                                           Index, 
                                                           ""
                                                           )
        return OutputBuffer
        
    def decompress(self,
                   InputFileName    = "DEFAULT.txt",
                   OutputFileName   = "DEFAULT.txt",
                   ):
        """ Decompresses an input file using lzw and outputs to another file.
        
        Arguments:
            InputFileName:  The name of the file to be decompressed
            OutputFileName: The name of the decompressed file
        """
        
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -----------------------------------------------------------------------
        if self.FileFormat[FileFormat] == self.FileFormat["binary"]:
            BITS_IN_CHUNK = CONST_CHUNK_SIZE * CONST_NUM_BITS_ASCII
            DefaultByteArray = bytearray(BITS_IN_CHUNK)     
        -----------------------------------------------------------------------
        """
        self.LZWDictionary      = self.default_decompression_LZWDictionary()
        self.pattern            = self.default_pattern()
        
        LZWDictionaryLength     = len(self.LZWDictionary)
        self.w = self.calculate_w( LZWDictionaryLength )

        self.incr_mem_ele       = 0
        self.next_file_obj      = ""
        
        RF = self.set_ReadFormat()            
        self.open_files(InputFileName, OutputFileName, ReadFormat = RF)
    
        OutputBuffer            = ""
        InputBuffer             = self.set_InputBuffer()
        
        while True:
            PeekBuffer = self.set_InputBuffer()
            
            'End Condition: If we read in the empty string, we\'re done'
            if PeekBuffer == "":
                Output = self.lzw_decode(InputBuffer, OutputBuffer,
                                         EOF = True)
                self.ofs.write(Output)                                
                break
            """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
            -------------------------------------------------------------------
            elif PeekBuffer == DefaultByteArray:
                break     
            -------------------------------------------------------------------
            """
            
            Output = self.lzw_decode(InputBuffer, OutputBuffer)
            self.ofs.write(Output)
            InputBuffer = PeekBuffer
        self.close_files()           
        
    def lzw_decode(self, InputBuffer, OutputBuffer, 
                   EOF = False ):
        #These arguments should probably largely belong to SELF
                   #Fix that up tomorrow
                  #Should pass in an EOF argument when EOF before breaking
                   #and then use that to get the very last part of the encoding
        """ The MEAT of the Lempel-Ziv-Welch decompression schema.
        
        LZWDictionary uses binary indices as keys and their interpreted
        encodings as values. w keeps track of the necessary length of the key 
        as it gets encoded so that the correct number of bits can be read in.
        
        Arguments:
            InputBuffer: 
                A chunk of data read from the input file.
            OutputBuffer:
                A chunk of lzw decoded data.
            EOF:
                Signals if this is the last chunk of data.
        Return:
            OutputBuffer:
                An chunk of lzw decoded data.
        """
        for element in InputBuffer:
            #Get w characters to find what the index is
            if self.incr_mem_ele < self.w:
                #To preserve key patterning
                if not (len(self.pattern) == 0 and element == '0'):  
                    self.add_element_to_pattern( element )
                self.incr_mem_ele += 1
            elif self.incr_mem_ele < \
                (self.w + self.get_num_bits_file_obj()):
                    
                self.next_file_obj = ''.join([self.next_file_obj, element])
                self.incr_mem_ele += 1
                
            #Once we have w characters, we're good.
            else:    
                #Handle the degenerate case of all zeros key
                if self.pattern == '':
                    self.pattern = '0'

                self.convert_next_file_obj()
                    
                LenLZWDictionary    = len(self.LZWDictionary)
                LZWIndex            = '{:b}'.format(LenLZWDictionary)

                DictValue = self.LZWDictionary[self.pattern]
                NewDictValue = ''.join([DictValue, self.next_file_obj])
                self.LZWDictionary[LZWIndex] = NewDictValue
                
                LastIndex = self.LZWDictionary[self.pattern]
                OutputBuffer = self.append_decode_OutputBuffer(OutputBuffer,
                                                               LastIndex)
                                                               
                LenLZWDictionary = len(self.LZWDictionary)
                self.w = self.calculate_w( LenLZWDictionary )

                #Reset iteration values               
                self.pattern        = self.default_pattern()
                self.next_file_obj  = ""
                self.incr_mem_ele   = 0
                
                if not (len(self.pattern) == 0 and element == '0'):  
                    self.add_element_to_pattern( element )
                self.incr_mem_ele += 1
            
            # If our current pattern is as much data as we can take in
            if len(self.pattern) >= CONST_CHUNK_SIZE:        
                """
                Index = self.LZWDictionary[self.pattern]
                OutputBuffer = self.append_encode_OutputBuffer(OutputBuffer,
                                                        Index, 
                                                        element,
                                                        True)

                #Reset iteration values               
                self.pattern        = self.default_pattern()
                self.next_file_obj  = ""
                self.incr_mem_ele   = 0
                
                if not (len(self.pattern) == 0 and element == '0'):  
                    self.add_element_to_pattern( element )
                self.incr_mem_ele += 1
                """
        
        # Our last encoding, if there is a message to encode.
        if EOF and (self.pattern != self.default_pattern()):
            if self.pattern == '':
                self.pattern = '0'
            self.convert_next_file_obj()
            Index = self.LZWDictionary[str(int(self.pattern))]
 
            OutputBuffer = self.append_decode_OutputBuffer(OutputBuffer,
                                                           Index)
        return OutputBuffer
            
    def calculate_w(self, LEN_LZWDICTIONARY):
        """ Sets the self value of w based on the length of the LZW dictionary.

        Arguments:
            LEN_LZWDICTIONARY: Self explanatory
        Return:
            w: Smallest number of bits needed to display the largest code.
        """
        POWER_OF_TWO = 1
        w = 1
        while( POWER_OF_TWO * 2 < LEN_LZWDICTIONARY ):
            POWER_OF_TWO *= 2
            w += 1
        
        return w
        
    def set_ReadFormat(self):
        """ Use  FileFormat to determine how to read from the file 

        Return:
            RF: The parameter needed for the Input File Stream to read the
                data in the input file properly.
        """
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            RF = 'r'
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            RF = 'r'
        else:
            RF = 'r'
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -----------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:              
            RF = 'rb'
        -----------------------------------------------------------------------
        """
        
        return RF
        
    def set_InputBuffer(self):
        """ Use FileFormat to determine how to put data in InputBuffer 
        
        Return:
            InputBuffer: A buffered chunk of data pulled from the input file.
        """
        
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
        else:
            InputBuffer = self.ifs.read(CONST_CHUNK_SIZE)
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:              
            InputBuffer = DefaultByteArray.copy()
            self.ifs.readinto(InputBuffer)
        -------------------------------------------------------------------
        """
        
        return InputBuffer
    
    def default_compression_LZWDictionary(self):
        """ Use FileFormat to determine how to initialize LZWDictionary
        
        Return:
            LZWDictionary: An initialized dictionary for LZW compression
        """
        
        LZWDictionary = dict()
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            for ASCII_ORDINAL in range(0,128):
                LZWIndex = '{:b}'.format(ASCII_ORDINAL)
                LZWDictionary[chr(ASCII_ORDINAL)] = LZWIndex     
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            LZWDictionary[""] = '0'        
        else:
            LZWDictionary[""] = '0'          
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:              
            LZWDictionary[""] = '0'
        -------------------------------------------------------------------
        """
        
        return LZWDictionary
        
    def default_decompression_LZWDictionary(self):
        """ Use FileFormat to determine how to initialize LZWDictionary
        
        Return:
            LZWDictionary: An initialized dictionary for LZW compression
        """
        
        LZWDictionary = dict()
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            for ASCII_ORDINAL in range(0,128):
                LZWIndex = '{:b}'.format(ASCII_ORDINAL)
                LZWDictionary[LZWIndex] = chr(ASCII_ORDINAL)     
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            LZWDictionary['0'] = ""        
        else:
            LZWDictionary['0'] = ""          
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:              
            LZWDictionary['0'] = ""
        -------------------------------------------------------------------
        """
        
        return LZWDictionary    
        
    def default_pattern(self):
        """ Use FileFormat to determine how to initialize LZWDictionary
        
        Return:
            pattern: The initialized pattern 
        """
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            pattern = ""
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            pattern = ""
        else:
            pattern = ""
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:              
            pattern = bytearray(0)
        -------------------------------------------------------------------
        """
        
        return pattern
        
    def add_element_to_pattern(self, element ):
        """ Use FileFormat to determine how to add an element to the pattern
        
        Arguments:
            element: The element to be added to the pattern.
        """
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            self.pattern = ''.join([self.pattern, element])
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            self.pattern = ''.join([self.pattern, element])
        else:
            self.pattern = ''.join([self.pattern, element])
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:     
            self.pattern = pattern.append(element)
        -------------------------------------------------------------------
        """
    
        
    def append_encode_OutputBuffer(self, OutputBuffer, Index, element, 
                                   NoPad = False):
        """ Use FileFormat to determine how to add an element to the pattern
        
        Arguments:
            OutputBuffer:   The current state of the output buffer
            Index:          The lzw value of the last recognized pattern.
            Element:        The new element to be appended to OutputBuffer
            NoPad:          Prevents padding
        Return:
            OutputBuffer:
                The new state of the output buffer.
        """
        if NoPad:
            w = 0
        else:
            w = self.w
            
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            if element != "":
                ASCII_ORDINAL = ord(element)
                BINARY_ASCII = '{:b}'.format(ASCII_ORDINAL).zfill(7)
            else:
                BINARY_ASCII = ""

            PADDED_INDEX = Index.zfill(w)
            
            OutputBuffer = ''.join([OutputBuffer, 
                                    PADDED_INDEX, 
                                    BINARY_ASCII])
                                    
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            PADDED_INDEX = Index.zfill(w)
            OutputBuffer = ''.join([OutputBuffer, PADDED_INDEX, element])
            
        else:
            PADDED_INDEX = Index.zfill(w)
            OutputBuffer = ''.join([OutputBuffer, PADDED_INDEX, element])
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:
            element = CONVERT BYTE ARRAY TO STRBIN
            OutputBuffer = ''.join([OutputBuffer, Index, element])
        -------------------------------------------------------------------
        """
        return OutputBuffer
        
    def append_decode_OutputBuffer(self, OutputBuffer, Index):
        """ Use FileFormat to determine how to add an element to the pattern
        
        Arguments:
            OutputBuffer:   The current state of the output buffer
            Index:          The lzw value of the last recognized pattern.
        Return:
            OutputBuffer:
                The new state of the output buffer.
        """
        element = self.next_file_obj
            
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:            
            OutputBuffer = ''.join([OutputBuffer, 
                                    Index, 
                                    element])
                                    
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            OutputBuffer = ''.join([OutputBuffer, Index, element])    
        else:
            OutputBuffer = ''.join([OutputBuffer, Index, element])
        """ CURRENTLY UNUSED, HERE FOR FUTURE EXPANSION
        -------------------------------------------------------------------
        elif self.FileFormat[self.file_format] == self.FileFormat["binary"]:
            element = CONVERT BYTE ARRAY TO STRBIN
            OutputBuffer = ''.join([OutputBuffer, Index, element])
        -------------------------------------------------------------------
        """
        return OutputBuffer
        
        
    def get_num_bits_file_obj(self):
        """ Use FileFormat to determine how many bits in a file object
        
        Bits, char, etc.
        """
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            return CONST_NUM_BITS_ASCII - 1 
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            return 1
        else:
            return 1
            
    def convert_next_file_obj(self):
        """ Convert the binary file object to the character it represents.
        
        Main function:  With strbin, 7 binary characters will be read and
                        converted to a character.
        """
        if self.FileFormat[self.file_format] == self.FileFormat["ASCII"]:
            if self.next_file_obj != '':
                self.next_file_obj = self.next_file_obj.lstrip('0')
                if self.next_file_obj == '':
                    self.next_file_obj = '0'
                self.next_file_obj = self.LZWDictionary[self.next_file_obj]
        elif self.FileFormat[self.file_format] == self.FileFormat["strbin"]:
            pass
        else:
            pass
        

        