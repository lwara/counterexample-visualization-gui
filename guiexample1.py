import tkinter as tk
from tkinter import filedialog, scrolledtext, Menu, messagebox
from PIL import Image, ImageTk
from tkinterdnd2 import TkinterDnD, DND_FILES

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Editor with Logo")
        
        # Initialize DnD
        self.root = TkinterDnD.Tk()
        
        # Create the menu bar
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add file menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add edit menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=lambda: self.code_editor.event_generate("<<Undo>>"))
        self.edit_menu.add_command(label="Redo", command=lambda: self.code_editor.event_generate("<<Redo>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.code_editor.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.code_editor.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.code_editor.event_generate("<<Paste>>"))
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Add help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Add the logo
        self.logo_frame = tk.Frame(self.root)
        self.logo_frame.pack(side=tk.TOP, anchor="nw")

        self.logo_image = Image.open("logo.png")  # Provide the path to your logo image
        self.logo_image = self.logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.logo_frame, image=self.logo_photo)
        self.logo_label.pack(side=tk.LEFT)
        
                # Create the code editor area
        self.code_editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, undo=True)
        self.code_editor.pack(fill=tk.BOTH, expand=1)

        # Create the console/output area
        self.console_output = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state='disabled')
        self.console_output.pack(fill=tk.BOTH)

        # Add a run button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(side=tk.BOTTOM)

        # Enable drag and drop
        self.code_editor.drop_target_register(DND_FILES)
        self.code_editor.dnd_bind('<<Drop>>', self.drop)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            self.load_file(file_path)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.code_editor.get("1.0", tk.END))

    def run_code(self):
        code = self.code_editor.get("1.0", tk.END)
        exec_globals = {}
        exec_locals = {}

        self.console_output.config(state='normal')
        self.console_output.delete("1.0", tk.END)
        try:
            exec(code, exec_globals, exec_locals)
        except Exception as e:
            self.console_output.insert(tk.END, str(e))
            self.console_output.config(state='disabled')

    def show_about(self):
        messagebox.showinfo("About", "Code Editor with Logo\nVersion 1.0")

    def drop(self, event):
        file_path = event.data.strip('{}')  # Remove curly braces if any
        self.load_file(file_path)

    def load_file(self, file_path):
        with open(file_path, "r") as file:
            self.code_editor.delete("1.0", tk.END)
            self.code_editor.insert(tk.END, file.read())

if  __name__  == "main":
    root = TkinterDnD.Tk() # Use TkinterDnD's Tk class
    app = CodeEditorApp(root)
    root.geometry("800x600")
    root.mainloop()