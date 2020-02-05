# Import stuff
from sqlalchemy.sql import select
import sqlalchemy as db
import cv2
import json


with open('settings.json', 'r+') as settingsFile:
	settings = json.load(settingsFile)
	settingsFile.close()

sql_settings = settings["sql-settings"]

# SQLAlchemy engine instantiation
connection_string = f"{sql_settings['dialect']}://{sql_settings['username']}:{sql_settings['password']}@{sql_settings['host']}:{sql_settings['port']}/{sql_settings['database']}"
try:
	engine = db.create_engine(connection_string)
	connection = engine.connect()
	metadata = db.MetaData()
	table = db.Table(sql_settings["table"], metadata, autoload=True, autoload_with=engine)
except Exception as e:
	print("Error!")
	print(e)
	exit()
	
try:
	query = select([table.columns.IMGT, table.columns.IMG]).where(table.columns.Inativo != 1)
	ResProxy = connection.execute(query)
	ResSet = ResProxy.fetchall()
	print(ResSet)
	print(len(ResSet))
	
except Exception as e:
	print("Error!")
	print(e)
	exit()
