#!/usr/bin/env python3
# or only python without 3 if system-default python is requestes
#/usr/bin/python3
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
#reload(sys)  
#sys.setdefaultencoding('utf8')  #for handling pdf files in unicode

from PyPDF2 import PdfFileReader #for pdf reading
import pandas as pd

import os # for "walk()" function
from os import listdir  #for listing contents of a directory
from os.path import isfile, join  #for getting files from a directory

#http://pyxattr.k1024.org/module.html
import xattr  #for setting and reading xtended attributes
import argparse #for commandline arguments
import traceback  #for error reporting

#https://docs.python.org/2/reference/datamodel.html?highlight=__str__#object.__str__
#for different filetypes: http://stackoverflow.com/questions/10937350/how-to-check-type-of-files-without-extensions-in-python
#https://pythonhosted.org/PyPDF2/PdfFileReader.html
#http://stackoverflow.com/questions/4403827/fast-python-pdf-metadata-reader

import numpy as np  #for nan
import logging
logging.basicConfig
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='paratag.log',level=logging.DEBUG)

from collections import Counter # for word counting
import subprocess  #to process all kinds of files and capture stdout

import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

class fileinfos(object):
    def __init__(self,filename):
        self.filename=filename
        self.info={}        
        self.info['filename'] = self.filename
        filetype=self.filename.split(".")
        if len(filetype)>=1: self.info['type'] = filetype[-1]
        
        self.metadata_read=False  #for some functions that need metadata as a prerequisite (like word_count)
        self.get_meta_data()
        #TODO: initialize file database (that can be used to generate scores)
    
    #TODO: extract more metainformation with this method:
    #https://pythonhosted.org/PyPDF2/PageObject.html#PyPDF2.pdf.PageObject
    #for example, extracting page dimensions (and recognizing presentations)
    def get_meta_data(self):
        logging.info("reading: " +self.filename)
        if self.info['type'] =='pdf':
            try:
                #strict=False because of this: https://github.com/mstamy2/PyPDF2/issues/244#issuecomment-173539608
                #it basically helps the pdffilereader stops at all kinds of situations
                pdf_toread = PdfFileReader(open(self.filename, "rb"), strict=False)
                self.pdf_toread=pdf_toread
                self.metadata_read=True
                #TODO: increase pdf score
                self.info['pagenum']=-1 #potential unknown pagenumber if decrypted
                try:
                    if pdf_toread.isEncrypted: 
                        self.info['encrypted']=True# if pdf_toread.isEncrypted else False
                        pdf_toread.decrypt("")
                        self.info['pagenum']=-1 #potential unknown pagenumber if decrypted
                    else:
                        self.info['pagenum'] = pdf_toread.getNumPages()
                        
                    #TODO: getXmpMetadata()
                    for k,v in pdf_toread.getDocumentInfo().items():  #loop through pdf metadata (exif)
                        self.info[str(k)]=str(v)
                        
                except Exception as e:
                    logging.error("{}\n{}".format(self.filename,traceback.format_exc()))
            except Exception as e:
                logging.error(traceback.format_exc())
                logging.warning("something is wrong with this file: " + self.filename)
            
    def get_info(self,key):
        return self.info.get(key,np.nan)

    def word_count(self,keyword=None):
        #TODO: from collections import Counter  #for counting all words
        if not self.metadata_read: self.get_meta_data()#
        try:
            logging.info("counting words")
            c=Counter() #https://docs.python.org/3.5/library/collections.html#collections.Counter
            #the pypdf2 method does not work well for extracting text
            #for p in self.pdf_toread.pages:
                #pagetext=p.extractText()
                ##pagetext.replace("\n","")
                ##print(p.getContents())
                #c.update([s.split(pagetext)])
                ##from IPython import embed; embed()
                #word_count=0
            
            #TODO: maybe using ps2ascii?  whicever is faster...
            print(os.getcwd())
            txt = subprocess.check_output(['pdf2txt "{}"'.format(self.filename)], shell=True)
            #proc = subprocess.Popen(["pdf2txt", self.filename], stdout=subprocess.PIPE, shell=True)
            #(out, err) = proc.communicate()
            #print(out,err)
            #from IPython import embed; embed()
            txt=txt.lower().split()
            c.update(txt)
            self.info["word_count"]=sum(c.values())
            self.info["most_common_word"]=c.most_common(1)
            if keyword: self.info["score"]=c.get(keyword.encode('utf-8'))
        except Exception as e:
            logging.error(traceback.format_exc())

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
        self.path= os.path.join(os.getcwd(),path)
        print("anylyzing: {}".format(self.path))
        self.filenum = 0
        self.files=[]
        self.infos={}
        self.filetypes=defaultdict(list)
        
        self.filefilter="pdf" #TODO use filter to filter for certain filetypes (whitelist)
                
        self.readfiles()
        self.sortfiles()
        #self.generatestatistics()
        
    #TODO:  def calc_similarty_score()  #similarity score between several documents
    # TODO:  use genim or sklearn (scikit-learn)
    # http://radimrehurek.com/gensim/install.html
        
    def readfiles(self):
        for subdir, dirs, files in os.walk(self.path):
            for file in files:
                filetype=file[-3:]
                if filetype in self.filefilter:
                    self.files+=[os.path.join(subdir, file)]
                
        logging.info("file-size: {}".format(len(self.files)))
        
    def sortfiles(self):
        for f in self.files:
            self.filetypes[f[-3:]]+=[f]
        
    def generate_meta_data(self, keyword=None):
        for f in self.files:
            fi = fileinfos(f)
            if keyword: fi.word_count(keyword)
            self.infos[f]=fi.info

    def savetoexcel(self, filename="dirinfo.xls"):
        self.infodb = pd.DataFrame.from_dict(self.infos,orient='index')
        self.infodb.to_excel(filename)
        
    def get_info(self):
        return self.infos
    
    def clear_paratags(self):
        for f in self.files:
            x = xattr.xattr(f)
            if 'user.xdg.tags' in x:
                tags = set([tags for tags in x['user.xdg.tags'].split(b",")])
            else: tags = set()
    
            #print(tags)
            newlist=[x for x in tags if not x.endswith(b'_pt')]
            #print(newlist)
            x['user.xdg.tags']=b",".join(newlist)
            
            
    def write_tags(self):
        for f,info in self.infos.items():
         try:
          if info['type']=='pdf':
            x = xattr.xattr(f)

            #print(x)
            if 'user.xdg.tags' in x:
                tags = set([tags for tags in x['user.xdg.tags'].split(b",")])
            else: tags = set()

            # find more categories:
            #   * (presentation, thesis)
            #   * manuals
            if   200 < info["pagenum"]     : tags.update([b'book_pt'])
            elif 20 < info["pagenum"] < 200: tags.update([b'report_pt'])
            elif 0 < info["pagenum"] < 40  : tags.update([b'paper_pt'])
            else: tags.update([b'docs_pt']) #everything else is a "document"
            #print("setting tags: " + ",".join([i.decode("utf-8") for i in tags]))

            #print("set tags")
            x['user.xdg.tags']=b",".join(tags)
         except Exception as e:
            logging.warning("error setting attributes for file:" + f)
            logging.error(traceback.format_exc())

