
# Import stuff
import os
import json
from sqlalchemy.sql import select
import sqlalchemy as db
import numpy as np
import cv2

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
            connection = engine.connect()
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

    def addWaterMark(self, file_path):
        watermark = cv2.imread(self.settings["watermark-image-location"], cv2.IMREAD_UNCHANGED)
        (wH, wW) = watermark.shape[:2]

        # r = 120 / float(wH)
        # dim = (int(wH * r), wH)
        
        # # Return the resized image
        # watermark = cv2.resize(watermark, dim, interpolation=cv2.INTER_AREA)

        (B, G, R, A) = cv2.split(watermark)
        B = cv2.bitwise_and(B, B, mask=A)
        G = cv2.bitwise_and(G, G, mask=A)
        R = cv2.bitwise_and(R, R, mask=A)

        watermark = cv2.merge([B, G, R, A])

        image = cv2.imread(file_path)
        (h, w) = image.shape[:2]
        image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])

        overlay = np.zeros((h, w, 4), dtype="uint8")
        overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark

        output = image.copy()
        cv2.addWeighted(overlay, 0.4, output, 1.0, 0, output)
        
        filename = file_path[file_path.rfind(os.path.sep) + 1:]
        p = os.path.sep.join((self.settings["output-dir"], filename))
        cv2.imwrite(p, output)


marker = WMarkr()
marker.addWaterMark(marker.settings["input-dir"])
# result = marker.query(marker.connect())

