import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def analyze_numbers(csv_file="number_facts.csv", output_file="number_report.txt"):
    # Load data
    df = pd.read_csv(csv_file)
    df.columns = [col.strip() for col in df.columns]

    # Preview
    print("Dataset Preview:\n", df.head(), "\n")
    print("Data Overview:\n")
    print(df.info(), "\n")
    print("Summary Statistics:\n", df.describe(), "\n")

    # Metrics
    unique_numbers = df["Number"].nunique()
    top_numbers = df.sort_values(by="Search Count", ascending=False).head(3)
    avg_search = df["Search Count"].mean()
    first_search, last_search = df["Timestamp"].min(), df["Timestamp"].max()

    # Popular threshold
    threshold = avg_search + df["Search Count"].std()
    popular_numbers = df[df["Search Count"] > threshold]["Number"].tolist()

    # Print insights
    print(f"Total unique numbers searched: {unique_numbers}")
    print("\nTop 3 most searched numbers:\n", top_numbers[["Number", "Search Count"]])
    print(f"\nAverage search count per number: {avg_search:.2f}")
    print(f"\nSearch timeline:\nFirst: {first_search}\nLast: {last_search}")
    print(f"\n🌟 Popular numbers (above-average searches): {popular_numbers or 'None detected'}")

    # Plot
    df_sorted = df.sort_values(by="Search Count", ascending=False)
    plt.bar(df_sorted["Number"].astype(str), df_sorted["Search Count"])
    plt.title("Most Searched Numbers")
    plt.xlabel("Number")
    plt.ylabel("Search Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # Report
    most_searched = ", ".join(
        f"{row['Number']} ({row['Search Count']} times)" 
        for _, row in top_numbers.iterrows()
    )
    report = f"""
    Number Facts Analysis Report Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ============================
    Total Unique Numbers Searched: {unique_numbers}
    Most Searched Numbers: {most_searched}
    Average Search Count: {avg_search:.2f}
    Data range: {first_search} to {last_search}

    🌟 Popular numbers (above-average searches):
    {', '.join(map(str, popular_numbers)) if popular_numbers else 'None detected'}

    Visualization:
    Chart saved as: {plot_path}
    ---
    Summary:
    This report provides insights into the frequency and diversity of number searches.
    It automatically updates whenever new data is added to the CSV.
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport generated successfully! Check {output_file}")


if __name__ == "__main__":
    analyze_numbers()