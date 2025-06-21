from flask import Flask, render_template, request
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename.endswith(('.csv', '.xlsx')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)

                preview = df.head(10).to_html(classes='data')
                summary = df.describe().to_html(classes='data')
                return render_template('preview.html', preview=preview, summary=summary, filename=filename)

            except Exception as e:
                return f"❌ Error reading file: {e}"

        return "❌ Invalid file type. Please upload CSV or Excel."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
