#from tkinter import filedialog
import tkinter as tk
from tkinter import filedialog
import requests as rq
 


def send_to_django(file_path):
    # Customize the Django API endpoint URL
    api_url = "http://localhost:8000/uclid5_endpoint/"

    try:
        files = {"uclid5_file": open(file_path, "rb")}
        response = rq.post(api_url, files=files)
        result = response.json()

        # Handle the result (update GUI, show output, etc.)
        print("UCLID5 Output:", result.get("output"))
        print("UCLID5 Error:", result.get("error"))

    except Exception as e:
        print("Error:", e)


def browse_file():
    file_path = filedialog.askopenfilename(
        title="Select a UCLID5 file", filetypes=[("UCLID5 Files", "*.ucl")]
    )
    if file_path:
        send_to_django(file_path)


# GUI setup
root = tk.Tk()
root.title("UCLID5 GUI")

# Create a button to browse and select a file
browse_button = tk.Button(root, text="Browse UCLID5 File", command=browse_file)
browse_button.pack(pady=20)

# Run the GUI
root.mainloop()
