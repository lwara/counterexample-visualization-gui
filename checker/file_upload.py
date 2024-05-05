import subprocess
import re
import orjson

class UclidRunner:
    def __init__(self):
        pass

    def run_uclid5_command(self, file_path):
        #print("Inside run-uclid5 command function")
        try:
                  
            # Run the UCLID5 command
            uclid5_command = f"uclid {file_path}"
            #print(uclid5_command)

            process = subprocess.Popen(uclid5_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Retrieve the output and error
            output, error = process.communicate()
            

            # Handle the output or error as needed
            #TODO: find json parser
            result = orjson.dumps({'output': output.decode(), 'error': error.decode()}) # pylint: disable=maybe-no-member
            print(result)            
            return result
        except subprocess.CalledProcessError as e:
            return {'error': str(e)}
        
class ProcessUclidResults:
    def __init__(self):
        pass
    
    def check_for_CEX(self, json_uclid5_result):
        if "CEX" in json_uclid5_result:
            return True
        
        return False
    
    def get_CEX(self, json_uclid5_result):
        # Initialize variables to store steps and their corresponding test results
        steps = []
        #print(json_uclid5_result)
        # Split the output text by "CEX for f"
        sections = json_uclid5_result.split("CEX for f")[1:]

        # Define the regex pattern to match variable names followed by a colon
        pattern = r'\b\w+\s*:\s*-?\d*\.?\d+'  # Matches word characters followed by optional whitespace and a colon

        step_checker = 0
        serial_number = 1
        # Loop through each section
        for section in sections:
            #print(section)
            # Extract the step number and line number
            cex_info = section.split("[Step #")[1].split("]")[0].strip()
    
            step_number = int(cex_info.split()[0])
            line_number = section.split(", line ")[1].split("\n")[0].strip()
            
            match = re.search(r'\d+', line_number)  # Match one or more digits
            line_number = match.group() if match else None  # Get the matched number
    
            # Check if the output contains "========="
            if "=================================" in section:
                #print(True)
                # Split the output text by "========="
                sections_without_equals= section.split("=================================")
                cex_header = sections_without_equals[0]
        
                for sub_section in sections_without_equals:
                    # Check if the section contains the step number
                    if f"Step #{step_checker}".strip() in sub_section and re.search(pattern, sub_section):
                        if f"Step #{step_number}".strip() in sub_section:
                            steps.append((f"CEX for f {cex_header}", sub_section, line_number))
                        else:
                            steps.append((f"CEX for f {cex_header}", sub_section, line_number))    
                        serial_number += 1
                        step_checker += 1
                serial_number =1
                step_checker = 0
        return steps
        
    
    def get_summary(self, json_uclid5_result):
        #print(json_uclid5_result)
        # Initialize variables to store steps and assertions
        #assertions_failed = 0
        #assertions_passed = 0
        #assertions_indeterminate = 0

        # Extract the number of assertions failed, passed, and indeterminate from the summary
        summary = json_uclid5_result.split("=================================")[-1]
        summary_lines = summary.split("\n")
        for line in summary_lines:
            if "assertions failed." in line:
                assertions_failed = int(line.split()[0])
                #assertions_failed=assertions_failed
            elif "assertions passed." in line:
                assertions_passed = int(line.split()[0])
            elif "assertions indeterminate." in line:
                assertions_indeterminate = int(line.split()[0])

        return assertions_passed, assertions_failed, assertions_indeterminate

"""
if __name__ == "__main__":
    # Example usage:
    uclid_runner = UclidRunner()
    result = uclid_runner.run_uclid5_command("path/to/your/file.ucl")

    # Print the result (customize based on your needs)
    print(result)
"""
