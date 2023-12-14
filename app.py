from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
import time

app = Flask(__name__)

names = ["papper", "rock", "scissor"]

def predict_label(img_path):
    model = load_model('model.h5')
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
	
    start_time = time.time()
    res = model.predict(img_array)
    end_time = time.time()

    label = np.argmax(res)
    prediction_time = round(end_time - start_time, 4)

    return names[label], prediction_time

# routes
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return "About You..!!!"

@app.route("/submit", methods=['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/" + img.filename
        img.save(img_path)
        p, prediction_time = predict_label(img_path)

    return render_template("index.html", prediction=p, img_path=img_path, prediction_time=prediction_time)

if __name__ == '__main__':
    app.run(debug=True)