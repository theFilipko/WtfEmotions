import sqlite3
import os


connection = sqlite3.connect("wtfemotions.db")
sql = ''' INSERT INTO faces (name,emotions,count)
              VALUES(?,?,?) '''
with connection:
    cursor = connection.cursor()
    image_names = os.listdir("data")
    for image_name in image_names:
        data = (image_name, "", 0)
        cursor.execute(sql, data)

