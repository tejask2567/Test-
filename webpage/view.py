from DeepImageSearch import Index, LoadData, SearchImage
from flask import request, redirect, render_template, Flask
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import base64
from werkzeug.utils import secure_filename
import cv2 as cv

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "C:/Users/tejas/OneDrive/Desktop/Intership/webpage/static/Images"
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Star')
def Star():
    return render_template('Star.html')


var_List = []


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':

        image = request.files['myFile']
        if image.filename == '':
            print("file name is invalid")
            return redirect(request.url)
        filename = secure_filename(image.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename))
        path = os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename)
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imwrite('Black/Img.jpg', gray)
        results = SearchImage().get_similar_images(
            image_path='Black/Img.jpg', number_of_images=1)
        res = list(results.values())[0]
        var_List.append(res)

        return render_template("index.html", filename=filename)

    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        res2 = var_List.pop()
        processed_text = res2.split('\\')[1].split('_')[0]
        return render_template('index.html', processed_text=processed_text)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
