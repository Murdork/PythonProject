# ==========================================
# COM4018 – Introduction to Programming
# Tasks 2 & 3 integrated program (enhanced I/O)
#
# Save as: <student_number>.py  (Tasks 2 & 3)
# Provide a separate <student_number>_T1.py for Task 1 placeholder menu.
# Do not import any modules.
#
# ------------ HOW TO USE ------------
# 1) From the main menu choose "Customer & hire details".
# 2) Enter customer details on ONE line, comma/quoted separated:
#      name, phone, house_no, postcode, card_last4
#    Examples:
#      Bob Barker,07970263076,3b,WA9 RY,1452
#      "B Barker","07970 263076","3b","WA9 RY","1452"
#
# 3) Enter item lines, ONE per line, then press ENTER on a blank line to finish.
#    Quantity is MANDATORY. Format:
#      CODE, nights, quantity, overdue_days, returned_late(y/n)
#    Examples:
#      DCH, 3, 2, 0, n
#      BAS, 2, 1, 1, y
#
# PRICING RULES:
#   • Base hire:     daily_rate * nights * quantity
#   • Overdue:       daily_rate * overdue_days * quantity
#   • Returned late: +50% of daily_rate * quantity (once per item line)
#   All money handled in pence to avoid float issues.
# ==========================================

# -----------------------------
# Read-only equipment catalogue
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
# Mutable store
# -----------------------------
HIRE_RECORDS = []        # list of hire dicts
_next_customer_id = 101  # simple running ID

# -----------------------------
# Utilities (no imports)
# -----------------------------
def money(pence):
    """Format integer pence as £x.xx."""
    pounds = pence // 100
    pp = pence % 100
    return f"£{pounds}.{pp:02d}"

def show_catalog():
    """Print the read-only equipment list."""
    print("\nAvailable equipment (read-only)")
    print("CODE  ITEM                                        RATE/DAY")
    print("----  ------------------------------------------  --------")
    for it in CATALOG:
        print(f"{it['code']:<4}  {it['name']:<42}  {money(it['daily_p']):>8}")

def find_item(code):
    """Return the catalog dict for a code, or None."""
    code = code.strip().upper()
    for item in CATALOG:
        if item["code"] == code:
            return item
    return None

def catalog_codes():
    """Return a comma-separated list of known codes."""
    return ", ".join([it["code"] for it in CATALOG])

def display_menu():
    """Main menu UI."""
    print("\n=== Main Menu ===")
    print("1) Customer & hire details")
    print("2) Earnings report")
    print("3) Exit")

def read_choice():
    """Read a menu choice (1–3). Return int or None if invalid."""
    s = input("Select an option (1-3): ").strip()
    if not s.isdigit():
        return None
    n = int(s)
    return n if n in (1, 2, 3) else None

def read_yes_no(prompt="(y/n): "):
    """Read 'y' or 'n' (accepts 'yes'/'no'). Returns 'y' or 'n'."""
    while True:
        s = input(prompt).strip().lower()
        if s in ("y", "n", "yes", "no"):
            return "y" if s.startswith("y") else "n"
        print("Please enter 'y' or 'n'.")

def parse_csv_line(line):
    """
    Basic CSV parser supporting quotes and commas (no imports).
    Returns list of fields with surrounding spaces trimmed.
    """
    fields = []
    buf = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == '"':
                # doubled quote -> literal "
                if i + 1 < len(line) and line[i+1] == '"':
                    buf.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                buf.append(ch)
        else:
            if ch == '"':
                in_quotes = True
            elif ch == ',':
                fields.append("".join(buf).strip())
                buf = []
            else:
                buf.append(ch)
        i += 1
    fields.append("".join(buf).strip())
    return fields

def read_customer_line():
    """
    Prompt for customer details on one comma/quoted line:
      name, phone, house_no, postcode, card_last4
    Minimal validation: non-empty name; phone >=7 digits; card_last4 exactly 4 digits.
    If the user presses Enter on a blank line, ask to confirm returning to the main menu.
    Returns a dict of details, or None if the user chooses to return to the menu.
    """
    print("\nEnter customer details (one line, comma/quoted separated):")
    print("  name, phone, house_no, postcode, card_last4")
    while True:
        raw = input("> ").strip()
        if raw == "":
            if read_yes_no("No details entered. Return to main menu (y/n)? ") == "y":
                return None
            else:
                # stay in the loop and ask again
                continue

        parts = parse_csv_line(raw)
        if len(parts) != 5:
            print("Expected 5 fields. Example: Bob Barker,07970263076,3b,WA9 RY,1452")
            continue

        name, phone, house_no, postcode, card_last4 = [p.strip() for p in parts]
        digits_phone = "".join(ch for ch in phone if ch.isdigit())
        digits_card  = "".join(ch for ch in card_last4 if ch.isdigit())

        if not name:
            print("Name cannot be empty.")
            continue
        if len(digits_phone) < 7:
            print("Phone must have at least 7 digits.")
            continue
        if len(digits_card) != 4:
            print("Card last 4 must be exactly 4 digits.")
            continue

        return {
            "customer_name": name,
            "phone": digits_phone,
            "house_no": house_no,
            "postcode": postcode,
            "card_last4": digits_card,
        }

