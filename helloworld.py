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
##themes_label.pack(side=LEFT, fill=X, pady=10)

themes_label2 = tb.Label(root, text="Select Theme:")
#themes_label2.pack(side=LEFT, fill=X, pady=10)

# Notebook
my_notebook = tb.Notebook(root, bootstyle="light", width=2500, height=2000)
my_notebook.pack(pady=200)

  
    
       
def on_button1_click(tab_frame):
    """_summary_

    Args:
        tab_frame (_type_): _description_
    """
    text1 = tab_frame.text_area1.get("1.0", "end-1c")
    text2 = tab_frame.text_area2.get("1.0", "end-1c")
    print(f"Button 1 clicked on Tab {tab_frame.tab_number}")
    print(f"Text Area 1 Content: {text1}")
    print(f"Text Area 2 Content: {text2}")

def on_button2_click(tab_frame):
    """_summary_

    Args:
        tab_frame (_type_): _description_
    """
    text1 = tab_frame.text_area1.get("1.0", "end-1c")
    text2 = tab_frame.text_area2.get("1.0", "end-1c")
    print(f"Button 2 clicked on Tab {tab_frame.tab_number}")
    print(f"Text Area 1 Content: {text1}")
    print(f"Text Area 2 Content: {text2}")

def upload_file(tab_frame):
    """_summary_

    Args:
        tab_frame (_type_): _description_
    """
    file_path = filedialog.askopenfilename(title="Select a file")
    tab_frame.text_area2.insert("1.0", f"File Uploaded: {file_path}\n")

def clear_text_areas(tab_frame):
    """_summary_

    Args:
        tab_frame (_type_): _description_
    """
    tab_frame.text_area1.delete("1.0", END)
    tab_frame.text_area2.delete("1.0", END)


class TabFrame(tb.Frame):
    """_summary_

    Args:
        tb (_type_): _description_
    """
    def __init__(self, notebook, tab_number, label1, label2):
        super().__init__(notebook)
        self.tab_number = tab_number
        
        label1 = Label(self, text=label1)        
        label1.pack(fill=X, pady=10)
        label2 = Label(self, text=label2)
        label2.pack(pady=5)

        self.text_area1 = Text(self, width=70, height=30)
        self.text_area1.pack(side=LEFT)
        
        
        self.text_area2 = Text(self, width=70, height=30)
        self.text_area2.pack(side=RIGHT)

        
        
        button1 = tb.Button(self, text="Button 1", bootstyle="primary outline", command=lambda: on_button1_click(self))
        #button1.pack(pady=10)

        button2 = tb.Button(self, text="Button 2", bootstyle="danger outline", command=lambda: on_button2_click(self))
        #button2.pack(pady=10)
        
        
        if self.tab_number == 2:
            upload_button = tb.Button(self, text="Upload File", bootstyle="warning", command=lambda: upload_file(self))
            upload_button.pack(side=LEFT, pady=10, padx=(0,5))
            
            # Hide text_area1 in Tab 2
             # Bind the clear_text_areas function to the tab selected event
            self.bind("<Visibility>", lambda event: clear_text_areas(self))

            self.text_area1.pack_forget()

# Create TabFrames and add them to the notebook
tab1 = TabFrame(my_notebook, 1, "Type code Here", "Counter Example Report")
tab2 = TabFrame(my_notebook, 2, "Please click the Button to upload a file", "Label Y")

my_notebook.add(tab1, text="Run Code")
my_notebook.add(tab2, text="Upload Code file")

root.mainloop()
