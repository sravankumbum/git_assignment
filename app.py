from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment variables. Please check your .env file.")

client = MongoClient(MONGO_URI)

db = client["app_db"]        # Database
collection = db["Users"]       # Collection

Data = 'DataFile.json'  


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return render_template("form.html", error="All fields are required")

        # Insert into MongoDB
        collection.insert_one({
            "name": name,
            "email": email
        })

        return redirect(url_for('success'))

    except Exception as e:
        return render_template("form.html", error=str(e))


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/api', methods=['GET'])
def get_data():
    try:
        with open(Data, 'r') as file:
            data = json.load(file)
            
        return {"message": "Data retrieved successfully", "data": data}
    except FileNotFoundError:
        return {"message": "DataFile.json not found. Please create the file and add some data."}

if __name__ == '__main__':
    app.run(debug=True)