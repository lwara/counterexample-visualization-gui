import json

# Sample JSON data
json_data = {
   "output": "Successfully instantiated 1 module(s).\nCEX for f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 8\n=================================\nStep #0\n  test1 : 1000\n  test2 : 1000\n=================================\nCEX for f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 9\n=================================\nStep #0\n  test1 : 1000\n  test2 : 1000\n=================================\n0 assertions passed.\n2 assertions failed.\n0 assertions indeterminate.\n  FAILED -> f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 8\n  FAILED -> f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 9\nFinished execution for module: main.",
    "error": ""
}

# Extract the output text
output_text = json_data.get("output", "")

# Initialize variables to store steps and their corresponding test results
steps = []
test_results = []

# Check if the output contains "CEX"
if "CEX" in output_text:
    # Extract the step number and line number from "CEX for f [Step #4] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-5.ucl, line 13"
    cex_info = output_text.split("CEX for f [Step #")[1].split("]")[0].strip()
    step_number = cex_info.split()[0]
    # Check if ", line " exists in cex_info
    if ", line " in output_text:
        line_number = output_text.split(", line ")[1].split("\n")[0].strip()
        print(line_number)
    else:
        line_number = None
    # Mark the step as failed
    status = "FAILED"
    # Append the step number, status, and line number to the steps list
    #steps.append((step_number, status, line_number))
    
    step_details = None
    # Check if the output contains "========="
    if "=================================" in output_text:
        # Split the output text by "========="
        sections = output_text.split("=================================")
        step_checker = 0
        serial_number = 1
        for section in sections:
            # Check if the section contains the step number
            if f"Step #{step_checker}".strip() and "test1".strip()  in section:
                if f"Step #{step_number}".strip() in section:
                    steps.append((serial_number, section, "FAILED", line_number))
                else:
                    steps.append((serial_number, section, "PASSED", line_number))    
                serial_number += 1
                step_checker += 1
    # Print the extracted steps and test results
    print("Steps:", steps)
    if test_results:
        print("Test Results:", test_results)
