
# Import stuff
import os
import json
# from sqlalchemy.sql import select
# import sqlalchemy as db
from PIL import Image
import time

class WMarkr:
    def __init__(self):
        # Reading JSON
        with open('settings.json', 'r+') as settingsFile:
            self.settings = json.load(settingsFile)
            settingsFile.close()
        self.sql_settings = self.settings["sql-settings"]

        with open('AllImages.json', 'r+') as allImagesIdx:
            self.allIMG = json.load(allImagesIdx)
            allImagesIdx.close()

    def connect(self):
        # SQLAlchemy engine instantiation
        dialect = self.sql_settings['dialect']
        username = self.sql_settings['username']
        password = self.sql_settings['password']
        host = self.sql_settings['host']
        port = str(self.sql_settings['port'])
        database = self.sql_settings['database']

        connection_string = dialect + "://" + username + ":" + password + "@" + host + ":" + port + "/" + database
        print(connection_string)
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

    def addWatermarkImage(self, file_path, output_path):
        try:
            base_image = Image.open(file_path)
        except Exception as e:
            print("Skipped image!")
            return False
        
        logo = Image.open(self.settings["watermark-image-location"])
        logo = logo.convert('RGBA')

        imageWidth, imageHeight = base_image.width, base_image.height
        logoWidth, logoHeight = logo.width, logo.height
        
        base_image.paste(logo, (imageWidth - logoWidth - 10, imageHeight - logoHeight - 10), logo)
        
        filename = file_path[file_path.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((output_path, filename))
        try:
            base_image.save(p)
            print("\nImage saved successfully!", end="\r")
            return True
        except Exception as e:
            print(e)
            return False

    def addWatermarkThumbnail(self, file_path, output_path):
        try:
            base_image = Image.open(file_path)
        except Exception as e:
            print("Skipped image!")
            return False
        logo = Image.open(self.settings["watermark-image-location"])
        logo.thumbnail((110, 110), Image.ANTIALIAS)
        logo = logo.convert('RGBA')

        imageWidth, imageHeight = base_image.width, base_image.height
        logoWidth, logoHeight = logo.width, logo.height

        base_image.paste(logo, (imageWidth - logoWidth - 5,
                                imageHeight - logoHeight - 5), logo)

        filename = file_path[file_path.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((output_path, filename))

        try:
            base_image.save(p)
            print("\nThumbnail saved successfully!", end="\r")
            return True
        except Exception as e:
            print(e)
            return False

bnchmrk_start = time.time()

marker = WMarkr()

query = marker.allIMG

for _ in query:
    image_tuple = (_["IMGT"], _["IMG"])
    thumbnail_path = marker.settings["thumbnails-dir"] + image_tuple[0]
    actual_image = marker.settings["input-dir"] + image_tuple[1]

    if not marker.addWatermarkImage(actual_image, marker.settings["output-main-dir"]):
        print("Skipped file " + image_tuple[1] + "!")
    if not marker.addWatermarkThumbnail(thumbnail_path, marker.settings["output-thumb-dir"]):
        print("Skipped thumbnail " + image_tuple[0] + "!")


bnchmrk_end = time.time() - bnchmrk_start
print("It took about" + str(bnchmrk_end) +" seconds to mark all images!")
