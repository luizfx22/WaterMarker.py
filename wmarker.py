
# Import stuff
import os
import json
from sqlalchemy.sql import select
import sqlalchemy as db
from PIL import Image

class WMarkr:
    def __init__(self):
        # Reading JSON
        with open('settings.json', 'r+') as settingsFile:
            self.settings = json.load(settingsFile)
            settingsFile.close()
        self.sql_settings = self.settings["sql-settings"]

    def connect(self):
        # SQLAlchemy engine instantiation
        connection_string = f"{self.sql_settings['dialect']}://{self.sql_settings['username']}:{self.sql_settings['password']}@{self.sql_settings['host']}:{self.sql_settings['port']}/{self.sql_settings['database']}"
        try:
            engine = db.create_engine(connection_string)
            self.connection = engine.connect()
            metadata = db.MetaData()
            table = db.Table(self.sql_settings["table"],
                metadata, autoload=True, autoload_with=engine)
            return table

        except Exception as e:
            print("Error!")
            print(e)
            return

    def query(self, table):
        try:
            self.query = select([table.columns.IMGT, table.columns.IMG]).where(table.columns.Inativo != 1)
            self.resproxy = self.connection.execute(self.query)
            self.resset = self.resproxy.fetchall()
            return self.resset
            
        except Exception as e:
            print("Error!")
            print(e)
            return

    def addWatermarkImage(self, file_path):
        base_image = Image.open(file_path)
        logo = Image.open(self.settings["watermark-image-location"])
        logo = logo.convert('RGBA')

        imageWidth, imageHeight = base_image.width, base_image.height
        logoWidth, logoHeight = logo.width, logo.height
        
        base_image.paste(logo, (imageWidth - logoWidth - 10, imageHeight - logoHeight - 10), logo)
        
        filename = file_path[file_path.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((self.settings["output-main-dir"], filename))

        base_image.save(p)

    def addWatermarkThumbnail(self, file_path):
        base_image = Image.open(file_path)
        logo = Image.open(self.settings["watermark-image-location"])
        logo.thumbnail((110, 110), Image.ANTIALIAS)
        logo = logo.convert('RGBA')

        imageWidth, imageHeight = base_image.width, base_image.height
        logoWidth, logoHeight = logo.width, logo.height

        base_image.paste(logo, (imageWidth - logoWidth - 5,
                                imageHeight - logoHeight - 5), logo)

        filename = file_path[file_path.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((self.settings["output-thumb-dir"], filename))

        base_image.save(p)


marker = WMarkr()
conn = marker.connect()

query = marker.query(conn)

for image_tuple in query:
    

# marker.addWatermarkThumbnail(marker.settings["thumbnails-dir"])
# result = marker.query(marker.connect())

