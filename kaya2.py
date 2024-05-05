import json
import re

# Sample JSON data
json_data = {
    "output":"Successfully instantiated 1 module(s).\\nCEX for f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 8\\n=================================\\nStep #0\\n  test1 : 1000\\n  test2 : 1000\\n=================================\\nCEX for f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 9\\n=================================\\nStep #0\\n  test1 : 1000\\n  test2 : 1000\\n=================================\\n0 assertions passed.\\n2 assertions failed.\\n0 assertions indeterminate.\\n  FAILED -> f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 8\\n  FAILED -> f [Step #0] assertion @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/test-assert-4.ucl, line 9\\nFinished execution for module: main.\\n"
}

# Extract the output text
output_text = json_data.get("output", "")

# Initialize variables to store steps and their corresponding test results
steps = []

# Split the output text by "CEX for f"

sections = output_text.split("CEX for f")[1:]

# Define the regex pattern to match variable names followed by a colon
pattern = r'\b\w+\s*:\s*-?\d*\.?\d+'  # Matches word characters followed by optional whitespace and a colon


step_checker = 0
serial_number = 1
# Loop through each section
for section in sections:
    #print(section)
    #print("\n")
    
    # Extract the step number and line number
    cex_info = section.split("[Step #")[1].split("]")[0].strip()
    
    step_number = cex_info.split()[0]
    #print(step_number)
    line_number = section.split(", line ")[1].split("\n")[0].strip()  
    match = re.search(r'\d+', line_number)  # Match one or more digits
    line_number = match.group() if match else None  # Get the matched number
    #print(line_number)
    # Mark the step as failed
    status = "FAILED"
    
    # Check if the output contains "========="
    if "=================================" in section:
        #print(True)
        # Split the output text by "========="
        sections_without_equals= section.split("=================================")
        cex_header = sections_without_equals[0]
        
        for sub_section in sections_without_equals:
            # get the line for CEX
            #print(re.search(pattern, sub_section))
            # Check if the section contains the step number
            if f"Step #{step_checker}".strip() in sub_section and re.search(pattern, sub_section):
                if f"Step #{step_number}".strip() in sub_section:
                    #print(sub_section)
                    #print(line_number)
                    #print("\n")
                    steps.append((f"CEX for f {cex_header}", sub_section, line_number))
                else:
                    steps.append((f"CEX for f {cex_header}", sub_section, line_number))    
                serial_number += 1
                step_checker += 1
        serial_number = 1
        step_checker = 0
    # Append the step number, status, and line number to the steps list
    #steps.append((step_number, status, line_number))

# Print the extracted steps
print("**************8")
print("Steps:", steps)
