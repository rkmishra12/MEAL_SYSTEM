# MEAL SYSTEM 
import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

# Path to the database
database = "mealp/database.csv"

def take_input():
    datei = input("Enter date (YYYY-MM-DD): ")
    if "today" in datei.lower():
        datei = str(date.today())
    daymeal = int(input("Enter day meal rate: "))
    nightmeal = int(input("Enter night meal amount: "))
    description = input("Enter description (if any): ")
    with open(database, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datei, daymeal, nightmeal, description])

def get_info():
    print("\n\t\t-: MEAL STATEMENTS :-")
    print("-" * 54)
    print("Date    Day_Meal   Night_Meal   Description \n")
    with open(database, "r") as f:
        read = csv.reader(f)
        next(read)
        for text in read:
            print("\t".join(text))

def analyze_data():
    try:
        # Load data into a Pandas DataFrame
        data = pd.read_csv(database, names=["Date", "Day_Meal", "Night_Meal", "Description"], skiprows=1)
        data["Total_Meal"] = data["Day_Meal"] + data["Night_Meal"]

        print("\n\t-: MEAL DATA ANALYSIS :-")
        print("-" * 54)
        
        # Basic statistics
        print("\nBasic Statistics:")
        print(data.describe())

        # Maximum and minimum total meal costs
        max_meal = data.loc[data['Total_Meal'].idxmax()]
        min_meal = data.loc[data['Total_Meal'].idxmin()]

        print(f"\nDay with Maximum Total Meal Cost: {max_meal['Date']} - {max_meal['Total_Meal']}")
        print(f"Day with Minimum Total Meal Cost: {min_meal['Date']} - {min_meal['Total_Meal']}")

        # Pie chart of descriptions
        desc_counts = data['Description'].value_counts()
        plt.pie(desc_counts, labels=desc_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Meal Description Distribution')
        plt.show()

        # Line plot for daily meal trends
        plt.plot(data['Date'], data['Day_Meal'], label='Day Meal', marker='o')
        plt.plot(data['Date'], data['Night_Meal'], label='Night Meal', marker='x')
        plt.xticks(rotation=45)
        plt.title('Day Meal vs Night Meal Trends')
        plt.xlabel('Date')
        plt.ylabel('Meals')
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Bar plot for total meal cost
        plt.bar(data['Date'], data['Total_Meal'], color='skyblue')
        plt.xticks(rotation=45)
        plt.title('Total Meals per Day')
        plt.xlabel('Date')
        plt.ylabel('Total Meals')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error during analysis: {e}")


def export_data():
    try:
        # Load data into a Pandas DataFrame
        data = pd.read_csv(database, names=["Date", "Day_Meal", "Night_Meal", "Description"], skiprows=1)
        # Ask user for the file format
        print("\nChoose the format to export the data:")
        print("1. CSV File")
        print("2. Excel File")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            filename = input("Enter the filename for the CSV file (e.g., meals.csv): ")
            data.to_csv(filename, index=False)
            print(f"Data successfully exported to {filename}")
        elif choice == "2":
            filename = input("Enter the filename for the Excel file (e.g., meals.xlsx): ")
            data.to_excel(filename, index=False, engine="openpyxl")
            print(f"Data successfully exported to {filename}")
        else:
            print("Invalid choice. Returning to menu.")

    except Exception as e:
        print(f"Error exporting data: {e}")


def total_costs():
    try:
        # Load data into a Pandas DataFrame
        data = pd.read_csv(database, names=["Date", "Day_Meal", "Night_Meal", "Description"], skiprows=1)
        total_day_meal_cost = data['Day_Meal'].sum()
        total_night_meal_cost = data['Night_Meal'].sum()
        total_meal_cost = total_day_meal_cost + total_night_meal_cost

        print("\n\t-: TOTAL MEAL COSTS :-")
        print(f"Total Day Meal Cost: {total_day_meal_cost}")
        print(f"Total Night Meal Cost: {total_night_meal_cost}")
        print(f"Total Meal Cost: {total_meal_cost}")

    except Exception as e:
        print(f"Error calculating total costs: {e}")



def generate_summaries():
    try:
        # Load data into a Pandas DataFrame
        data = pd.read_csv(database, names=["Date", "Day_Meal", "Night_Meal", "Description"], skiprows=1)
        data["Date"] = pd.to_datetime(data["Date"])  # Convert Date column to datetime format

        print("\nGenerate Summary for:")
        print("1. Monthly")
        print("2. Weekly")
        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            # Group by month
            data["Month"] = data["Date"].dt.to_period("M")
            monthly_summary = data.groupby("Month")[["Day_Meal", "Night_Meal"]].sum()
            monthly_summary["Total_Meal"] = monthly_summary["Day_Meal"] + monthly_summary["Night_Meal"]
            print("\nMonthly Summary:")
            print(monthly_summary)
        elif choice == "2":
            # Group by week
            data["Week"] = data["Date"].dt.to_period("W")
            weekly_summary = data.groupby("Week")[["Day_Meal", "Night_Meal"]].sum()
            weekly_summary["Total_Meal"] = weekly_summary["Day_Meal"] + weekly_summary["Night_Meal"]
            print("\nWeekly Summary:")
            print(weekly_summary)
        else:
            print("Invalid choice. Returning to menu.")

    except Exception as e:
        print(f"Error generating summaries: {e}")


def menu():
    while True:
        print("\n\t-: MEAL MANAGEMENT SYSTEM MENU :-")
        print("1. Add Meal Record")
        print("2. View Meal Records")
        print("3. Analyze Data")
        print("4. Show Total Costs")
        print("5. Export Data")
        print("6. Generate Summaries")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            take_input()
        elif choice == "2":
            get_info()
        elif choice == "3":
            analyze_data()
        elif choice == "4":
            total_costs()
        elif choice == "5":
            export_data()
        elif choice == "6":
            generate_summaries()
        elif choice == "7":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

menu()
