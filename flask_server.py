#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import time
import logging
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask import Response
from flask_cors import CORS
from flask_cors import cross_origin
import main
debug = False
OPlog = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)
runTime = time.strftime("%Y-%m-%d_%H-%M-%S")

if OPlog:
	logcsv = open("./log/logfile_"+runTime+".csv", 'w', encoding="utf-8", errors='ignore')
	# 11 items in csv
	logcsv.write('PdfFileName,FileSize,SentenceNums,Summary,pdfWriteTime(ms),pdfHashTime(ms),checkExist_Time(ms),getHash_Time(ms),checkPlagiarism_Time(ms),upload_Time(ms),flask_func_Time(ms)\n')
	logcsv.close()
CORS(app)
@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def getData():
	global logcsv, runTime
	sTime = time.time()
	if request.method == 'POST':
		receviceData = request.get_data()
		# if debug:print(receviceData.decode())
		data = json.loads(receviceData.decode())
		sTime = time.time()
		resp = main.flask_func(data['title'], data['content'], sTime)
		eTime = time.time()
		strSize = ''
		intSize = os.path.getsize('./bin/temp.fdp')
		if intSize > 1048576: # MB
			strSize = '%.3f'%(intSize/1048576)+' MB'
		elif intSize > 1024: #KB
			strSize = '%.3f'%(intSize/1024)+' KB'
		else:
			strSize = intSize+' B'
		if OPlog:
			logcsv = open("./log/logfile_"+runTime+".csv", 'a', encoding="utf-8", errors='ignore')
			logcsv.write(data['title']+','+strSize+','+resp['NOS']+','+resp['summary']+','+resp['pdfWriteTime']+','+resp['pdfHashTime']+','+resp['checkExist()Time']+','+resp['getHash()Time']+','+resp['checkPlagiarism()Time']+','+resp['upload()Time']+','+str((eTime-sTime)*1000)+'\n')
			logcsv.close()
		#resp['paperStatus'] is the return msg for BPSS WebPage
		return Response(resp['paperStatus'],status=200)
	else:
		return Response(
        'only support post request!',
        status=200
    	)

if __name__ =='__main__':
	app.run(host='0.0.0.0', debug=True, port=58088)