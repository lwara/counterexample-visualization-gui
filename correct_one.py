import customtkinter as ctk
#import tkinter as tk
from tkinter import filedialog

import orjson
from checker.file_upload import UclidRunner

class UclidGui(ctk.CTk):
    """_summary_

    Args:
        ctk (_type_): _description_
    """
    def __init__(self):
        super().__init__()

        self.title("UCLID5 GUI")
        self.geometry("2500x1600")  # Set the size of the window
        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.upload_button = ctk.CTkButton(self, text="Upload UCLID5 File", command=self.browse_file)
        self.upload_button.pack(pady=20)

        # Custom Text widget for displaying results
        self.result_text = ctk.CTkTextbox(self, wrap="word", height=10, width=60)
        self.result_text.pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select a UCLID5 file", filetypes=[("UCLID5 Files", "*.ucl")])
        if file_path:
            # Run UCLID5 command within the Docker container
            # Create an instance of the UclidRunner class
            uclid_runner = UclidRunner()
            result = uclid_runner.run_uclid5_command(file_path)
            decoded_result=result.decode('utf8').replace("'", '"')
            print(result)
            print("#################################33")
            print(type(decoded_result))
            # Convert the result to a JSON string
            json_result = orjson.dumps(decoded_result) # pylint: disable=maybe-no-member

            # Display the result in the custom text widget
            self.result_text.delete(1.0, ctk.END)  # Clear previous content
            self.result_text.insert(ctk.END, json_result)

if __name__ == "__main__":
    app = UclidGui()
    app.mainloop()
