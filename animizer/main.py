from wsgiref import simple_server
from flask import Flask, request, render_template, send_from_directory, redirect, send_file
import os
from flask_cors import CORS, cross_origin
# import test
import cartoonize
# import cv2
import shutil
# from PIL import Image
# import sys
# import numpy as np
# import glob

app = Flask(__name__)
CORS(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
@cross_origin()
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
@cross_origin()
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    if os.path.isdir(target):
        shutil.rmtree(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    myFiles = []
    for file in request.files.getlist("file"):
        filename = file.filename
        print("filename", filename)
        destination = "".join([target, filename])
        print("destination", destination)
        file.save(destination)
        myFiles.append(filename)
    print(myFiles)

    return render_template("upload.html", image_names=myFiles)

@app.route('/upload/<filename>')
@cross_origin()
def send_original_image(filename):
    return send_from_directory("images", filename)

@app.route('/complete/<filename>')
@cross_origin()
def send_processed_image(filename):
    load_folder = os.path.join(APP_ROOT, 'images/')
    newImg = cartoonize.cartoonize(load_folder, filename)
    return send_from_directory("images", newImg)

# good practise to have this: this means this will only run if its run directly (and not called from somewhere else)
#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    from os import environ
    app.run(debug=False, port=environ.get("PORT", 5000), host='0.0.0.0')


