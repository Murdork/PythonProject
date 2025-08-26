#!/usr/bin/env python3
"""
Automated test script for the hire management system.
This script will simulate user input to test all the test cases from Test Data.txt
"""

import subprocess
import sys
import time

# Test data from Test Data.txt
test_cases = [
    {
        "customer": "Ted Danson,07970263076,1a,W4 0HY,2222",
        "items": [
            "DCH, 3, 1, 1, y",
            "BBT, 5, 2, 3, n", 
            "SLP, 3, 1, 1, n",
            "TNT, 3, 1, 1, n"
        ]
    },
    {
        "customer": "Bob Barker,09790263976,4b,G3 R30,1234",
        "items": [
            "TNT, 3, 4, 0, n",
            "STV, 3, 1, 0, n"
        ]
    },
    {
        "customer": "Angela Lansbury,07980111222,7c,NW1 6XE,5678",
        "items": [
            "BAS, 4, 1, 0, y",
            "BA1, 2, 2, 1, n",
            "R3T, 5, 1, 0, n"
        ]
    }
]

def test_program():
    """Test the program with automated input."""
    print("=== Automated Test of Hire Management System ===\n")
    
    # Prepare input sequence
    inputs = []
    
    # Test first few customers
    for i, case in enumerate(test_cases):
        inputs.append("1")  # Select customer & hire details
        inputs.append(case["customer"])  # Customer details
        
        # Add items
        for item in case["items"]:
            inputs.append(item)
        inputs.append("")  # Blank line to finish items
        inputs.append("y")  # Confirm save
    
    # Generate earnings report
    inputs.append("2")  # Select earnings report
    inputs.append("3")  # Exit
    
    # Join all inputs with newlines
    input_string = "\n".join(inputs) + "\n"
    
    print("Input sequence to be sent:")
    print("-" * 40)
    for i, inp in enumerate(inputs):
        if inp == "":
            print(f"{i+1:2}: <BLANK LINE>")
        else:
            print(f"{i+1:2}: {inp}")
    print("-" * 40)
    print()
    
    # Run the program with input
    try:
        python_exe = "C:/Users/louis/OneDrive/University/Assignments/Programming/PythonProject/.venv/Scripts/python.exe"
        program_file = "Wip 2 calc corrrected maybe.py"
        
        print("Running program with test data...")
        print("=" * 50)
        
        result = subprocess.run(
            [python_exe, program_file],
            input=input_string,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("PROGRAM OUTPUT:")
        print("=" * 50)
        print(result.stdout)
        
        if result.stderr:
            print("\nERRORS:")
            print("=" * 50)
            print(result.stderr)
        
        print(f"\nProgram exit code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("Program timed out - this might indicate an infinite loop or waiting for input")
    except Exception as e:
        print(f"Error running program: {e}")

if __name__ == "__main__":
    test_program()
