#!/usr/bin/env python3
"""
Analysis of the pricing scenario vs current implementation
"""

# Current implementation analysis
def current_implementation():
    """What your code currently does"""
    print("=== CURRENT IMPLEMENTATION ===")
    print("Base hire: daily_rate × nights × quantity")
    print("Overdue: daily_rate × overdue_days × quantity (100% rate)")
    print("Late penalty: 50% of daily_rate × quantity (when returned late)")
    print()

def scenario_interpretation():
    """What the scenario actually describes"""
    print("=== SCENARIO INTERPRETATION ===")
    print("Standard hire: Day 1 (9am) to Day 2 (2pm) = 1 standard period")
    print("Additional nights: 50% DISCOUNT (so only 50% rate, not 100%)")
    print("Late return after 2pm: Counts as additional night + extra 50% penalty")
    print()
    
    print("This suggests:")
    print("- Base period: full daily rate")
    print("- Additional nights: 50% of daily rate (DISCOUNT)")
    print("- Late penalty: +50% of daily rate")
    print()

def test_scenario_calculation():
    """Test with Ted Danson case using scenario rules"""
    print("=== TESTING SCENARIO RULES ===")
    print("Ted Danson - DCH: 3 nights, 1 qty, 1 overdue, returned late")
    print("Daily rate: £15.00")
    print()
    
    # Scenario interpretation:
    # 3 nights = 1 standard period + 2 additional nights
    # 1 overdue = additional night beyond the 3 nights
    # Returned late = extra penalty
    
    daily_rate = 1500  # pence
    
    print("Interpretation 1: 3 nights total hire period")
    base = daily_rate * 1 * 1  # First night at full rate
    additional = (daily_rate // 2) * 2 * 1  # 2 additional nights at 50%
    overdue = (daily_rate // 2) * 1 * 1  # 1 overdue at 50%
    late_penalty = (daily_rate // 2) * 1  # Late penalty 50%
    total1 = base + additional + overdue + late_penalty
    
    print(f"Base (1st night): £{base/100:.2f}")
    print(f"Additional (2 nights @ 50%): £{additional/100:.2f}")
    print(f"Overdue (1 day @ 50%): £{overdue/100:.2f}")
    print(f"Late penalty (50%): £{late_penalty/100:.2f}")
    print(f"TOTAL: £{total1/100:.2f}")
    print()
    
    print("Interpretation 2: All nights at full rate + overdue discount")
    base2 = daily_rate * 3 * 1  # All 3 nights at full rate
    overdue2 = (daily_rate // 2) * 1 * 1  # Overdue at 50% (discount)
    late_penalty2 = (daily_rate // 2) * 1  # Late penalty 50%
    total2 = base2 + overdue2 + late_penalty2
    
    print(f"Base (3 nights @ full): £{base2/100:.2f}")
    print(f"Overdue (1 day @ 50%): £{overdue2/100:.2f}")
    print(f"Late penalty (50%): £{late_penalty2/100:.2f}")
    print(f"TOTAL: £{total2/100:.2f}")
    print()
    
    print("Current implementation result: £67.50")
    print("Expected from test data: £67.50")
    print()
    
    if total1 == 6750:  # £67.50 in pence
        print("✅ Interpretation 1 matches!")
    elif total2 == 6750:
        print("✅ Interpretation 2 matches!")
    else:
        print("❌ Neither interpretation matches expected result")

if __name__ == "__main__":
    current_implementation()
    scenario_interpretation()
    test_scenario_calculation()
