# app.py
from flask import Flask, render_template
from clustering import run_clustering

app = Flask(__name__)

@app.route('/')
def home():
    results = run_clustering()  # Run analysis each time page loads
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
