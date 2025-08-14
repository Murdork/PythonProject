# <student_number>_T1.py
# COM4018 – Task 1: Main user menu (no imports)

def show_menu():
    print("\nMain Menu")
    print("1. Customer and hire details")
    print("2. Earnings report")
    print("0. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("Customer and hire details selected")
            # (Task 2 functionality will be integrated here later.)
        elif choice == "2":
            print("Earnings report selected")
            # (Task 3 functionality will be integrated here later.)
        elif choice == "0":
            print("You have chosen to exit. Goodbye.")
            break
        else:
            print("Wrong value entered. Try again.")

if __name__ == "__main__":
    main()
