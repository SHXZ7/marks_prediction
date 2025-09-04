from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.pipeline.predict_pipeline import CustomData, prediction_pipeline

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST']) 
def predict():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )

            pred_df = data.get_data_as_data_frame()
            print(pred_df)
            print("Before Prediction")

            predict_pipeline = prediction_pipeline()
            print("Pipeline initiated")
            results = predict_pipeline.predict(pred_df)
            print("after Prediction")
            return render_template('home.html', results=results[0])
        except Exception as e:
            # Print the exception to the console and show it in the browser for debugging
            print(f"Error during prediction: {e}")
            return render_template('home.html', results=f"Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

