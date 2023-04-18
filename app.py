from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
from helpers import manipulate_features
#Load the trained model using joblib.load():
km_4 = joblib.load("km_4_model.joblib")

#Create a new Flask app object:
app = Flask(__name__)

# Define a route for the home page, where users can input their data:
@app.route("/")
def home():
    return render_template("index.html")

# Define a route to handle the form submission and make predictions using the model:
@app.route("/predict", methods=["POST"])
def predict():
    # get the input data from the form
    features = []
    for i, value in enumerate(request.form.values()):
        try:
            if i == 0:
                features.append(value)
            else:
                features.append(float(value))
        except ValueError:
            # handle the error by setting a default value or returning an error message
            features.append(0.0)

    # manipulate the features as necessary (e.g. do any preprocessing)
    features = manipulate_features(features)
    # make a prediction using the model
    #prediction = km_4.predict(np.array(features).reshape(1, -1))[0]
    prediction = km_4.predict(features)
    # render the prediction on a new page
    return render_template("result.html", prediction=prediction)


# Manipulating features

if __name__ == "__main__":
    app.run(debug=True)


