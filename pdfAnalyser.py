#!/usr/bin/python
# -*- coding: utf-8 -*-
import PyPDF2
import hashlib
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import regularExpression as RE
debug = False
def AnalyserOld(filePath):
    file = open(filePath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    numberOfPages = pdfReader.getNumPages()
    if debug:print('[Analyser()] Pages:', numberOfPages)
    allData = []
    for page in range(numberOfPages):
        pageObj = pdfReader.getPage(page)
        page_content = pageObj.extractText()
        print(page_content)
        if debug:print('[Analyser()] Page ',page, 'content:\n',page_content)
        normal_content = RE.splitIntoSentences(page_content)
        for i in range(len(normal_content)):
            allData.append(normal_content[i])
    file.close()
    if debug:print('[Analyser()]', allData)
    return allData

def Analyser(filePath):
    normal_content = ''
    allData = []
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()
    with io.StringIO() as retstr:
        with TextConverter(rsrcmgr, retstr, codec=codec,laparams=laparams) as device:
            with open(filePath, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                caching = True
                pagenos = set()
                for page in PDFPage.get_pages(fp,pagenos,caching=caching,check_extractable=True):
                    interpreter.process_page(page)
                page_content = retstr.getvalue()
                normal_content = RE.splitIntoSentences(page_content)
    for i in range(len(normal_content)):
        allData.append(normal_content[i])
    if debug:print('[Analyser()]', allData)
    return allData