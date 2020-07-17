#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Response
import pdfAnalyser
import hashGen
import pymongo
import hashlib
import base64
import heapq
import time
threshold = 0.5
debug = False
# if debug:filePath = 'a.pdf'
Client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = Client["BPSS"]
collection = DB['paper']
pdfHash = ''

def getHash(filePath):
	splitSentence = pdfAnalyser.Analyser(filePath)
	total_list = hashGen.hashGenerate(filePath, splitSentence)
	hashNums = len(total_list[0])
	HashList = total_list[0]
	allHash = total_list[1]
	if debug:
		print('[getHash()] Hash Nums (Sentence Nums):\n', len(total_list[0]))
		print('[getHash()] ', len(total_list[0]), 'list:\n', total_list[0])
		print('[getHash()] CombHash:\n', total_list[1])
	return total_list

def fileHash(filePath):
	file = filePath # Location of the file (can be set a different way)
	BLOCK_SIZE = 65536 # The size of each read from the file
	file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
	with open(file, 'rb') as f: # Open the file to read it's bytes
		fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
		while len(fb) > 0: # While there is still data being read from the file
			file_hash.update(fb) # Update the hash
			fb = f.read(BLOCK_SIZE) # Read the next block from the file
	return file_hash.hexdigest()

def checkExist(pdfHash):
	content_pointer = collection.find_one({'pdfHash': pdfHash})
	if debug:print('[checkExist()] ', content_pointer)
	if content_pointer == None: # not exist
		if debug:print("[checkExist()] pdfHash doesn't exist!")
		return False
	else:
		if debug:print("[checkExist()] pdfHash already exist!")
		return True

def checkPlagiarism(TList):
	top3List = ['-','-','-'] #Freq:highest->lowest
	tempPercentageList = [0.0, 0.0, 0.0]
	sumNumerator = 0
	sumDenominator = 0
	for x in collection.find({}):
		if debug:print("[checkPlagiarism()] ", x['_id'], x['title'], x['timestamp'])
		s = len(set(TList[0])&set(x['allList']))
		sumNumerator += s
		sumDenominator += x['numOfSentence']
		plagiarismPercentage = float(s) / float(len(TList[0]))
		for i in range(3):
			if plagiarismPercentage > tempPercentageList[i]:
				tempPercentageList.append(plagiarismPercentage)
				tempPercentageList = heapq.nlargest(3,tempPercentageList)
				top3List[i] = x['title']
				break
		if debug:print("[checkPlagiarism()] ", plagiarismPercentage)
	summary = float(sumNumerator/sumDenominator)
	return [summary, top3List]

def upload(title, pdfHash, TList, ts, summary, top3List):
	collection = DB['paper']
	uploadData = {
	'title': title,
	'numOfSentence': len(TList[0]),
	'pdfHash': pdfHash,
	'allList': TList[0],
	'combHash:': TList[1],
	'timestamp': ts,
	'summary': summary,
	'top3List': top3List
	}
	return collection.insert(uploadData)

def flask_func(title, content, timestamp = time.time()):
	print('_Title: ', title)
	receivePdf = open('./bin/temp.fdp', 'bw')
	receivePdf.write(base64.b64decode(content))
	receivePdf.close()
	pdfHash = fileHash('./bin/temp.fdp')
	if checkExist(pdfHash):
		if debug:print('[flask_func()] status: This paper has been submitted before.')
		return ['This paper has been submitted before.','-','Exist']
	else:
		TList = getHash('./bin/temp.fdp')
		resp = checkPlagiarism(TList)
		if debug: print('[flask_func()] response@checkPlagiarism(): ', resp)
		res = upload(title, pdfHash, TList, timestamp, resp[0], resp[1])
		if debug: print('[flask_func()] Paper uploaded! Obj_Id@Mongo:', res)
		return ['Sent!\nThe top3List: '+str(resp[1]),str(len(TList[0])),resp[0]]