def parse_item_line(raw):
    """
    Mandatory item format (quantity required):
      code, nights, quantity, overdue_days, returned_late
    Returns (line_dict, None) or (None, error_message).
    """
    parts = [p.strip() for p in parse_csv_line(raw)]
    if len(parts) != 5:
        return None, "Expected 5 fields: CODE, nights, quantity, overdue_days, returned_late(y/n)"
    code = parts[0].upper()
    item = find_item(code)
    if not item:
        return None, f"Unknown code '{code}'. Known: {catalog_codes()}"
    try:
        nights = int(parts[1])
        qty = int(parts[2])
        overdue_days = int(parts[3])
        late = parts[4].lower()
        if nights < 1:
            return None, "Nights must be ≥ 1."
        if qty < 1:
            return None, "Quantity must be ≥ 1."
        if overdue_days < 0:
            return None, "Overdue days must be ≥ 0."
        if late not in ("y", "n", "yes", "no"):
            return None, "Returned-late must be 'y' or 'n'."
        returned_late = late.startswith("y")
    except ValueError:
        return None, "Numeric fields must be whole numbers."
    line = {
        "code": item["code"],
        "name": item["name"],
        "daily_p": item["daily_p"],
        "nights": nights,
        "qty": qty,
        "overdue_days": overdue_days,
        "returned_late": "y" if returned_late else "n",
    }
    return line, None

def compute_line_cost(line):
    """
    Compute costs for one item line.
    Returns (base_p, overdue_p, late_penalty_p, line_total_p).
    """
    base = line["daily_p"] * line["nights"] * line["qty"]
    overdue = line["daily_p"] * line["overdue_days"] * line["qty"]
    late_penalty = (line["daily_p"] * line["qty"]) // 2 if line["returned_late"] == "y" else 0
    total = base + overdue + late_penalty
    return base, overdue, late_penalty, total

# -----------------------------
# Task 2 — Hire workflow
# -----------------------------
def run_hire_flow():
    """
    Option 1: capture customer + any number of item lines, show summary, confirm, save.
    If the user chooses to return at the (blank) customer prompt, go back to the main menu.
    """
    global _next_customer_id

    show_catalog()
    cust = read_customer_line()
    if cust is None:
        print("Returning to main menu.")
        return

    print("\nEnter item lines (one per line). Format (quantity is mandatory):")
    print("  CODE, nights, quantity, overdue_days, returned_late(y/n)")
    print("Press ENTER on a blank line when done.\n")

    lines = []
    while True:
        raw = input("Item > ").strip()
        if raw == "":
            if len(lines) == 0:
                print("Please enter at least one item line.")
                continue
            break
        line, err = parse_item_line(raw)
        if err:
            print("  " + err)
            continue
        # compute & attach costs now (so summary is ready)
        base, overdue, late_penalty, total = compute_line_cost(line)
        line["base_p"] = base
        line["overdue_p"] = overdue
        line["late_penalty_p"] = late_penalty
        line["line_total_p"] = total
        lines.append(line)

    # Build hire record (but confirm first)
    rec = {
        "customer_id": _next_customer_id,
        "lines": lines,
        "customer_name": cust["customer_name"],
        "phone": cust["phone"],
        "house_no": cust["house_no"],
        "postcode": cust["postcode"],
        "card_last4": cust["card_last4"],
    }

    # ---- Summary + confirmation
    print("\nSummary of hire (NOT SAVED YET)")
    print("--------------------------------")
    print(f"Customer ID : {rec['customer_id']}")
    print(f"Name        : {rec['customer_name']}")
    print(f"Phone       : {rec['phone']}")
    print(f"Address     : {rec['house_no']}, {rec['postcode']}")
    print(f"Card (last4): {rec['card_last4']}")
    print("\nItems:")
    grand = 0
    print("CODE  ITEM                                NIGHT  QTY  OVERDUE  LATE  BASE     OVERDUE   PENALTY   LINE TOTAL")
    print("----  ----------------------------------  -----  ---  -------  ----  -------  --------  --------  ----------")
    for ln in lines:
        grand += ln["line_total_p"]
        print(f"{ln['code']:<4}  {ln['name'][:34]:<34}  "
              f"{ln['nights']:>5}  {ln['qty']:>3}  {ln['overdue_days']:>7}  {ln['returned_late']:^4}  "
              f"{money(ln['base_p']):>7}  {money(ln['overdue_p']):>8}  {money(ln['late_penalty_p']):>8}  {money(ln['line_total_p']):>10}")
    print("-" * 104)
    print(f"TOTAL DUE: {money(grand)}")

    sure = read_yes_no("\nConfirm and save this hire? (y/n): ")
    if sure == "n":
        print("Cancelled. Nothing saved.")
        return

    rec["total_p"] = grand
    HIRE_RECORDS.append(rec)
    _next_customer_id += 1
    print("Saved.")

