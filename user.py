import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

def change_theme(selected_theme):
    # Add your theme change logic here
    print(f"Selected Theme: {selected_theme}")

# Create the main window
root = tk.Tk()
root.title("Themed GUI")
root.geometry('2700x2000')  # Set the size to 2000x1500

# Apply a ttkbootstrap style
style = Style("superhero")  # Change the theme as needed

# Create a Canvas for scrollability
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.configure(yscrollcommand=scrollbar.set)

# Frame inside the canvas
frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Header Label
header_label = ttk.Label(frame, text="Header", font=("Helvetica", 16, "bold"))
header_label.pack(side=tk.LEFT)

# Theme Selector
themes = ["superhero", "darkly", "flatly", "minty"]
selected_theme = tk.StringVar()
selected_theme.set(themes[0])  # Set initial theme
theme_dropdown = ttk.Combobox(frame, values=themes, textvariable=selected_theme, state="readonly", style="TCombobox")
theme_dropdown.pack(pady=(0, 20))
theme_dropdown.bind("<<ComboboxSelected>>", lambda event: change_theme(selected_theme.get()))

# Notebook with Tabs
notebook = ttk.Notebook(frame, bootstyle="light", width=2500, height=2000)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Write Code")
notebook.add(tab2, text="Upload File")

notebook.pack(pady=20, fill="both", expand=True)

# Update the scroll region
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Run the GUI
root.mainloop()
