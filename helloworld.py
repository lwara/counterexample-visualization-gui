import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Presentation")
        self.geometry("2095x2000")
        
        # Data for pagination
        self.data = [
            ("0", "PASSED", "unroll [Step #0] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
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
        
        # Adding more data for testing scrollable functionality
        for i in range(100):
            self.data.append((str(i), "PASSED", f"Test {i}"))

        # Page settings
        self.page_size = 10
        self.current_page = 0

        # Create pagination buttons
        #prev_button = ttk.Button(self, text="Previous", command=self.show_previous_page)
        #prev_button.place(x=10, y=10)
        #next_button = ttk.Button(self, text="Next", command=self.show_next_page)
        #next_button.place(x=90, y=10)
        
        # Create pagination buttons
        self.prev_button = ttk.Button(self, text="Previous", command=self.show_previous_page)
        self.prev_button.place(x=10, y=10)
        self.next_button = ttk.Button(self, text="Next", command=self.show_next_page)
        self.next_button.place(x=90, y=10)


        # Create a frame to hold the table
        self.table_frame = ttk.Frame(self)
        self.table_frame.place(x=100, y=100)

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
                label = ttk.Label(self.table_frame, text=value, background=bg_color, padding=(10,20), borderwidth=1,
                relief="solid",
                font=("Helvetica", 10))
                label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Configure row and column weights to make the grid resizable
        for i in range(min(len(self.data) - self.current_page * self.page_size, self.page_size) + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)
        
        # Reposition pagination buttons above the table frame
        self.prev_button.grid(row=end_index + 1, column=0, columnspan=3, pady=(10, 5))
        self.next_button.grid(row=end_index + 1, column=3, columnspan=3, pady=(10, 5))

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