# -----------------------------
# Task 3 — Earnings report
# -----------------------------
def _summary_by_hire():
    """Yield tuples for summary-by-hire rows and grand total."""
    grand = 0
    rows = []
    for r in HIRE_RECORDS:
        items_count = sum(ln["qty"] for ln in r["lines"])
        total_p = sum(ln["line_total_p"] for ln in r["lines"])
        grand += total_p
        rows.append((r["customer_id"], r["customer_name"], items_count, total_p))
    return rows, grand

def _summary_by_item():
    """
    Aggregate across all hires by item code:
    returns dict code -> {name, hires, qty, item_days, late_lines, revenue_p}
    where item_days = (nights + overdue_days) * qty
    """
    agg = {}
    for r in HIRE_RECORDS:
        for ln in r["lines"]:
            code = ln["code"]
            a = agg.get(code)
            if a is None:
                a = {
                    "name": ln["name"],
                    "hires": 0,
                    "qty": 0,
                    "item_days": 0,
                    "late_lines": 0,
                    "revenue_p": 0,
                }
                agg[code] = a
            a["hires"] += 1
            a["qty"] += ln["qty"]
            a["item_days"] += (ln["nights"] + ln["overdue_days"]) * ln["qty"]
            if ln["returned_late"] == "y":
                a["late_lines"] += 1
            a["revenue_p"] += ln["line_total_p"]
    return agg

def run_earnings_report():
    """Option 2: print Summary by Hire, Summary by Item, and Detail lines."""
    if not HIRE_RECORDS:
        print("\nNo hire data to report yet.")
        return

    # ---- Section 1: SUMMARY BY HIRE
    rows, grand_total = _summary_by_hire()
    print("\n=== Earnings Report (Summary by Hire) ===")
    print("ID   CUSTOMER                 ITEMS  GRAND TOTAL")
    print("---  ------------------------  -----  -----------")
    for cid, name, items_count, total_p in rows:
        print(f"{cid:>3}  {name[:24]:<24}  {items_count:>5}  {money(total_p):>11}")
    print("-" * 54)
    print(f"TOTAL EARNINGS: {money(grand_total)}")

    # ---- Section 2: SUMMARY BY ITEM (figure-style aggregation)
    agg = _summary_by_item()
    print("\nSummary by Item:")
    print("CODE  ITEM                         HIRES  QTY  ITEM-DAYS  LATE  REVENUE")
    print("----  ---------------------------  -----  ---  ---------  ----  --------")
    for code in sorted(agg.keys()):
        a = agg[code]
        print(f"{code:<4}  {a['name'][:27]:<27}  {a['hires']:>5}  {a['qty']:>3}  {a['item_days']:>9}  {a['late_lines']:>4}  {money(a['revenue_p']):>8}")

    # ---- Section 3: DETAIL LINES (ALL ENTERED DATA)
    print("\nDetail lines (all entered data):")
    print("ID   CODE  ITEM                                NIGHT  QTY  OVERDUE  LATE  BASE     OVERDUE   PENALTY   LINE TOTAL")
    print("---  ----  ----------------------------------  -----  ---  -------  ----  -------  --------  --------  ----------")
    for r in HIRE_RECORDS:
        for ln in r["lines"]:
            print(f"{r['customer_id']:>3}  {ln['code']:<4}  {ln['name'][:34]:<34}  "
                  f"{ln['nights']:>5}  {ln['qty']:>3}  {ln['overdue_days']:>7}  {ln['returned_late']:^4}  "
                  f"{money(ln['base_p']):>7}  {money(ln['overdue_p']):>8}  {money(ln['late_penalty_p']):>8}  {money(ln['line_total_p']):>10}")

# -----------------------------
# Main loop
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
