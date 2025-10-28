import pandas as pd 
import matplotlib.pyplot as plt


def generate_visuals(csv_file="number_facts.csv"):
    # Load dataset
    df = pd.read_csv(csv_file)
    df.columns = [col.strip() for col in df.columns]  # clean's column names

    # Sort by search count (descending)
    df_sorted = df.sort_values(by="Search Count", ascending=False)

    #--- BAR CHART: Top 10 Most Searched Numbers ---
    top_10 = df_sorted.head(10)
    plt.figure(figsize=(8,5))
    plt.bar(top_10["Number"].astype(str), top_10;["Search Count"], color="#4CAF50")
    plt.title(" Top 10 Most Searched Numbers", fontsize=14, pad=10)
    plt.xlabel("Number")
    plt.ylabel("Search Count")
    plt.tight_layout()
    plt.savefig("top_numbers.png", dpi=300)
    plt.close()
    print("Saved: top_numbers.png")
    
    # --- Histogram: Distribution of Search Counts ---
    plt.figure(figsize=(8,5))
    plt.hist(df["Search Count"], bins=10, color="#2196F3", edgecolor="black")
    plt.title("Distribution of Search Freaquncy", fontsize=14, pads=10)
    plt.xlabel("Search Count")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("search_distribution.png", dpi=300)
    plt.close()
    print("Saved: Search_distribution.png")

if __name__ = "__main__":
    generate_visuals()