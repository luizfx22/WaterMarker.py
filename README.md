# WaterMarker.py

A simple script to add watermark in millions of photos in one click!

## Instructions:
---
1. Create a file called 'settings.json'
2. Write these lines in it:
```json
{
	"sql-settings": {
		"dialect": "mysql",
		"host": "",
		"port": "3306",
		"username": "",
		"database": "",
		"table": ""
	},
	"input-dir": "",
	"thumbnails-dir": "",
	"watermark-image-location": "",
	"output-dir": "/wmarker_results/"
}
```
3. Replace the empty spaces with your actual data, if you're not using MySQL leave it blank!
disclaimer: I didn't comitted settings.json due to sensitive data placed in it!
