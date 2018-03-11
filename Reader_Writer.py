# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:14:09 2017

@author: Isik
"""

class Reader_Writer():
    """ 
    A helper class that contains all the necessary tools for reading and
    writing text or binary files.
    
    Attributes:
        ifs:    Input File Stream. 
        ofs:    Output File Stream.
    """
    
    ifs = None
    ofs = None    
    
    def __init__(self):
        """ Default Constructor """
        pass
    
    def __del__(self):
        """ Destructor """
        try:
            self.ifs.close()
        except AttributeError:
            pass
        try:
            self.ofs.close()
        except AttributeError:
            pass
        
    def set_ifs(self, InputFileName = "DEFAULT.txt", ReadFormat = 'r', NewLine = ''):
        """ A useful function to set the input file stream.
        
        Arguments:
            InputFileName:  The the name of the file to be read from.
            ReadFormat:     The python-interpreted argument for reading files.
        """
        try:
            self.ifs = open(InputFileName, ReadFormat)
        except OSError:
            InputFileName = str(InputFileName)
            self.ifs = open(InputFileName, ReadFormat)  

    def set_ofs(self, OutputFileName = "DEFAULT.txt", WriteFormat = 'w', NewLine = ''):
        """ A useful function to set the output file stream.
        
        Arguments:
            InputFileName:  The the name of the file to write to.
            WriteFormat:    The python-interpreted argument for writing files.
        """
        try:
            self.ofs = open(OutputFileName, WriteFormat)
        except OSError:
            OutputFileName = str(OutputFileName)
            self.ofs = open(OutputFileName, WriteFormat)   
            
    def open_files(self, 
                   InputFileName    = "DEFAULT.txt", 
                   OutputFileName   = "DEFAULT.txt",
                   ReadFormat       = 'rU', 
                   WriteFormat      = 'w',
                   NewLine = ''
                   ):
        """ Opens Input and Output files 
        
        Arguments:
            ReadFormat:     The python-interpreted argument for reading files
            WriteFormat:    The python-interpreted argument for writing files
        """   
        self.set_ifs(InputFileName, ReadFormat, NewLine)
        self.set_ofs(OutputFileName, WriteFormat, NewLine)        
        
    def close_files(self):
        """ Closes Input and Output files """
        self.ifs.close()
        self.ofs.close()
        