#https://github.com/glamp/bashplotlib
def plotdistribution(folder):
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    axes = plt.subplot(211) # (figsize=(8,2.5))#(nrows=2, ncols=2)
    groups=np.array(folder.get_info())
    groups=groups[np.logical_not(np.isnan(groups))]  #get rid of files where information is not available
    np.histogram(groups, bins=20)
    axes.hist(groups,30,histtype='bar',label="pagenumber distribution")
    axes.set_ylabel=("overall pagenumber distribution")
    axes = plt.subplot(212) # (figsize=(8,2.5))#(nrows=2, ncols=2)
    axes.hist(groups,30,range=(0,100))
    axes.set_ylabel=("small pagenumber distribution")
    plt.show()

#folder = directory_infos(sys.argv[1])
#plotdistribution()
#print(filesizes)
#print(folder.infodb)

def main():
    parser = argparse.ArgumentParser(description="paratag")
    parser.add_argument('-c','--clear',action='store_true', help="clears all paratag 'tags' in this directory")
    parser.add_argument('-d','--dir',nargs='?', default=".", help="set directory to search for tags (default is current working directory)")
    parser.add_argument('-w','--write_tags',nargs='?', default=None, help="write tags from database in xtended attributes of files")
    parser.add_argument('-kw','--keyword', nargs='?', default=None, help="provide a keyword to search for with optional associated tag")
    parser.add_argument('-s','--stats',action='store_true', help="generate statistics for files and save them into excel file")
    #parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    #TODO: configure logging level

    print("analyzing path: " + args.dir)
    dirinfos = directory_infos(args.dir)
    if args.clear:
        print("clear paratags")
        dirinfos.clear_paratags()
        return 0
    elif args.write_tags:
        print("analyze files...")
        print("write tags...")
        dirinfos.generate_meta_data()
        interactive=False
        if interactive==True:
            from IPython import embed
            embed()
        dirinfos.write_tags()
        #dirinfos.savetoexcel()
    else:#if args.stats:
        print("analyze files...")
        if args.keyword: print("search for keyword: '{}'".format(args.keyword))
        dirinfos.generate_meta_data(keyword=args.keyword)
        print("save to excel file")
        dirinfos.savetoexcel("dirinfo.xls")
        return 0

if __name__ == '__main__':
    sys.exit(main())
