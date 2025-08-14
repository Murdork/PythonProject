# Filename: <student_number>.py

# Reference data (read-only)
equipment_list = {
    "Tent": 15.00,
    "Sleeping Bag": 5.00,
    "Fishing Rod": 10.00,
    "Camping Stove": 8.00,
    "Lantern": 4.00
}

# Hire records will be stored in this list
hire_records = []

def display_menu():
    print("\n--- Main Menu ---")
    print("1. Customer and hire details")
    print("2. Earnings report")
    print("3. Exit")

def hire_equipment():
    print("\n--- Hire Equipment ---")
    while len(hire_records) < 10:
        name = input("Enter customer name: ").strip()
        if not name:
            print("Customer name cannot be empty.")
            continue

        print("\nAvailable equipment:")
        for item, price in equipment_list.items():
            print(f"- {item} (£{price:.2f} per day)")

        equipment = input("Enter equipment name: ").strip()
        if equipment not in equipment_list:
            print("Invalid equipment name.")
            continue

        try:
            days = int(input("Enter number of days for hire: "))
            if days <= 0:
                print("Duration must be a positive integer.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        total_cost = equipment_list[equipment] * days
        hire_records.append({
            "name": name,
            "equipment": equipment,
            "days": days,
            "cost": total_cost
        })

        print(f"Successfully added hire for {name}: {equipment} for {days} days (£{total_cost:.2f})")

        more = input("Add another hire? (y/n): ").lower()
        if more != 'y':
            break

def earnings_report():
    print("\n--- Earnings Report ---")
    if not hire_records:
        print("No hire records available.")
        return

    total_earnings = 0
    print("{:<20} {:<15} {:<10} {:<10}".format("Customer", "Equipment", "Days", "Cost (£)"))
    print("-" * 60)
    for record in hire_records:
        print("{:<20} {:<15} {:<10} {:<10.2f}".format(
            record["name"], record["equipment"], record["days"], record["cost"]
        ))
        total_earnings += record["cost"]

    print("-" * 60)
    print(f"Total Earnings: £{total_earnings:.2f}")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            hire_equipment()
        elif choice == "2":
            earnings_report()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()