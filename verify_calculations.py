#!/usr/bin/env python3
"""
Manual calculation verification for the hire management system.
This script will manually calculate the expected totals from Test Data.txt
and compare them with the expected results.
"""

# Import the catalog and calculation function from the main program
import sys
import os

# Equipment catalog (from your program)
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

def find_item(code):
    """Return the catalog dict for a code, or None."""
    code = code.strip().upper()
    for item in CATALOG:
        if item["code"] == code:
            return item
    return None

def money(pence):
    """Format integer pence as £x.xx."""
    pounds = pence // 100
    pp = pence % 100
    return f"£{pounds}.{pp:02d}"

def compute_line_cost(daily_p, nights, qty, overdue_days, returned_late):
    """Calculate costs exactly as in your program."""
    base = daily_p * nights * qty
    overdue = daily_p * overdue_days * qty  # 100% of daily rate for overdue
    late_penalty = (daily_p * qty) // 2 if returned_late else 0
    total = base + overdue + late_penalty
    return base, overdue, late_penalty, total

# Test cases from Test Data.txt
test_cases = [
    {
        "customer_id": 101,
        "customer_name": "Ted Danson",
        "items": [
            ("DCH", 3, 1, 1, True),   # Day chairs, 3 nights, qty 1, 1 overdue, late
            ("BBT", 5, 2, 3, False),  # Bait Boat, 5 nights, qty 2, 3 overdue, not late
            ("SLP", 3, 1, 1, False),  # Sleeping bag, 3 nights, qty 1, 1 overdue, not late
            ("TNT", 3, 1, 1, False),  # Camping tent, 3 nights, qty 1, 1 overdue, not late
        ],
        "expected_total": "£1187.50"
    },
    {
        "customer_id": 102,
        "customer_name": "Bob Barker", 
        "items": [
            ("TNT", 3, 4, 0, False),  # Camping tent, 3 nights, qty 4, 0 overdue, not late
            ("STV", 3, 1, 0, False),  # Gas stove, 3 nights, qty 1, 0 overdue, not late
        ],
        "expected_total": "£270.00"
    },
    {
        "customer_id": 103,
        "customer_name": "Angela Lansbury",
        "items": [
            ("BAS", 4, 1, 0, True),   # Bite Alarm set, 4 nights, qty 1, 0 overdue, late
            ("BA1", 2, 2, 1, False),  # Bite Alarm single, 2 nights, qty 2, 1 overdue, not late
            ("R3T", 5, 1, 0, False),  # Rods 3lb, 5 nights, qty 1, 0 overdue, not late
        ],
        "expected_total": "£170.00"
    }
]

def verify_calculations():
    """Verify the calculations match expected results."""
    print("=== CALCULATION VERIFICATION ===\n")
    
    grand_total = 0
    
    for case in test_cases:
        print(f"Customer {case['customer_id']}: {case['customer_name']}")
        print("-" * 60)
        
        customer_total = 0
        
        for code, nights, qty, overdue_days, returned_late in case["items"]:
            item = find_item(code)
            if not item:
                print(f"ERROR: Unknown code {code}")
                continue
                
            base, overdue, late_penalty, total = compute_line_cost(
                item["daily_p"], nights, qty, overdue_days, returned_late
            )
            
            customer_total += total
            
            print(f"{code:<4} {item['name'][:30]:<30} "
                  f"N:{nights} Q:{qty} O:{overdue_days} L:{'Y' if returned_late else 'N'} "
                  f"Base:{money(base)} Overdue:{money(overdue)} Late:{money(late_penalty)} "
                  f"Total:{money(total)}")
        
        grand_total += customer_total
        print(f"\nCustomer Total: {money(customer_total)}")
        print(f"Expected:       {case['expected_total']}")
        
        if money(customer_total) == case['expected_total']:
            print("✅ MATCH!")
        else:
            print("❌ MISMATCH!")
        
        print("\n" + "="*80 + "\n")
    
    print(f"GRAND TOTAL CALCULATED: {money(grand_total)}")
    print(f"EXPECTED GRAND TOTAL:   £3370.00 (for all 10 customers)")

if __name__ == "__main__":
    verify_calculations()
