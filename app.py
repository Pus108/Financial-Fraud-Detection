from flask import Flask, render_template, request
import pandas as pd
import os
import streamlit as st
st.title("Fraud Detection Dashboard")


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return "No file uploaded", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Load dataset
    df = pd.read_csv(filepath)

    # Assuming dataset has "Class" column: 1 = Fraud, 0 = Non-Fraud
    total = len(df)
    fraud = df["Class"].sum()
    nonfraud = total - fraud

    # Send data to frontend
    return render_template("result.html", 
                           total=total, 
                           fraud=fraud, 
                           nonfraud=nonfraud)


if __name__ == "__main__":
    app.run(debug=True)
