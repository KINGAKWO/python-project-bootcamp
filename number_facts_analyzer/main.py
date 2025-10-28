import requests
import json
import os
from datetime import datetime
import csv

FACTS_FILE = "number_facts.json"
CSV_FILE = "number_facts.csv"


def get_number_fact(number):
    """Fetches a fun fact about a given number using the Numbers API"""
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


def load_existing_facts(filename=FACTS_FILE):
    """Loads existing facts if the JSON file exists"""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


def save_fact_to_json(facts, filename=FACTS_FILE):
    """Saves new facts with timestamps and counts to the JSON file."""
    all_facts = load_existing_facts(filename)

    for num, info in facts.items():
        if num in all_facts:
            all_facts[num]["count"] += 1
            all_facts[num]["timestamp"] = info["timestamp"]
        else:
            info["count"] = 1
            all_facts[num] = info

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(all_facts, file, indent=4)

    print(f"\nSaved {len(facts)} new facts to {filename}!")


def export_to_csv():
    """Export all saved facts to a CSV file for analysis."""
    facts = load_existing_facts()
    if not facts:
        print("No data available to export")
        return

    write_header = not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Number", "Fact", "Timestamp", "Search Count"])
        for number, info in facts.items():
            writer.writerow([number, info["fact"], info["timestamp"], info["count"]])

    print(f"\nData successfully exported to {CSV_FILE}")


def view_saved_facts(filename=FACTS_FILE):
    """Displays all previously saved facts."""
    facts = load_existing_facts(filename)
    if not facts:
        print("No saved facts yet. Try fetching some first!")
        return

    print("\nSaved Number Facts:")
    for number, info in sorted(facts.items(), key=lambda x: int(x[0])):
        print(f"{number}: {info['fact']} (x{info['count']} searches, saved on {info['timestamp']})")


def is_number(s):
    """Checks if a string can be converted to an integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False


def current_timestamp():
    """Returns the current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    while True:
        print("\n=== Number Facts Tracker ===")
        print("1. Get Number Fact")
        print("2. View Saved Facts")
        print("3. Export data to CSV")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            user_input = input("Enter numbers separated by commas (e.g., 5,4,3,2,1): ")
            numbers = [num.strip() for num in user_input.split(",") if is_number(num.strip())]

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
                        "timestamp": current_timestamp()
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
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()