import requests
import json
import os
from datetime import datetime
import csv

FACTS_FILE = "number_facts.json"
CSV_FILE = "number_facts.csv"


def get_number_fact(number):
    """fetches a fun fact about a given number using the NuMBERS API"""
    url = f"http://numbersapi.com/{number}?json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["text"]

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except ValueError:
        print("Error: Could not parse response.")
    return None


def load_existing_facts(filename="number_facts.json"):
    """Loads existing facts if the JSON FILE exists"""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


def save_fact_to_json(facts, filename="number_facts.json"):
    """Saves new facts with timestamps to the JSON file."""

    # load existing facts if file exists
    all_facts = load_existing_facts(filename)
    # add or update fact
    all_facts.update(facts)

    # save back to file
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(all_facts, file, indent=4)

    print(f"\n saved {len(facts)}  new facts to {filename}!")


def export_to_csv():
    """Export all saved facts to a csv file for analysis."""
    facts = load_existing_facts()
    if not facts:
        print("No data available to export")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Fact", "Timestamp", "Search Count"])
        for number, info in facts.items():
            writer.writerow([number, info["fact"], info["timestamp"], info["count"]])

    print(f"\n Data successfully exported to {CSV_FILE}")


def view_saved_facts(filename="number_facts.json"):
    """Displays all previously saved facts."""
    facts = load_existing_facts(filename)
    if not facts:
        print("NO saved facts found yet.")
        return

    print("\n Saved Number facts:")
    for number, info in facts.items():
        print(f"{number}: {info['fact']} (x{info['count']} searches, saved on {info['timestamp']})")


def main():
    while True:
        print("\n=== Number Facts Tracker ===")
        print("1. Get Number Fact")
        print("2. View Saved Facts")
        print("3. Export data to CSV")
        print("4. Exit")

        choice = input("choose an option: ").strip()

        if choice == "1":
            user_input = input("Enter numbers seperated by commas (e.g., 5,4,3,2,1): ")
            numbers = [num.strip() for num in user_input.split(",") if num.strip().isdigit()]

            if not numbers:
                print("Please enter valid numeric values.")
                continue

            facts_to_save = {}

            for num in numbers:
                fact = get_number_fact(num)
                if fact:
                    print(f"{num}: {fact}")
                    facts_to_save[num] = {
                        "fact": fact,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

            if facts_to_save:
                save_fact_to_json(facts_to_save)

        elif choice == "2":
            view_saved_facts()

        elif choice == "3":
            export_to_csv()

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
