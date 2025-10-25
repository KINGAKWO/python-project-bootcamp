from flask import Flask, render_template, send_from_directory, redirect, url_for 
import os

app = Flask(__name__)


@app.route("/")
def home():
    with open("reports/summary_report.txt", "r", encoding="utf-8") as f:
        report_content = f.read()
    return render_template("index.html", report=report_content)


@app.route("/visuals/<path:filename>")
def visual():
    return send_from_directory("visualizations", "number_trends.png")


@app.route("/update", methods=["POST"])
def update():
    os.system("python3 main.py")
    os.system("python3 generate_visuals.py")
    os.system("python generate_report.py")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
