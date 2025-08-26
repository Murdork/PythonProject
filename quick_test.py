#!/usr/bin/env python3
"""
Quick manual test to demonstrate the corrected program works.
"""

import subprocess
import sys

def test_single_customer():
    """Test with one customer from the test data."""
    
    # Input for Ted Danson case
    input_data = """1
Ted Danson,07970263076,1a,W4 0HY,2222
DCH, 3, 1, 1, y
BBT, 5, 2, 3, n
SLP, 3, 1, 1, n
TNT, 3, 1, 1, n

y
2
3
"""
    
    try:
        python_exe = "C:/Users/louis/OneDrive/University/Assignments/Programming/PythonProject/.venv/Scripts/python.exe"
        program_file = "Wip 2 calc corrrected maybe.py"
        
        print("Testing with Ted Danson case (should total £1187.50)...")
        print("=" * 60)
        
        result = subprocess.run(
            [python_exe, program_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        print("PROGRAM OUTPUT:")
        print("-" * 40)
        print(result.stdout)
        
        if result.stderr:
            print("\nERRORS:")
            print("-" * 40) 
            print(result.stderr)
        
        # Check if the expected total appears in output
        if "£1187.50" in result.stdout:
            print("\n✅ SUCCESS: Found expected total £1187.50 in output!")
        else:
            print("\n❌ Issue: Expected total £1187.50 not found in output")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Program timed out")
        return False
    except Exception as e:
        print(f"❌ Error running program: {e}")
        return False

if __name__ == "__main__":
    if test_single_customer():
        print("\n🎉 Program test completed successfully!")
    else:
        print("\n⚠️  Program test had issues")
