import subprocess
import re
import orjson


class UclidRunner:
    def __init__(self):
        pass

    def run_uclid5_command(self, file_path):
        # print("Inside run-uclid5 command function")
        try:

            # Run the UCLID5 command
            uclid5_command = f"uclid {file_path}"
            # print(uclid5_command)

            process = subprocess.Popen(
                uclid5_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Retrieve the output and error
            output, error = process.communicate()

            # Handle the output or error as needed
            # TODO: find json parser
            result = orjson.dumps(
                {"output": output.decode(), "error": error.decode()}
            )  # pylint: disable=maybe-no-member
            # print(result)
            return result
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}


class ProcessUclidResults:
    def __init__(self):
        pass

    def check_for_CEX(self, json_uclid5_result):
        print("we are checking if counterexamples are found iun this string :")
        print(json_uclid5_result)
        if "CEX for " in json_uclid5_result:
            return True
        else:
            return False

    def get_CEX(self, json_uclid5_result, file_path):
        # Initialize variables to store steps and their corresponding test results
        steps = []
        step_assertions = []  # hold the actual assertions

        # Split the output text by "CEX for f"
        sections = json_uclid5_result.split("CEX for ")[1:]

        # Define the regex pattern to match variable names followed by a colon
        pattern = r"\b\w+\s*:\s*-?\d*\.?\d+"  # Matches word characters followed by optional whitespace and a colon

        step_checker = 0
        # serial_number = 1
        # Loop through each section
        for section in sections:
            # Extract the step number and line number
            cex_info = section.split("[Step #")[1].split("]")[0].strip()
            step_number = int(
                cex_info.split()[0]
            )  # this and line number qre getting the line where the counter example failed
            line_number = section.split(", line ")[1].split("\n")[0].strip()
            # print("CEX are here :")
            # print(f"section:{section}")
            # print(f"cex info : {cex_info}")
            # print(f"step number : {step_number}")
            # print(f"line number : {line_number}")
            assertion_code = self.get_assertion_from_code(file_path, line_number)
            # print(file_path)
            match = re.search(r"\d+", line_number)  # Match one or more digits
            matched_line_number = (
                match.group() if match else None
            )  # Get the matched number
            # print(f"matched line number : {matched_line_number}")
            print(
                "*****************************************************************************"
            )
            # Check if the output contains "========="
            if "=================================" in section:
                # print(True)
                # Split the output text by "========="
                sections_without_equals = section.split(
                    "================================="
                )
                cex_header = sections_without_equals[0]
                # print(f"section without equals sign : {sections_without_equals}")
                # print(f"cex header : {cex_header}")
                for sub_section in sections_without_equals:
                    # Check if the section contains the step number
                    if f"Step #{step_checker}".strip() in sub_section:
                        matched_step = re.search(pattern, sub_section)
                        if matched_step:  # this section is ambiguous
                            step_assertions.append((sub_section))
                            if f"Step #{step_number}".strip() in sub_section:
                                # steps.append((f"CEX for f {cex_header}", sub_section, matched_line_number))
                                print(sub_section)
                                # step_assertions.append((sub_section))
                            else:
                                # step_assertions.append(sub_section)
                                print(sub_section)
                                # step_assertions.append((sub_section))
                            # print(step_assertions)
                            # steps.append((f"CEX for f {cex_header}", sub_section, matched_line_number))
                            # serial_number += 1

                            step_checker += 1
                steps.append(
                    (f"CEX for f {cex_header}", assertion_code, step_assertions)
                )
                # print(step_assertions)
                step_assertions = []
                # serial_number =1
                step_checker = 0
        return steps

    def get_summary(self, json_uclid5_result):
        passed = re.search(r"(\d+) assertions passed", json_uclid5_result)
        failed = re.search(r"(\d+) assertions failed", json_uclid5_result)
        indeterminate = re.search(r"(\d+) assertions indeterminate", json_uclid5_result)

        assertions_passed = int(passed.group(1)) if passed else 0
        assertions_failed = int(failed.group(1)) if failed else 0
        assertions_indeterminate = int(indeterminate.group(1)) if indeterminate else 0

        return assertions_passed, assertions_failed, assertions_indeterminate

    def get_assertion_from_code(self, file_path, line_number):
        print(file_path)
        print(line_number)
        with open(file_path, "r") as file:
            content = file.read()
        # Subtract 1 from line_number because list indices start from 0
        line_number = int(line_number)
        # Split the content by whitespace
        content_array = content.splitlines()
        line_content = content_array[line_number - 1].strip()  # Get the line content
        print(line_content)
        return line_content


"""
if __name__ == "__main__":
    # Example usage:
    uclid_runner = UclidRunner()
    result = uclid_runner.run_uclid5_command("path/to/your/file.ucl")

    # Print the result (customize based on your needs)
    print(result)
"""
