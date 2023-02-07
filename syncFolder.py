#!/usr/bin/env python

"""
LabKey Experiment Sync Tool

This tool is designed to help sync data from a local computer to workbooks on a LabKey server.  The server should have a series of workbooks,
which will be numbered.  There should be a folder on your computer with subfolders that correspond to workbook IDs.  Any files in the local workbook folder
will be copied to the corresponding workbook, preserving any subfolder.

Usage:
    syncFolder.py --serverUrl=<SERVER_URL> --labkeyFolderPath=<LABKEY_FOLDER> --localFolder=<LOCAL_FOLDER> --username=<USERNAME> --password=<PASSWORD> --jarFile=<JAR_FILE> [--splitFolderNameOnUnderscore] [--lastExecutionFile=<FILE_PATH>]

Oprions:
    -h, --help                                       Show this screen.
    --serverUrl=<SERVER_URL>                         The base URL for your LabKey Server, such as https://labkey.org
    --labkeyFolderPath=<LABKEY_FOLDER>               The full folder path to the target on your server, such as /MyProject/Experiments/
    --localFolder=<LOCAL_FOLDER>                     The full path to the local folder containing your experiments.  The sync tool will scan all subdirectories of this folder and attempt to sync with the server
    --username=<USERNAME>                            The LabKey username
    --password=<PASSWORD>                            The LabKey password
    --jarFile=<JAR_FILE>                             The path to the webdavsync JAR file.  This should be downloaded separately from https://sourceforge.net/projects/webdav-sync/files/latest/download
    --splitFolderNameOnUnderscore                    Normally the sync tool expects the subdirectories to match workbook #s (i.e. 1, 2, 3, 4).  If this switch is provided, the tool will split the foldername using underscore and take the first element as the workbook #.
	--lastExecutionFile=<FILE_PATH>					 Optional. If provided this file will store the last execution time of this script.  Directories with a max modified time less than this value will be skipped.

"""

from docopt import docopt
from natsort import natsorted
import os
import urllib.parse
import subprocess
import time
import datetime

def normalizeSlash(text):
	if text.endswith('/'):
		text = text[:-1]

	if not text.startswith('/'):
		text = '/' + text

	return text

def isInteger(text):
	try:
		return text.isdigit()
	except TypeError:
		return False
		
def processFolder(java, jar, urlBase, subDir, localPath):
	url = urlBase + subDir
	args = [java, '-jar', jar, '-up', '-u', url, '-d', localPath, '-r', '-force']
	#print(' '.join(args))
	code = subprocess.call(args)
	if code > 0:
		print('Non-zero exit: ' + str(code) + ', for path: ' + localPath)

if __name__ == "__main__":
	arguments = docopt(__doc__, version='LabKey Experiment Sync Tool {0}'.format(1.0), options_first=False)

	username=arguments['--username']
	password=arguments['--password']
	baseurl = arguments['--serverUrl']
	containerPath = arguments['--labkeyFolderPath']
	localFolder = arguments['--localFolder']
	lastExecutionFile = arguments['--lastExecutionFile']
	splitFolderNameOnUnderscore = arguments['--splitFolderNameOnUnderscore']
	jar = arguments['--jarFile']

	#Time in seconds
	startMills = int(round(time.time()))	 
	lastRunTime = 0
	if lastExecutionFile != None and os.path.exists(lastExecutionFile):
		with open(lastExecutionFile, 'r') as myfile:
			lines = ''.join(myfile.readlines()).strip()
			if (lines != None and lines != ''):
				lastRunTime = int(lines)
				print('Last run time: ' + str(lastRunTime) + ' / ' + str(datetime.datetime.fromtimestamp(lastRunTime)))
	
	java = 'java'
	
	files = natsorted(os.listdir(localFolder))
	files.reverse()	
	for fileName in files:
		path = os.path.join(localFolder, fileName)
		if os.path.isdir(path):
			pieces = urllib.parse.urlparse(baseurl)
			if splitFolderNameOnUnderscore:
				print('splitting name on underscore')
				fileName = fileName.split('_')[0]

			if not isInteger(fileName):
				print('Non-integer folder, skipping: ' + fileName)
				continue
			
			print('processing: ' + fileName)
			
			maxModifiedTime = 0
			for dirName, subdirList, fileList in os.walk(path):
				maxModifiedTime = max(maxModifiedTime, os.path.getmtime(dirName))
				for fname in fileList:
					maxModifiedTime = max(maxModifiedTime, os.path.getmtime(os.path.join(dirName, fname)))
			
			if maxModifiedTime < lastRunTime:
				print('Folder has not been modified since last sync, skipping')
				continue

			url = pieces.scheme + '://' + urllib.parse.quote(username, safe='') + ':' + urllib.parse.quote(password, safe='') + '@' + pieces.netloc + pieces.path + '_webdav' + normalizeSlash(containerPath) + normalizeSlash(fileName) + '/@files/'			
			try:
				processFolder(java, jar, url, '', path)
			except:
				print('Unable to upload file: ' + path)

		else:
			print('skipping file: ' + fileName)
			
			
	if lastExecutionFile != None:
		with open(lastExecutionFile, 'w') as myfile:
			lastRun = myfile.write(str(startMills))
	
	print('Sync Done')