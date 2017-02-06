#!/usr/bin/env python
 # -*- coding: utf-8 -*-

__author__ = "Thomas Meschede a.k. yeus"
__copyright__ = "Copyright 2007, Thomas Meschede"
__credits__ = ["Thomas Meschede"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Thomas Meschede"
__email__ = "Thomas.Meschede@ilr.tu-berlin.de"
__status__ = "pre-alpha"

#import pdfminer #http://euske.github.io/pdfminer/index.html #only work with python2!
# 1
#For Python 3 and new pdfminer (pip install pdfminer3k):



#https://github.com/mstamy2/PyPDF2

#from pdfminer.pdfparser import PDFParser
#from pdfminer.pdfdocument import PDFDocument

import sys #for commandline arguments
from PyPDF2 import PdfFileReader #for pdf reading

from os import listdir  #for listing contents of a directory
from os.path import isfile, join  #for getting files from a directory


#fp = open(sys.argv[1], 'rb')
#parser = PDFParser(fp)
#doc = PDFDocument(parser)

#print(doc.info)  # The "Info" metadata

#https://docs.python.org/2/reference/datamodel.html?highlight=__str__#object.__str__
#for different filetypes: http://stackoverflow.com/questions/10937350/how-to-check-type-of-files-without-extensions-in-python
class fileinfos(object):
    def __init__(self,filename):
        self.filename=filename
        
        self.get_meta_data()
        
    def get_meta_data(self):
        pdf_toread = PdfFileReader(open(self.filename, "rb"))
        self.pdf_info = pdf_toread.getDocumentInfo()
        self.pagenumber = pdf_toread.getNumPages()

    def __str__(self):
        info="""pdfinfo:      {}
                pagenumber:   {}
                """
        return info.format(self.pdf_info, self.pagenumber)

mypath="."
onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)))]

for i in onlyfiles:
    print(i[-3:])
    
mfile = fileinfos(sys.argv[1])

print(mfile)

