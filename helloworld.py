import csv
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import Frame
import webbrowser
from tkinter import messagebox


def counterExampleReport():
    Report()
    
class Report(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        #self.master.geometry("2095x2000")
        self.configure(bg="#D9D9D9")         
        
        # Data for pagination
        self.original_data = [
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
            self.original_data.append((str(i), "PASSED", f"Test {i}"))

        self.data = self.original_data.copy()

        # Display Heading of the Report
        heading_label = ttk.Label(self, text="CounterExample Report", font=("Helvetica", 32, "bold"))
        heading_label.place(x=600, y= 10)
                
        deatils_text = ttk.Label(self, text="The following are the details : ", font=("Helvetica", 20, "bold"))
        deatils_text.place(x=100, y=200)
        
        # Page settings
        self.page_size = 10
        self.current_page = 0

        # Create pagination buttons
        self.prev_button = ttk.Button(self, text="< Previous", command=self.show_previous_page)
        self.prev_button.place(x=10, y=850)
        self.next_button = ttk.Button(self, text="Next >", command=self.show_next_page)
        self.next_button.place(x=200, y=850)

        # Create filter entry
        self.filter_label = ttk.Label(self, text="Filter:")
        self.filter_label.place(x=500, y=850)
        self.filter_entry = ttk.Entry(self)
        self.filter_entry.place(x=580, y=850)
        self.filter_button = ttk.Button(self, text="Apply Filter", command=self.apply_filter)
        self.filter_button.place(x=950, y=850)

        # Create a save button
        self.save_button = ttk.Button(self, text="Save", command=self.save_data)
        self.save_button.place(x=1200, y=850)
        
        # Create a frame to hold the table
        self.table_frame = ttk.Frame(self)
        self.table_frame.place(x=100, y=1000)

        # Display column labels
        self.create_column_labels()

        # Display data for the current page
        self.display_current_page()
        
        self.master.resizable(False, False)
        
    def create_column_labels(self):
        # Create column labels
        columns = ["Step", "Status", "Property"]
        for col, column_name in enumerate(columns):
            label = ttk.Label(self.table_frame, text=column_name, font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    def display_current_page(self):
        # Show loading icon
        self.loading_icon = ttk.Progressbar(self, mode='indeterminate')
        self.loading_icon.place(x=100, y=50)
        self.loading_icon.start()

        # Clear previous data from the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
            
        # Variables to store summary information
        total_passed = 1000000
        total_passed_text = "Assertation Passed"
        total_failed = 0
        total_failed_text = "Assertations Failed"
        total_inderterminate = 0 
        total_inderterminate_text = "Assertions Inderterminated"
        # Display column labels
        self.create_column_labels()

        # Display data for the current page
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.data))
        for row, item in enumerate(self.data[start_index:end_index], start=1):
            for col, value in enumerate(item):
                # Choose background color based on row number and status
                bg_color = "lightgray" if row % 2 == 0 else "white"
                if col == 1 and value == "FAILED":
                    bg_color = "pink"
                label = HoverLabel(self.table_frame, text=value, background=bg_color, padding=(10,20), borderwidth=1,
                relief="solid",
                font=("Helvetica", 10), link=item[-1] if col == 2 else None)
                label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                label.bind("<Button-1>", self.open_link)

         # Display summary label
        total_failed_label = ttk.Label(self, text=f"{total_failed} {total_failed_text}", font=("Helvetica", 18), background="white", borderwidth=1, relief="flat",padding=(30,30) )
        total_failed_label.place(x=100, y= 300)        
        #total_failed_label_1 = ttk.Label(self, text=total_failed_text, font=("Helvetica", 20, "bold"))
        #total_failed_label_1.place(x=500, y=350)
        
        total_passed_label = ttk.Label(self, text=f"{total_passed} {total_passed_text}", font=("Helvetica", 18), background="white", borderwidth=1, relief="flat",padding=(30,30) )
        total_passed_label.place(x=100, y=450)        
        #total_passed_label_1 = ttk.Label(self, text=total_passed_text, font=("Helvetica", 20))
        #total_passed_label_1.place(x=500, y=500 )
        
        total_inderterminated_label = ttk.Label(self, text=f"{total_inderterminate} {total_inderterminate_text}", font=("Helvetica", 18), background="white", borderwidth=1, relief="flat",padding=(20,30) )
        total_inderterminated_label.place(x=100, y=600)
        #total_inderterminated_label_1 = ttk.Label(self, text=total_inderterminate_text, font=("Helvetica", 20, "bold"))
        #total_inderterminated_label_1.place(x=500, y=600)
        

        # Configure row and column weights to make the grid resizable
        for i in range(min(len(self.data) - self.current_page * self.page_size, self.page_size) + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)
        
        """# Reposition pagination buttons above the table frame
        self.prev_button.grid(row=end_index + 1, column=0, columnspan=3, pady=(10, 5))
        self.next_button.grid(row=end_index + 1, column=3, columnspan=3, pady=(10, 5))"""

        # Schedule stopping the loading icon after 5 seconds
        self.after(5000, self.stop_loading_icon)

    def stop_loading_icon(self):
        # Hide loading icon
        self.loading_icon.stop()
        self.loading_icon.destroy()
        
        
    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

    def show_next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_current_page()

    def apply_filter(self):
        filter_text = self.filter_entry.get().strip()
        if filter_text:
            self.data = [row for row in self.original_data if filter_text.lower() in " ".join(row).lower()]
        else:
            self.data = self.original_data.copy()
        self.current_page = 0
        self.display_current_page()
        
    def save_data(self):
        # Ask user to select a file location for saving
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            if os.path.exists(file_path):
                # File already exists, ask user if they want to overwrite
                response = messagebox.askyesno(
                    "File Exists",
                    "The file already exists. Do you want to overwrite it?"
                )
                if not response:
                    return  # Cancel saving
            # Save data to the selected CSV file
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Step", "Status", "Property"])  # Write header
                writer.writerows(self.data)
            # Notify the user that the file has been saved
            messagebox.showinfo("File Saved", f"The data has been saved to:\n{file_path}")
         
    def open_link(self, event):
        link = event.widget.link
        if link:
            if messagebox.askyesno("Open Link", f"Do you want to open the link:\n\n{link}"):
                webbrowser.open_new_tab(link)

class HoverLabel(ttk.Label):
    def __init__(self, master=None, **kwargs):
        self.link = kwargs.pop('link', None)
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.cursor = "hand2"

    def on_enter(self, event):
        self.config(foreground="blue", cursor=self.cursor)

    def on_leave(self, event):
        self.config(foreground="black", cursor="")
"""
if __name__ == "__main__":
    app = App()
    app.mainloop()
"""