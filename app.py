from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import bikeshare  # Import bikeshare module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Retrieve user inputs from the form
    city = request.form['city']
    month = request.form['month']
    day = request.form['day']

    # Load and filter data using the bikeshare module
    df = bikeshare.load_data(city, month, day)

    if df is not None:
        statistics = bikeshare.calculate_statistics(df)
        raw_data = bikeshare.display_raw_data(df)
        return render_template('results.html', statistics=statistics, raw_data=raw_data)

if __name__ == "__main__":
    app.run(debug=True)
