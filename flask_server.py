#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import time
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

app = Flask(__name__)
runTime = time.strftime("%Y-%m-%d_%H-%M-%S")
if OPlog:
	logcsv = open("./log/logfile_"+runTime+".csv", 'w', encoding="utf-8", errors='ignore')
	logcsv.write('PdfFileName,FileSize,SentenceNums,Summary,OpenFileTS, StartCheckTS, EndCheckTS, CheckTime(ms), TotalTime(ms), \n')
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
		if ('timestamp' in data):
			sTime = time.time()
			resp = main.flask_func(data['title'], data['content'], data['timestamp'])
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
				logcsv.write(data['title']+','+strSize+','+str(resp[1])+','+str(resp[2])+','+str(data['timestamp']*1000)+','+str(sTime*1000)+','+str(eTime*1000)+','+str((eTime-sTime)*1000)+','+str(float(eTime-data['timestamp'])*1000)+'\n')
				logcsv.close()
			return Response(resp[0],status=200)
		else:
			strSize = ''
			intSize = os.path.getsize('./bin/temp.fdp')
			if intSize > 1048576: # MB
				strSize = '%.3f'%(intSize/1048576)+' MB'
			elif intSize > 1024: #KB
				strSize = '%.3f'%(intSize/1024)+' KB'
			else:
				strSize = intSize+' B'
			sTime = time.time()
			resp = main.flask_func(data['title'], data['content'], sTime)
			eTime = time.time()
			if OPlog:
				logcsv = open("./log/logfile_"+runTime+".csv", 'a', encoding="utf-8", errors='ignore')
				logcsv.write(data['title']+','+strSize+','+str(resp[1])+','+str(resp[2])+','+str('-')+','+str(sTime*1000)+','+str(eTime*1000)+','+str((eTime-sTime)*1000)+','+str('-')+'\n')
				logcsv.close()
			return Response(resp[0],status=200)
	else:
		return Response(
        'only support post request!',
        status=200
    	)

if __name__ =='__main__':
	app.run(host='0.0.0.0', debug=True, port=58088)