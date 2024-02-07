import quantstats as qs
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def calc_portfolio(price, col, strategy):
    price['New_Close'] = price[col].pct_change()
    price['Date'] = pd.to_datetime(price['Date'], format='%d/%m/%Y')
    price = price.set_index('Date')
    stock = price['New_Close']

    output_file_path = f'output/full_report_{strategy}.html'
    qs.reports.html(stock, title=f"Portfolio Analysis {strategy}", output=output_file_path)
    return output_file_path


@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        # If the user does not select a file, the browser may send an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Read the uploaded CSV file using Pandas
        price = pd.read_csv(file)

        # Call the calc_portfolio function
        html_report_path = calc_portfolio(price, 'Close', 'alpha')

        # Read the generated HTML report
        # Read the generated HTML report
        with open(html_report_path, 'r') as f:
            html_content = f.read()
        # Delete the HTML file
        os.remove(html_report_path)

        return html_content, 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({'error': 'Failed to process file', 'exception': str(e)})


if __name__ == '__main__':
    app.run(debug=True,port=8000)


