from flask import Flask, render_template, send_from_directory, redirect, url_for 
import os
import sys
import subprocess


app = Flask(__name__)


@app.route("/")
def home():
    report_content = "No report available yet."
    report_path = os.path.join("reports", "summary_report.txt")
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_content = f.read()
    return render_template("index.html", report=report_content)


@app.route("/visual")
def visual():
    return send_from_directory("visualizations", "number_trends.png")


@app.route("/update", methods=["POST"])
def update():
    subprocess.run([sys.executable, "main.py"])
    subprocess.run([sys.executable, "generate_visuals.py"])
    subprocess.run([sys.executable, "generate_report.py"])

if __name__ == "__main__":
    app.run(debug=True)
