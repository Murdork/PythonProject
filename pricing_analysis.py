#!/usr/bin/env python3
"""
Reverse engineering the expected calculation to understand the pricing model
"""

def reverse_engineer_calculation():
    """Work backwards from expected results to understand the pricing model"""
    print("=== REVERSE ENGINEERING THE PRICING MODEL ===")
    print()
    
    # Ted Danson DCH case: Expected £67.50
    # Input: DCH, 3 nights, 1 qty, 1 overdue, returned late
    # Daily rate: £15.00
    
    daily_rate = 1500  # pence
    expected_total = 6750  # £67.50 in pence
    
    print("Ted Danson DCH case analysis:")
    print("Input: 3 nights, 1 qty, 1 overdue, returned late")
    print("Daily rate: £15.00")
    print("Expected total: £67.50")
    print()
    
    # Test current implementation
    base_current = daily_rate * 3 * 1  # £45.00
    overdue_current = daily_rate * 1 * 1  # £15.00 (100% rate)
    late_penalty_current = (daily_rate * 1) // 2  # £7.50 (50% rate)
    total_current = base_current + overdue_current + late_penalty_current
    
    print("Current implementation:")
    print(f"Base (3 nights @ 100%): £{base_current/100:.2f}")
    print(f"Overdue (1 day @ 100%): £{overdue_current/100:.2f}")
    print(f"Late penalty (50%): £{late_penalty_current/100:.2f}")
    print(f"TOTAL: £{total_current/100:.2f}")
    print(f"Matches expected: {'✅' if total_current == expected_total else '❌'}")
    print()
    
    # Test scenario-compliant implementation
    print("Scenario-compliant implementation:")
    print("(1 standard period + 2 additional @ 50% + 1 overdue @ 50% + late penalty)")
    base_scenario = daily_rate * 1 * 1  # First period at full rate
    additional_scenario = (daily_rate // 2) * 2 * 1  # 2 additional at 50%
    overdue_scenario = (daily_rate // 2) * 1 * 1  # 1 overdue at 50%
    late_penalty_scenario = (daily_rate // 2) * 1  # Late penalty 50%
    total_scenario = base_scenario + additional_scenario + overdue_scenario + late_penalty_scenario
    
    print(f"Base (1 period @ 100%): £{base_scenario/100:.2f}")
    print(f"Additional (2 nights @ 50%): £{additional_scenario/100:.2f}")
    print(f"Overdue (1 day @ 50%): £{overdue_scenario/100:.2f}")
    print(f"Late penalty (50%): £{late_penalty_scenario/100:.2f}")
    print(f"TOTAL: £{total_scenario/100:.2f}")
    print(f"Matches expected: {'✅' if total_scenario == expected_total else '❌'}")
    print()
    
    # Check other test cases to see which model they follow
    print("=== CHECKING OTHER TEST CASES ===")
    print()
    
    # Bob Barker TNT case: 3 nights, 4 qty, 0 overdue, not late
    # Expected: £240.00 (from test data)
    print("Bob Barker TNT case:")
    print("Input: 3 nights, 4 qty, 0 overdue, not late")
    print("Daily rate: £20.00, Expected: £240.00")
    
    tnt_rate = 2000  # £20.00 in pence
    
    # Current model: all nights at full rate
    bob_current = tnt_rate * 3 * 4  # £240.00
    print(f"Current model (3 nights @ 100%): £{bob_current/100:.2f}")
    
    # Scenario model: 1 standard + 2 additional at 50%
    bob_base = tnt_rate * 1 * 4  # £80.00
    bob_additional = (tnt_rate // 2) * 2 * 4  # £80.00
    bob_scenario = bob_base + bob_additional
    print(f"Scenario model (1+2@50%): £{bob_scenario/100:.2f}")
    
    if bob_current == 24000:  # £240.00
        print("✅ Bob case matches CURRENT model")
    if bob_scenario == 24000:
        print("✅ Bob case matches SCENARIO model")
    print()

def conclusion():
    """Draw conclusions about the pricing model"""
    print("=== CONCLUSION ===")
    print()
    print("The test data appears to follow a model where:")
    print("1. ALL nights are charged at FULL daily rate (not discounted)")
    print("2. Overdue days are charged at FULL daily rate (not discounted)")
    print("3. Late penalties are 50% of daily rate")
    print()
    print("This CONTRADICTS the scenario description which mentions:")
    print("- '50% discount for additional nights'")
    print("- Overdue as discounted rates")
    print()
    print("RECOMMENDATION:")
    print("Follow the test data model since it provides concrete expected results.")
    print("The scenario description may be ambiguous or your test data represents")
    print("a different interpretation of the business rules.")

if __name__ == "__main__":
    reverse_engineer_calculation()
    conclusion()
