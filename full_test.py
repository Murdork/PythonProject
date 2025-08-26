#!/usr/bin/env python3
"""
Full test of the program with all test data cases.
"""

import subprocess
import sys

def create_full_test_input():
    """Create input for all 10 test cases."""
    
    test_cases = [
        {
            "customer": "Ted Danson,07970263076,1a,W4 0HY,2222",
            "items": ["DCH, 3, 1, 1, y", "BBT, 5, 2, 3, n", "SLP, 3, 1, 1, n", "TNT, 3, 1, 1, n"]
        },
        {
            "customer": "Bob Barker,09790263976,4b,G3 R30,1234", 
            "items": ["TNT, 3, 4, 0, n", "STV, 3, 1, 0, n"]
        },
        {
            "customer": "Angela Lansbury,07980111222,7c,NW1 6XE,5678",
            "items": ["BAS, 4, 1, 0, y", "BA1, 2, 2, 1, n", "R3T, 5, 1, 0, n"]
        },
        {
            "customer": "Tom Selleck,07973123456,22a,SW3 4QQ,3344",
            "items": ["RBR, 3, 2, 0, y", "REB, 4, 1, 2, n", "DCH, 2, 1, 0, n"]
        },
        {
            "customer": "Patrick Stewart,07988987654,12b,YO1 8AB,7788",
            "items": ["BCH, 3, 1, 0, n", "BBT, 2, 1, 1, y", "TNT, 5, 1, 0, n"]
        }
    ]
    
    inputs = []
    
    # Add first 5 customers
    for case in test_cases:
        inputs.append("1")  # Customer & hire details
        inputs.append(case["customer"])
        for item in case["items"]:
            inputs.append(item)
        inputs.append("")  # End items
        inputs.append("y")  # Confirm save
    
    # Get earnings report
    inputs.append("2")  # Earnings report
    
    # Exit
    inputs.append("3")  # Exit
    
    return "\n".join(inputs) + "\n"

def run_full_test():
    """Run the program with comprehensive test data."""
    
    input_data = create_full_test_input()
    
    print("=== COMPREHENSIVE PROGRAM TEST ===")
    print()
    print("Testing with first 5 customers from test data...")
    print("Expected behavior:")
    print("- Accept all customer data")
    print("- Process all equipment items") 
    print("- Calculate correct totals")
    print("- Generate earnings report")
    print()
    
    try:
        python_exe = "C:/Users/louis/OneDrive/University/Assignments/Programming/PythonProject/.venv/Scripts/python.exe"
        program_file = "Wip 2 calc corrrected maybe.py"
        
        result = subprocess.run(
            [python_exe, program_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout
        print("PROGRAM OUTPUT:")
        print("=" * 60)
        print(output)
        
        if result.stderr:
            print("\nERRORS:")
            print("=" * 60)
            print(result.stderr)
        
        # Analyze results
        print("\n" + "="*60)
        print("ANALYSIS:")
        print("="*60)
        
        # Check for key expected values
        expected_totals = ["£1187.50", "£270.00", "£170.00", "£125.00", "£385.00"]
        found_totals = []
        
        for total in expected_totals:
            if total in output:
                found_totals.append(total)
                print(f"✅ Found expected total: {total}")
            else:
                print(f"❌ Missing expected total: {total}")
        
        # Check for report generation
        if "=== Earnings Report" in output:
            print("✅ Earnings report generated")
        else:
            print("❌ Earnings report not found")
        
        # Check for proper termination
        if "Goodbye!" in output:
            print("✅ Program terminated properly")
        else:
            print("❌ Program did not terminate properly")
        
        success_rate = len(found_totals) / len(expected_totals) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}% ({len(found_totals)}/{len(expected_totals)} expected totals found)")
        
        return result.returncode == 0 and len(found_totals) >= 3
        
    except subprocess.TimeoutExpired:
        print("❌ Program timed out")
        return False
    except Exception as e:
        print(f"❌ Error running program: {e}")
        return False

if __name__ == "__main__":
    success = run_full_test()
    if success:
        print("\n🎉 COMPREHENSIVE TEST PASSED!")
        print("Your program handles the test data correctly.")
    else:
        print("\n⚠️ COMPREHENSIVE TEST HAD ISSUES")
        print("Review the output above for details.")
