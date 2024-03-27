import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Presentation")
        self.geometry("800x600")
        
        # Data for pagination
        self.data = [
            ("0", "PASSED", "unroll [Step #0] property a_lhelloworld.pye_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("1", "PASSED", "unroll [Step #1] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("2", "PASSED", "unroll [Step #2] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("3", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("4", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("5", "FAILED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("6", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("7", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("8", "FAILED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("9", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("10", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            ("11", "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
        ]
        
        # Page settings
        self.page_size = 5
        self.current_page = 0

        # Create a frame to hold the table
        self.table_frame = ttk.Frame(self)
        self.table_frame.place(x=100, y=50)  # Centering the table
        self.table_frame.pack(fill="both", expand=True)
        
        # Create pagination buttons
        prev_button = ttk.Button(self, text="Previous", command=self.show_previous_page)
        prev_button.pack(side="left", padx=10, pady=5)
        next_button = ttk.Button(self, text="Next", command=self.show_next_page)
        next_button.pack(side="right", padx=10, pady=5)

        # Display column labels
        self.create_column_labels()

        # Display data for the current page
        self.display_current_page()
        
    def create_column_labels(self):
        # Create column labels
        columns = ["Step", "Status", "Property"]
        for col, column_name in enumerate(columns):
            label = ttk.Label(self.table_frame, text=column_name, font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    def display_current_page(self):
        # Clear previous data from the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Display column labels
        self.create_column_labels()

        # Display data for the current page
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.data))
        for row, item in enumerate(self.data[start_index:end_index], start=1):
            for col, value in enumerate(item):
                # Choose background color based on row number
                bg_color = "lightgray" if row % 2 == 0 else "white"
                label = ttk.Label(self.table_frame, text=value, background=bg_color)
                label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Configure row and column weights to make the grid resizable
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(2, weight=2)
        for i in range(min(len(self.data) - self.current_page * self.page_size, self.page_size) + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)

    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

    def show_next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_current_page()

if __name__ == "__main__":
    app = App()
    app.mainloop()
