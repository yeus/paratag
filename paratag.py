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

from collections import defaultdict
import sys #for commandline arguments
from PyPDF2 import PdfFileReader #for pdf reading
import pandas as pd

import os # for "walk()" function
from os import listdir  #for listing contents of a directory
from os.path import isfile, join  #for getting files from a directory

#https://docs.python.org/2/reference/datamodel.html?highlight=__str__#object.__str__
#for different filetypes: http://stackoverflow.com/questions/10937350/how-to-check-type-of-files-without-extensions-in-python
#https://pythonhosted.org/PyPDF2/PdfFileReader.html
#http://stackoverflow.com/questions/4403827/fast-python-pdf-metadata-reader

import numpy as np  #for nan
import logging
#logging.basicConfig(filename='paratag.log',level=logging.DEBUG)

class fileinfos(object):
    def __init__(self,filename):
        self.filename=filename
        self.info={}        
        self.info['filename'] = self.filename

        self.get_meta_data()
    
    def get_meta_data(self):
        print("reading: " +self.filename)
        try:
            #strict=False because of this: https://github.com/mstamy2/PyPDF2/issues/244#issuecomment-173539608
            #it basically helps the pdffilereader stops at all kinds of situations
            pdf_toread = PdfFileReader(open(self.filename, "rb"), strict=False) 
            if not pdf_toread.isEncrypted:
                self.extractpdfdata(pdf_toread)
            else:
                self.info['encrypted']=True
                try:
                    pdf_toread.decrypt("")
                    self.extractpdfdata(pdf_toread)
                except Exception as e: 
                    print(e)
        except Exception as e:
            print(e)
            logging.warning("something is wrong with this file: " + self.filename)
            
    def get_info(self,key):
        return self.info.get(key,np.nan)

    def extractpdfdata(self, pdf_toread):
        self.info['pdfinfos'] = pdf_toread.getDocumentInfo()
        self.info['pagenum'] = pdf_toread.getNumPages()

#import json
#>>> print json.dumps({'a':2, 'b':{'x':3, 'y':{'t1': 4, 't2':5}}},
#...                  sort_keys=True, indent=4)
    def __str__(self):
        info=""
        for k,v in self.info.iteritems():
            info+="{}:  {}".format(k,v)
        return info

#TODO: https://github.com/sciunto-org/python-bibtexparser

class directory_infos(object):
    def __init__(self, path="."):
        self.path=path
        self.filesizes = []
        self.filenum = 0
        self.files=[]
        self.filetypes=defaultdict(list)
        
        self.filter="" #TODO use filter to filter for certain filetypes
                
        self.readfiles()
        self.sortfiles()
        self.generate_meta_data_table()
        #self.generatestatistics()
        
    def readfiles(self):
        for subdir, dirs, files in os.walk(self.path):
            for file in files:
                self.files+=[os.path.join(subdir, file)]
                
        print("size: {}".format(len(self.files)))
        
    def sortfiles(self):
        for f in self.files:
            self.filetypes[f[-3:]]+=[f]
        
    def generate_meta_data_table(self):
        infos=[]
        for f in self.files:
            infos+=[fileinfos(f).info]
            
        self.infodb = pd.DataFrame.from_dict(infos)
        self.infodb.to_excel("dirinfo.xls")

#onlyfiles = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and f[-3:]=='pdf')]  #get all pdf files from a directory
##sys arguments: sys.argv
#filesizes = []
#for f in onlyfiles:#[:5]:
    #mfile = fileinfos(f)
    #filesizes += [mfile.get_info('pagenum')]

folder = directory_infos(sys.argv[1])

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
#https://github.com/glamp/bashplotlib
def plotdistribution():
    fig, ax = plt.subplots()
    axes = plt.subplot(211) # (figsize=(8,2.5))#(nrows=2, ncols=2)
    groups=np.array(folder.filesizes)
    groups=groups[np.logical_not(np.isnan(groups))]  #get rid of files where information is not available
    np.histogram(groups, bins=20)
    axes.hist(groups,30,histtype='bar',label="pagenumber distribution")
    axes.set_ylabel=("overall pagenumber distribution")
    axes = plt.subplot(212) # (figsize=(8,2.5))#(nrows=2, ncols=2)
    axes.hist(groups,30,range=(0,100))
    axes.set_ylabel=("small pagenumber distribution")
    plt.show()

#plotdistribution()
#print(filesizes)
print(folder.infodb)


