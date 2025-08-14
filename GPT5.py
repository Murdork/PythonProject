""""
COM4018 – Introduction to Programming
Final Submission Code

This file combines:
- Task 1: Main menu system
- Task 2A & 2B: Hire workflow
- Task 3A & 3B: Earnings report

Replace `<student_number>` in the filename with your actual student number before submission.
"""

from typing import Optional, Dict, Any, List, Tuple

# -----------------------------
# Read‑only reference catalogue
# -----------------------------
EQUIPMENT_CATALOG: Tuple[Dict[str, Any], ...] = (
    {"code": "TEN", "name": "2‑Person Tent",  "daily_rate": 120_000},
    {"code": "TAR", "name": "Tarp Shelter",   "daily_rate":  50_000},
    {"code": "STV", "name": "Portable Stove", "daily_rate":  35_000},
    {"code": "RDS", "name": "Rod & Reel Set", "daily_rate":  80_000},
    {"code": "BTK", "name": "Basic Tackle Kit","daily_rate":  25_000},
)

# -----------------------------
# Mutable store for hire records
# -----------------------------
HIRES: List[Dict[str, Any]] = []
_next_id: int = 1

# -----------------------------
# Shared utilities
# -----------------------------

def display_menu() -> None:
    print("\n=== Main Menu ===")
    print("1) Customer & hire details")
    print("2) Earnings report")
    print("3) Exit")


def pause() -> None:
    input("\nPress Enter to continue...")


def read_choice(prompt: str = "Select an option (1-3): ") -> Optional[int]:
    raw = input(prompt).strip()
    if not raw.isdigit():
        return None
    val = int(raw)
    return val if val in (1, 2, 3) else None


def list_codes() -> str:
    return ", ".join(item["code"] for item in EQUIPMENT_CATALOG)


def show_catalog() -> None:
    print("\nAvailable Equipment (read‑only)")
    print("CODE  ITEM                         RATE/DAY (VND)")
    print("----  ---------------------------  -------------")
    for item in EQUIPMENT_CATALOG:
        print(f"{item['code']:<4}  {item['name']:<27}  {item['daily_rate']:>13}")


def find_catalog_item(code: str) -> Optional[Dict[str, Any]]:
    code = code.upper()
    for item in EQUIPMENT_CATALOG:
        if item["code"] == code:
            return item
    return None


def read_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty. Try again.")


def read_positive_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            val = int(raw)
            if val >= 1:
                return val
        print("Enter a whole number ≥ 1.")


def read_phone(prompt: str = "Phone number: ") -> str:
    while True:
        phone = input(prompt).strip()
        if len(phone) >= 7 and all(ch.isdigit() or ch in "+ -()" for ch in phone):
            return phone
        print("Enter a valid phone number (min 7 chars; digits/+, -, (), space allowed).")


def compute_total(daily_rate: int, days: int, quantity: int) -> int:
    return daily_rate * days * quantity

# -----------------------------
# Task 2 – Hire workflow (Option 1)
# -----------------------------

def run_hire_flow() -> None:
    global _next_id

    if len(HIRES) >= 10:
        print("You already have 10 or more records. You may still add more for testing.")
        proceed = input("Add another record (Y/N)? ").strip().upper()
        if proceed != "Y":
            return

    show_catalog()

    customer_name = read_nonempty("Customer name: ")
    phone = read_phone()

    while True:
        code = input(f"Enter item code ({list_codes()}): ").strip().upper()
        item = find_catalog_item(code)
        if item:
            break
        print("Unknown code. Please try again.")

    days = read_positive_int("Number of days (≥1): ")
    quantity = read_positive_int("Quantity (≥1): ")

    total = compute_total(item["daily_rate"], days, quantity)

    print("\nSummary of hire:")
    print(f"  Customer : {customer_name}")
    print(f"  Phone    : {phone}")
    print(f"  Item     : {item['name']} ({item['code']})")
    print(f"  Days     : {days}")
    print(f"  Quantity : {quantity}")
    print(f"  Daily    : {item['daily_rate']}")
    print(f"  TOTAL    : {total}")

    confirm = input("Confirm and save (Y/N)? ").strip().upper()
    if confirm != "Y":
        print("Cancelled. Nothing saved.")
        return

    record = {
        "id": _next_id,
        "customer_name": customer_name,
        "phone": phone,
        "item_code": item["code"],
        "item_name": item["name"],
        "daily_rate": item["daily_rate"],
        "days": days,
        "quantity": quantity,
        "total_cost": total,
    }
    HIRES.append(record)
    _next_id += 1

    print(f"Saved. Hire ID: {record['id']}")
    print(f"Current records: {len(HIRES)}")

# -----------------------------
# Task 3 – Earnings report (Option 2)
# -----------------------------

def _group_by_item() -> Dict[str, Dict[str, Any]]:
    groups: Dict[str, Dict[str, Any]] = {}
    for r in HIRES:
        code = r["item_code"]
        g = groups.setdefault(code, {
            "name": r["item_name"],
            "hires": 0,
            "quantity": 0,
            "days": 0,
            "revenue": 0,
        })
        g["hires"] += 1
        g["quantity"] += r["quantity"]
        g["days"] += r["days"] * r["quantity"]
        g["revenue"] += r["total_cost"]
    return groups


def run_earnings_report() -> None:
    if not HIRES:
        print("\nNo hire data to report.")
        return

    groups = _group_by_item()

    print("\n=== Earnings Report ===")
    print("CODE  ITEM                         HIRES  QTY  ITEM‑DAYS       REVENUE (VND)")
    print("----  ---------------------------  -----  ---  ---------  ------------------")

    grand_revenue = 0
    grand_hires = 0
    grand_qty = 0
    grand_itemdays = 0

    for code in sorted(groups.keys()):
        g = groups[code]
        print(f"{code:<4}  {g['name']:<27}  {g['hires']:>5}  {g['quantity']:>3}  {g['days']:>9}  {g['revenue']:>18}")
        grand_revenue += g["revenue"]
        grand_hires += g["hires"]
        grand_qty += g["quantity"]
        grand_itemdays += g["days"]

    print("-" * 74)
    print(f"TOTAL{'':<33}  {grand_hires:>5}  {grand_qty:>3}  {grand_itemdays:>9}  {grand_revenue:>18}")

    print("\nDetail (most recent first):")
    print("ID   CUSTOMER                  ITEM (CODE)     DAYS  QTY      TOTAL")
    print("---  ------------------------  -------------  -----  ---  ----------")
    for r in reversed(HIRES):
        print(f"{r['id']:>3}  {r['customer_name'][:24]:<24}  {r['item_name'][:13]:<13}  {r['days']:>5}  {r['quantity']:>3}  {r['total_cost']:>10}")

# -----------------------------
# Main loop
# -----------------------------

def main() -> None:
    while True:
        display_menu()
        choice = read_choice()
        if choice is None:
            print("Invalid option, try again.")
            continue

        if choice == 1:
            run_hire_flow()
            pause()
        elif choice == 2:
            run_earnings_report()
            pause()
        elif choice == 3:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
