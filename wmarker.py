# Import stuff
import sqlalchemy as sql
import cv2
import json

"""
	Instructions:
		1. Create a file called 'settings.json'
		2. Write these lines in it:
			{
				"mysql": {
					"url": "",
					"user": "",
					"password": "",
					"db": ""
				},
				"input-dir": "",
				"thumbnails-dir": "",
				"output-dir": "/wmarker_results/"
			}
		3. Replace the empty spaces with your actual data, if you're not using MySQL leave it blank!
		disclaimer: I didn't comitted settings.json due to sensitive data placed in it!
"""

with open('settings.json', 'r+') as settingsFile:
	settings = json.load(settingsFile)
	settingsFile.close()

mysql = settings["mysql"]
print(mysql)