# ==========================================
# Issues/ design considerations.
#Item entry, add equipment lines (but only accepts one), doesnt support hiring different equipment for different times, if an item is overdue it needs to know when it is returned (to caculate penalty, obviously 1 person can have 2 items for different periods and different overdue lengths)
# maybe confirmation before summary, not sure if summary necessary but nice touch IMO

# COM4018 – Introduction to Programming
# Tasks 2 & 3 integrated program
#
# IMPORTANT FOR SUBMISSION:
# - Save this file as <student_number>.py (no suffix) for Tasks 2 & 3.
# - Provide a separate <student_number>_T1.py for Task 1 placeholder menu.
# - Do not import any modules (per brief).
# ==========================================

# -----------------------------
# Read-only equipment catalogue (Figure 2)
# Prices stored in pence to avoid float issues
# -----------------------------
CATALOG = (
    {"code": "DCH", "name": "Day chairs",                           "daily_p": 1500},
    {"code": "BCH", "name": "Bed chairs",                           "daily_p": 2500},
    {"code": "BAS", "name": "Bite Alarm (set of 3)",                "daily_p": 2000},
    {"code": "BA1", "name": "Bite Alarm (single)",                  "daily_p":  500},
    {"code": "BBT", "name": "Bait Boat",                            "daily_p": 6000},
    {"code": "TNT", "name": "Camping tent",                         "daily_p": 2000},
    {"code": "SLP", "name": "Sleeping bag",                         "daily_p": 2000},
    {"code": "R3T", "name": "Rods (3lb TC)",                        "daily_p": 1000},
    {"code": "RBR", "name": "Rods (Bait runners)",                  "daily_p":  500},
    {"code": "REB", "name": "Reels (Bait runners)",                 "daily_p": 1000},
    {"code": "STV", "name": "Camping Gas stove (Double burner)",    "daily_p": 1000},
)

# -----------------------------
# Mutable store (Tasks 2 & 3)
# -----------------------------
HIRE_RECORDS = []       # list of dicts (one per hire)
_next_customer_id = 101 # matches the sample style

# -----------------------------
# Helpers (no imports allowed)
# -----------------------------
def money(pence):
    pounds = pence // 100
    pp = pence % 100
    return f"£{pounds}.{pp:02d}"

def find_item(code):
    code = code.strip().upper()
    for item in CATALOG:
        if item["code"] == code:
            return item
    return None

def catalog_codes():
    return ", ".join([it["code"] for it in CATALOG])

def show_catalog():
    print("\nAvailable equipment (read-only)")
    print("CODE  ITEM                                        RATE/DAY")
    print("----  ------------------------------------------  --------")
    for it in CATALOG:
        print(f"{it['code']:<4}  {it['name']:<42}  {money(it['daily_p']):>8}")

def read_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Value cannot be empty. Try again.")

def read_positive_int(prompt):
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            n = int(s)
            if n >= 1:
                return n
        print("Enter a whole number ≥ 1.")

def read_yes_no(prompt="(y/n): "):
    while True:
        s = input(prompt).strip().lower()
        if s in ("y", "n"):
            return s
        print("Please enter 'y' or 'n'.")

def read_digits(prompt, length=None, min_len=None):
    while True:
        s = input(prompt).strip().replace(" ", "")
        if s.isdigit():
            if length is not None and len(s) == length:
                return s
            if min_len is not None and len(s) >= min_len:
                return s
            if length is None and min_len is None:
                return s
        if length is not None:
            print(f"Enter exactly {length} digits.")
        elif min_len is not None:
            print(f"Enter at least {min_len} digits.")
        else:
            print("Digits only, please.")

def display_menu():
    print("\n=== Main Menu ===")
    print("1) Customer & hire details")
    print("2) Earnings report")
    print("3) Exit")

def read_choice():
    s = input("Select an option (1-3): ").strip()
    if not s.isdigit():
        return None
    n = int(s)
    return n if n in (1, 2, 3) else None

# -----------------------------
# Pricing rules (scenario)
# • First night: 100% daily
# • Additional nights: 50% daily each
# • Late return (after 2pm): add one extra 50% daily per item (per hire)
# -----------------------------
def cost_for_line(daily_p, nights, qty):
    first = daily_p * qty
    additional_nights = max(0, nights - 1)
    additional = (daily_p * qty * additional_nights) // 2
    return first + additional

def late_extra_for_hire(lines):
    extra = 0
    for ln in lines:
        extra += (ln["daily_p"] * ln["qty"]) // 2
    return extra

