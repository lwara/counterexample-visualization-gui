
import tkinter as tk
from tkinter import Text, Scrollbar, Menu

class CodeEditor(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.configure(bg="#D9D9D9")
        
        # Create the Text widget
        self.result_text = Text(self, wrap="word", width=100, height=30)
        
        # Place the Text widget
        self.result_text.place(x=200, y=200)

        # Create the Scrollbar widget
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.result_text.yview)
        self.scrollbar.place(x=1780, y=200, height=600)  # Adjust height as needed

        # Configure the Scrollbar to work with the Text widget
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Configure tags for different sections
        self.result_text.tag_configure("output", foreground="green")
        self.result_text.tag_configure("error", foreground="red")
        self.result_text.tag_configure("nofile", foreground="#7393B3")

        # Add context menu to the Text widget
        self.create_context_menu()

    def create_context_menu(self):
        # Create a context menu
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)

        # Bind the context menu to the Text widget
        self.result_text.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def cut_text(self):
        self.result_text.event_generate("<<Cut>>")

    def copy_text(self):
        self.result_text.event_generate("<<Copy>>")

    def paste_text(self):
        self.result_text.event_generate("<<Paste>>")

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    editor.pack(fill="both", expand=True)
    root.mainloop()
