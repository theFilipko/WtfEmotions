import sqlite3
import pymongo
import random
import json
import time
import os
import cv2
import numpy
import config
from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from bson.objectid import ObjectId


app = Flask(__name__)
api = Api(app)
# this allows CORS
CORS(app, origins="*", allow_headers=["Access-Control-Allow-Origin"])


def log(text, topic="Server"):
    print("{} - {} - {} - {}".format(
        datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
        os.getppid(),
        topic,
        text
    ), flush=True)


def create_connection(database="wtfemotions.db"):
    """ create a database connection to the SQLite database
        specified by db_file
    :param database: database file
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(database)
        return connection
    except sqlite3.Error as e:
        print(e)

    return None


def create_face(connection, data):
    """
    Create a new face into the faces table
    :param connection:
    :param data:
    :return: data id
    """
    sql = ''' INSERT INTO faces (name,emotions,count)
              VALUES(?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, data)

    return cursor.lastrowid


def get_all_faces(connection):
    """
       Query all rows in the faces table
       :param connection: the Connection object
       :return:
       """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM faces")

    return [row for row in cursor.fetchall()]


def delete_all_faces(connection):
    """
        Delete a face by face id
        :param connection:  Connection to the SQLite database
        :return:
        """
    cursor = connection.cursor()
    cursor.execute("DELETE FROM faces")


def get_random_face(cur, exclude=None):
    """
    Returns a random face from database matching parameters
    :param cur: The Cursor object from database connection
    :param exclude: The id of face to be excluded from search
    :return: path to the selected face
    """
    count = config.COUNT_DATABASE
    if exclude:
        cur.execute("SELECT id, name FROM faces WHERE count=? AND id<>?", (count, exclude))
    else:
        cur.execute("SELECT id, name FROM faces WHERE count=?", (count,))
    faces = [row for row in cur.fetchall()]
    while len(faces) == 0:
        count += 1
        config.COUNT_DATABASE = count
        log("Count: {}".format(count))
        if exclude:
            cur.execute("SELECT id, name FROM faces WHERE count=? AND id<>?", (count, exclude))
        else:
            cur.execute("SELECT id, name FROM faces WHERE count=?", (count,))
        faces = [row for row in cur.fetchall()]

    return random.choice(faces)


class Face(Resource):

    def get(self):
        """
        Handling the GET request
        :return: random image
        """

        conn = create_connection()
        with conn:
            cur = conn.cursor()
            data = get_random_face(cur)
        log("Response: {}".format(data))
        return data, 200

    def put(self):
        """
        Handling the PUT request
        :return: random image
        """

        data_bytes = request.data
        log("Received: {}".format(data_bytes))
        data = json.loads(data_bytes.decode('utf-8'))
        conn = create_connection()

        with conn:
            cur = conn.cursor()
            query = "SELECT * FROM faces WHERE id=?"
            cur.execute(query, (data['id'],))
            face = cur.fetchone()
            facelift = (face[1], face[2] + str(data['emotion']), face[3] + 1, face[0])
            query = "UPDATE faces SET name=?, emotions=?, count=? WHERE id=?"
            cur.execute(query, facelift)
            log("Update done")

            data = get_random_face(cur, data['id'])
        log("Response: {}".format(data))
        return data, 200


class Admin(Resource):

    def __init__(self):
        # make sure the mongod service is set correctly
        self.client = pymongo.MongoClient('localhost', 27018)
        self.db = self.client.faces_database

    def get(self):
        pass

    def post(self):
        r = request
        post = {}
        post["_id"] = ObjectId()
        post["path"] = os.path.join("mongo_db", "data", str(post.get("_id")) + ".jpg")
        post["original_image_name"] = request.files['image'].filename
        post["name"] = request.form.get("name")
        post["emotion"] = request.form.get("emotion")
        post["include"] = request.form.get("include")
        post["updated"] = datetime.utcnow()

        self.db.posts.insert_one(post)

        # read image file string data
        filestr = request.files['image'].read()
        # convert string data to numpy array
        npimg = numpy.fromstring(filestr, numpy.uint8)
        # convert numpy array to image
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        cv2.imwrite(post["path"], image)

        if post["include"] == "on":
            with create_connection() as connection:
                create_face(connection, (post["path"], "", 0))

        return self._respond(post)

    def _respond(self, post):
        return {"id": str(post["_id"]),
                "path": post["path"],
                "original_image_name": post["original_image_name"],
                "name": post["name"],
                "emotion": post["emotion"],
                "include": post["include"],
                "updated": str(post["updated"])}


api.add_resource(Face, '/face')
api.add_resource(Admin, '/admin')

if __name__ == '__main__':
    app.run()