# -----------------------------
# Task 2 — Hire workflow (Option 1)
# (Data structures per Figure 3; accessible to Task 3)
# -----------------------------
def run_hire_flow():
    global _next_customer_id

    show_catalog()
    print("\nEnter customer & hire details")

    # Minimal details per Figure 3
    name = read_nonempty("Customer name: ")
    phone = read_digits("Phone number (min 7 digits): ", min_len=7)
    house_no = read_nonempty("House number: ")
    postcode = read_nonempty("Postcode: ")
    card_last4 = read_digits("Card (last 4 digits): ", length=4)

    print("\nAdd equipment lines (at least one).")
    lines = []
    while True:
        code = read_nonempty(f"Enter item code ({catalog_codes()}): ").upper()
        item = find_item(code)
        if not item:
            print("Unknown code. Try again.")
            continue
        qty = read_positive_int("Quantity (≥1): ")
        lines.append({
            "code": item["code"],
            "name": item["name"],
            "daily_p": item["daily_p"],
            "qty": qty,
        })
        more = read_yes_no("Add another item? (y/n): ")
        if more == "n":
            if len(lines) == 0:
                print("At least one line is required.")
                continue
            break

    nights = read_positive_int("Number of nights (≥1): ")
    returned_on_time = read_yes_no("Returned on time (y/n): ")

    # Compute per-line and totals
    total_lines_p = 0
    for ln in lines:
        ln_cost = cost_for_line(ln["daily_p"], nights, ln["qty"])
        ln["line_total_p"] = ln_cost
        total_lines_p += ln_cost

    extra_p = 0
    if returned_on_time == "n":
        extra_p = late_extra_for_hire(lines)

    grand_total_p = total_lines_p + extra_p

    # Build and store record
    record = {
        "customer_id": _next_customer_id,
        "customer_name": name,
        "phone": phone,
        "house_no": house_no,
        "postcode": postcode,
        "card_last4": card_last4,
        "nights": nights,
        "returned_on_time": returned_on_time,
        "extra_charge_p": extra_p,
        "lines": lines,
        "total_p": grand_total_p,
    }
    HIRE_RECORDS.append(record)
    _next_customer_id += 1

    # Confirmation
    print("\nSummary of hire")
    print("----------------")
    print(f"Customer ID : {record['customer_id']}")
    print(f"Name        : {name}")
    print(f"Nights      : {nights}")
    print("Items       :")
    for ln in lines:
        print(f"  - {ln['name']} × {ln['qty']} @ {money(ln['daily_p'])}/night"
              f" => {money(ln['line_total_p'])}")
    if extra_p > 0:
        print(f"Late extra  : {money(extra_p)}  (50% of daily per item)")
    print(f"TOTAL DUE   : {money(grand_total_p)}")

# -----------------------------
# Task 3 — Earnings report (Option 2)
# Prints ALL data entered so far (no filters), similar to Figure 4
# -----------------------------
def run_earnings_report():
    if not HIRE_RECORDS:
        print("\nNo hire data to report yet.")
        return

    # ---- Section 1: SUMMARY BY HIRE (matches Figure 4 essentials)
    print("\n=== Earnings Report (Summary by Hire) ===")
    print("ID   CUSTOMER                 NIGHTS  ON-TIME  EXTRA (late)  HIRE TOTAL")
    print("---  ------------------------  ------  -------  -----------  ----------")

    grand_total = 0
    for r in HIRE_RECORDS:
        print(f"{r['customer_id']:>3}  {r['customer_name'][:24]:<24}  "
              f"{r['nights']:>6}  {r['returned_on_time']:>7}  "
              f"{money(r['extra_charge_p']):>11}  {money(r['total_p']):>10}")
        grand_total += r["total_p"]

    print("-" * 74)
    print(f"TOTAL EARNINGS: {money(grand_total)}")

    # ---- Section 2: DETAIL LINES (ALL ENTERED DATA)
    print("\nDetail lines (all items entered):")
    print("ID   CODE  ITEM                                DAILY   QTY  NIGHTS   LINE TOTAL")
    print("---  ----  ----------------------------------  ------  ---  ------   ----------")
    for r in HIRE_RECORDS:
        for ln in r["lines"]:
            print(f"{r['customer_id']:>3}  {ln['code']:<4}  {ln['name'][:34]:<34}  "
                  f"{money(ln['daily_p']):>6}  {ln['qty']:>3}  {r['nights']:>6}   {money(ln['line_total_p']):>10}")

    # ---- Section 3: (Optional) CUSTOMER INFO recap (to show ALL captured fields)
    print("\nCustomer details captured:")
    print("ID   NAME                      PHONE        HOUSE  POSTCODE  CARD(Last4)")
    print("---  ------------------------  -----------  -----  --------  ----------")
    for r in HIRE_RECORDS:
        print(f"{r['customer_id']:>3}  {r['customer_name'][:24]:<24}  "
              f"{r['phone']:<11}  {r['house_no']:<5}  {r['postcode']:<8}  {r['card_last4']:<10}")

# -----------------------------
# Main loop (Task 1 integrated)
# (Your separate Task 1 file should only print the placeholder messages)
# -----------------------------
def main():
    while True:
        display_menu()
        choice = read_choice()
        if choice is None:
            print("Invalid option, try again.")
            continue

        if choice == 1:
            run_hire_flow()
        elif choice == 2:
            run_earnings_report()
        elif choice == 3:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
