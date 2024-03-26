from tkinter import *
from tkinter import filedialog
import ttkbootstrap as tb

root = tb.Window(themename="superhero")
root.title("Counterexample Visualisation- UCLID5")
root.geometry('2700x2000')

# Heading
heading_label = Label(root, text="Counterexample Visualisation- UCLID5", font=("Helvetica", 20))
heading_label.pack(pady=30)

# Horizontal Line
line = tb.Separator(root, orient='horizontal')
line.pack(fill='x', pady=10)

# Dropdown Menu for Themes
themes_label = tb.Label(root, text="Select Theme:", width=50)
themes_label.pack(side=LEFT, fill=X, pady=10)

themes_label2 = tb.Label(root, text="Select Theme:")
themes_label2.pack(side=LEFT, fill=X, pady=10)

# Notebook
my_notebook = tb.Notebook(root, bootstyle="light", width=2500, height=2000)
my_notebook.pack(pady=200)

# Add tabs to the notebook as needed
tab1 = my_notebook.add("Tab 1")
tab2 = my_notebook.add("Tab 2")

# Add widgets to the tabs as needed
label_tab1 = Label(tab1, text="Content of Tab 1")
label_tab1.pack(pady=20)

label_tab2 = Label(tab2, text="Content of Tab 2")
label_tab2.pack(pady=20)

# Additional tabs and widgets can be added similarly
