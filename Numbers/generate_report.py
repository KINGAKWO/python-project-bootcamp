import pandas as pd
from datetime import datetime
import os 


def generate_report():
    # Load dataset
    df = pd.read_csv("number_facts.csv")

    total_entries = len(df)
    unique_numbers = df["number"].nunique()
    most_common = df["number"].mode()[0]
    most_common_fact = df[df["number"] == most_common]["fact"].values[0]

    random_facts = df.sample(min(5, len(df)))["fact"].tolist()

    #  Create report content
    report = f"""
📊 NUMBER FACTS ANALYZER REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total facts collected: {total_entries}
Unique numbers analyzed: {unique_numbers}

Most frequent number: {most_common}
Fact about it: "{most_common_fact}"

Some interesting facts:
{chr(10).join(f'- {fact}' for fact in random_facts)}

Keep learning something new every day! 🚀
"""

    os.makedirs("reports", exist_ok=True)

    with open("reports/summary_report.txt","w", encoding="utf-8") as f:
        f.write(report.strip())
    print("Analytics report generated successfully")

if __name__ == "__main__":
    generate_report()
