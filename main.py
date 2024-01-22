# Note: nseindia https://www.nseindia.com/reports-indices-historical-index-data has spaces at end of col name in csv



# # Task 1
# Calculate the Daily Volatility and annualized volatility for the dataset in Python.
# Please use the data file from here.
# You can download similar files from nseindia website.
# Implement the formulas:
# 1. Daily Returns = (current close / previous close) - 1
# (This will be a data series)
# 2. Daily Volatility = Standard Deviation (Daily Returns)
# (This will be a single value)
# 3. Annualized Volatility = Daily Volatility * Square Root (length of data)
# (This will be a single value)
# You can decide on whatever tools/packages you need to implement the above data calculations.

import io
import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


def calculate_volatility(data):
    data['Daily Returns'] = data['Close '].pct_change()
    daily_volatility = data['Daily Returns'].std()
    annualized_volatility = daily_volatility * np.sqrt(len(data))
    return daily_volatility, annualized_volatility

if __name__ == '__main__':

    data = pd.read_csv('NIFTY 50-22-01-2023-to-22-01-2024.csv')
    print(data.head())

    dv, av = calculate_volatility(data)

    print("Daily Volatility:", dv)
    print("Annualized Volatility:", av)


# Task 2
# Make a http endpoint using any one of the python web frameworks – FastAPI or Flask or Django.
# Implement following Functionality:
# 1. Accept a csv file or a parameter with which data can be fetched from directory. (like file used in Task1)
# 2. Compute Daily, Annualized volatility and return these values.
# You can decide on the endpoint name, file headers and other required parameters for the functionality implementation.
# Please mention in the docstrings what parameters name and headers were chosen.
app = Flask(__name__)

@app.route('/volatility', methods=['POST'])
def volatility():
    """
    This web service accepts a CSV file and returns the daily and annualized volatility of the data.
    The CSV file should have a header named 'Close ' that contains the closing prices of the stock or index.

    Python code to send the file:
    import requests
    url = "http://127.0.0.1:5000/volatility"

    file_path = "NIFTY 50-22-01-2023-to-22-01-2024.csv"
    with open(file_path, 'rb') as file:
        files = {'file': (file.name, file, 'text/csv')}
        response = requests.post(url, files=files)
    print(response.text)



    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    # Save the file
    # filename = secure_filename(file.filename)
    # file_path = 'uploads/' + filename
    # file.save(file_path)

    data = pd.read_csv(file)
    daily_volatility, annualized_volatility = calculate_volatility(data)

    return jsonify({"daily_volatility": daily_volatility, "annualized_volatility": annualized_volatility})

if __name__ == '__main__':
    app.run(debug=True)