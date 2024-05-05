import json

# Sample JSON data
json_data = {
    "output": 'Successfully instantiated 1 module(s).\nCEX for f [Step #4] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-5.ucl, line 13\n=================================\nStep #0\n  test1 : 0\n  test2 : 0\n=================================\n=================================\nStep #1\n  test1 : 1\n  test2 : 1\n=================================\n=================================\nStep #2\n  test1 : 2\n  test2 : 2\n=================================\n=================================\nStep #3\n  test1 : 3\n  test2 : 3\n=================================\n=================================\nStep #4\n  test1 : 3\n  test2 : 3\n=================================\n3 assertions passed.\n1 assertions failed.\n0 assertions indeterminate.\n  PASSED -> f [Step #1] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-5.ucl, line 13\n  PASSED -> f [Step #2] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-5.ucl, line 13\n  PASSED -> f [Step #3] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-5.ucl, line 13\n  FAILED -> f [Step #4] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-5.ucl, line 13\nFinished execution for module: main.',
    "error": ""
}

# Extract the output text
output_text = json_data.get("output", "")

# Split the output text by "CEX for f"
sections = output_text.split("CEX for f")[1:]

# Initialize variables to store steps and assertions
steps = []
assertions_failed = 0
assertions_passed = 0
assertions_indeterminate = 0

# Loop through each section
for section in sections:
    # Extract the step number from the CEX entry
    cex_info = section.split("[Step #")[1].split("]")[0].strip()
    cex_step_number = cex_info.split()[0]

    # Split the section by "Step #"
    section_parts = section.split("Step #")[1:]

    # Loop through each part of the section
    for part in section_parts:
        # Extract the step number from the part
        part_step_number = part.split()[0]

        # If the part contains a step number
        if part_step_number.isdigit():
            # Append the step number from the CEX entry to the current step
            full_step_number = f"{part_step_number} (CEX Step #{cex_step_number})"
            steps.append(full_step_number)

# Extract the number of assertions failed, passed, and indeterminate from the summary
summary = output_text.split("=================================")[-1]
summary_lines = summary.split("\n")
for line in summary_lines:
    if "assertions failed." in line:
        assertions_failed = int(line.split()[0])
    elif "assertions passed." in line:
        assertions_passed = int(line.split()[0])
    elif "assertions indeterminate." in line:
        assertions_indeterminate = int(line.split()[0])

# Print the extracted steps and assertions
print("Steps:", steps)
print("Assertions Failed:", assertions_failed)
print("Assertions Passed:", assertions_passed)
print("Assertions Indeterminate:", assertions_indeterminate)
