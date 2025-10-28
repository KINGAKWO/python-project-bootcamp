import schedule
import time
import os
from datetime import datetime


def run_pipeline():
    print(f"🔁 Running Number Facts Update — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    #Run your main data collection and visualization scripts
    os.system("python3 main.py")
    os.system("python3 generate_visuals.py")
    os.system("python generate_report.py")


    print("update complete\n")


# Schedule the task 
schedule.every().day.at("10:00").do(run_pipeline)

print(" Scheduler started...... waiting for next run.")

while True:
    schedule.run_pending()
    time.sleep(30)