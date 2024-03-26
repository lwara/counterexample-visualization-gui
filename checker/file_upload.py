import subprocess

import orjson

class UclidRunner:
    def __init__(self):
        pass

    def run_uclid5_command(self, file_path):
        print("Inside run-uclid5 command function")
        try:
                  
            # Run the UCLID5 command
            uclid5_command = f"uclid {file_path}"
            print(uclid5_command)

            process = subprocess.Popen(uclid5_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Retrieve the output and error
            output, error = process.communicate()

            # Handle the output or error as needed
            #TODO: find json parser
            result = orjson.dumps({'output': output.decode(), 'error': error.decode()})
            return result
        except subprocess.CalledProcessError as e:
            return {'error': str(e)}

if __name__ == "__main__":
    # Example usage:
    uclid_runner = UclidRunner()
    result = uclid_runner.run_uclid5_command("path/to/your/file.ucl")

    # Print the result (customize based on your needs)
    print(result)
