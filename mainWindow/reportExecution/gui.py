import csv
import json
import os
import tkinter as tk
from tkinter import END, Canvas, Scrollbar, Text, ttk
from tkinter import filedialog
from tkinter import Frame
import webbrowser
from tkinter import messagebox

import orjson

from checker.file_upload import ProcessUclidResults, UclidRunner




def counterExampleReport():
    Report()
    
class Report(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        #self.master.geometry("2095x2000")
        self.configure(bg="#D9D9D9")  
        
        
        self._file_upload_ = None       
        self.passed = 0
        self.failed = 0
        self.inderteminated = 0
        
        # Data for pagination
        #self.original_data = None
        """self.original_data = [
            (0, 'PASSED', "unroll [Step #0] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            (1, "PASSED", "unroll [Step #1] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            (2, "PASSED", "unroll [Step #2] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
            (3, "PASSED", "unroll [Step #3] property a_le_b @ /home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/samples.ucl, line 13"),
             
        ]
        """ 
        #self.load_json_result_data()

        self.data = []

        # Display Heading of the Report
        heading_label = ttk.Label(self, text="CounterExample Visualization GUI", font=("Helvetica", 24, "bold"))
        heading_label.place(x=600, y= 10)
        
        # Draw a horizontal line
        line_header_canvas = Canvas(self, width=1250, height=5, bg="black")
        line_header_canvas.create_line(0, 0, 100, 0, width=2)
        line_header_canvas.place(x=500, y=60)
        
        # for uploading the file
        upload_text = ttk.Label(self, text="Click the buttons to upload file : ", font=("Helvetica", 14, "bold"))
        #upload_text.place(x=100, y=200)
               
        # Create upload buttons
        upload_button = ttk.Button(self, text="Upload File", command=self.get_uploaded_file)
        upload_button.place(x=10, y=100)
        run_button = ttk.Button(self, text="Run Uclid5", command=self.run_uclid, style="Run.TButton")
        run_button.place(x=200, y=100)
        
        # Define a custom style for the save button
        self.style = ttk.Style()
        self.style.configure("Run.TButton", background="#dfe2e8")
        # for showing uploaded file
        self.uploaded_file = ttk.Label(self, text="Uploaded file is : ", font=("Helvetica", 12))
        #uploaded_file.place(x=100, y=320) 
        
        #clear and save buttons
        save_code_button = ttk.Button(self, text="Save", command=self.get_uploaded_file)
        save_code_button.place(x=550, y=100)
        clear_code_button = ttk.Button(self, text="Clear Code", command=self.run_uclid)
        clear_code_button.place(x=750, y=100)        
                
        ###############TEXT EDITOR FOR CODE###############
        # Create a canvas for line numbers
        self.line_number_canvas = tk.Canvas(self, width=40, height=965, bg="green", highlightthickness=0)
        self.line_number_canvas.place(x=170,y=200)
        
        self.result_text = Text(self, wrap="word", width=100, height=30)         
        # Calculate the height of the Text widget in terms of lines
        text_height_in_lines = int(self.result_text.cget("height"))

        # Create the Text widget
        #self.result_text = Text(self, wrap="word", width=80, height=10)
        self.result_text.place(x=200, y=200)

        # Calculate the height of one line of text in the Text widget
        line_height = self.result_text.tk.call("font", "metrics", self.result_text.cget("font"), "-linespace")

        # Calculate the height of the Text widget in terms of pixels
        self.text_height_in_pixels = text_height_in_lines * line_height

        # Create the Scrollbar widget
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.result_text.yview)
        self.scrollbar.place(x=1780, y=200, height=self.text_height_in_pixels)  # Set the height to match the Text widget

        # Configure the Scrollbar to work with the Text widget
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Configure tags for different sections
        self.result_text.tag_configure("output", foreground="green")
        self.result_text.tag_configure("error", foreground="red")
        ############################
                
                
                
                
        deatils_text = ttk.Label(self, text="The following are the details : ", font=("Helvetica", 18, "bold"))
        #deatils_text.place(x=100, y=400)
        
        # Page settings
        self.page_size = 5
        self.current_page = 0
        
        # Draw a horizontal line for CEX report
        line_cex_report = Canvas(self, width=2000, height=5, bg="black")
        line_cex_report.create_line(0, 0, 100, 0, width=2)
        line_cex_report.place(x=0, y=1180)
        
        # Create pagination buttons
        self.prev_button = ttk.Button(self, text="< Previous", command=self.show_previous_page)
        self.prev_button.place(x=10, y=1210)
        self.next_button = ttk.Button(self, text="Next >", command=self.show_next_page)
        self.next_button.place(x=200, y=1210)

        # Create filter entry
        self.filter_label = ttk.Label(self, text="Filter:")
        self.filter_label.place(x=500, y=1210)
        self.filter_entry = ttk.Entry(self)
        self.filter_entry.place(x=580, y=1210)
        self.filter_button = ttk.Button(self, text="Apply Filter", command=self.apply_filter)
        self.filter_button.place(x=950, y=1210)

        # Create a save button
        self.save_button = ttk.Button(self, text="Save", command=self.save_data)
        self.save_button.place(x=1200, y=1210)
        
        # Create a frame to hold the table
        self.table_frame = ttk.Frame(self)
        self.table_frame.place(x=200, y=1300)
        
        # here is canvas that will cover the Frame 
        
        table_text_area = Text(self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            state='disabled'  # Set the state to 'disabled'
            )
        table_text_area.place(
            x=120.0,
            y=1270.0,
            width=1849.0,
            height=800.0
            )
        self.table_frame.lift()
        """# Display column labels
        self.create_column_labels()

        # Display data for the current page
        self.display_current_page()"""
        
        self.master.resizable(False, False)
        
        # Create an instance of the Uclid5GUI class
             
    # from FILE UPLOAD WINDOW :
    
    def get_uploaded_file(self):
        """_summary_
        """
        #print("select the file")
        file_path = filedialog.askopenfilename(title="Select a UCLID5 file", filetypes=[("UCLID5 Files", "*.ucl")])
        if file_path:
            #self._file_upload_ = file_path
            self.place_word_on_canvas(file_path)
            
    # This is to show which file has been uploaded                 
    def place_word_on_canvas(self, word):
        # Clear the canvas first   
        self.uploaded_file.pack_forget()     
        # for showing uploaded file
        self.uploaded_file = ttk.Label(self, text=f"Uploaded file is : {word}", font=("Helvetica", 12))
        self.uploaded_file.place(x=10, y=150) 
        self._file_upload_ = word
        
    def run_uclid(self):
        """_summary_
        """
        #print("We are inside the run Uclid function") 
        if self._file_upload_ is not  None:
            #print("we got the file")
            # Create an instance of the UclidRunner class
            uclid_runner = UclidRunner()
            result = uclid_runner.run_uclid5_command(self._file_upload_)      
            decoded_result=result.decode('utf8').replace("'", '"')         
                         
            # Convert the result to a JSON string
            json_result = orjson.loads(decoded_result) # pylint: disable=maybe-no-member

            # Display the result in the custom text widget
            #self.result_text.delete(1.0, END)  # Clear previous content
                                     
            # Uclid5 sections
            output_text = json_result.get("output", "")
            error_text = json_result.get("error", "")
            
            #Check if there are any errors in the scripts
            if error_text != "":
                self.result_text.pack_forget()
                self.scrollbar.pack_forget()
                self.result_text.insert(END, "\nError: ")
                self.result_text.insert(END, f"UCLID5 failed to run properly, Please fix these Errors\n{error_text}", "error")
                
            elif "Syntax error" in output_text:
                self.result_text.pack_forget()
                self.scrollbar.pack_forget()
                self.result_text.insert(END, "\nCheck Syntax: ")
                self.result_text.insert(END, f"Please fix these Syntax Error(s): \n{output_text}", "syntaxerror")
                
            else:  
                # Display the result in the custom text widget
                self.result_text.delete(1.0, END)  # Clear previous content
                
                # Check the summary if it is there.           
                
                uclid_summary = ProcessUclidResults()
                #passed,failed,inderteminated = uclid_summary.get_summary(output_text)
                #print(passed,failed,inderteminated)
                
                # with the json results, check if the file contains Counterexamples
                if uclid_summary.check_for_CEX:
                    cex_steps = uclid_summary.get_CEX(output_text)
                    passed,failed,inderteminated = uclid_summary.get_summary(output_text)
                    self.data = cex_steps
                    self.passed = passed
                    self.failed = failed
                    self.inderteminated = inderteminated
                     
                    #self.save_CEX_to_json(cex_steps,passed,failed, inderteminated)
                    # Then create 
                    # Display column labels
                    self.create_column_labels()

                    # Display data for the current page
                    self.display_current_page()
                    
                else:                    
                    self.when_no_cex(output_text)
                    
                    
        else:
            self.result_text.pack_forget()
            self.scrollbar.pack_forget()
            #print("it seems file is none Prof")
            # Clear previous content
            self.result_text.delete(1.0, END)  # Clear previous content
            self.result_text.insert(END, "\nNo File Chosen: ")
            self.result_text.insert(END, "Please Upload file first", "nofile")
            #self.result_text.place(x=200, y=400)
           # self.scrollbar.place(x=1680, y=400, height=self.text_height_in_pixels)  # Set the height to match the Text widget

            
    def when_no_cex(self, word):
        ##############################
         # Clear previous content
        self.result_text.delete(1.0, END)  # Clear previous content
        self.result_text.insert(END, "Output: \n")
        self.result_text.insert(END, word, "reportWithoutCEX")
                    
        # Create the Text widget
        #self.result_text = Text(self, wrap="word", width=80, height=10)
        self.result_text.place(x=200, y=400)   
        # Configure tags for different sections
        self.result_text.tag_configure("output", foreground="green")
        self.result_text.tag_configure("error", foreground="red")
        ############################
        
    #############################END #######################################################################     
            
    def create_column_labels(self):
        # Create column labels
        columns = ["No:","Step", "Status"]
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
        total_passed = self.passed
        total_passed_text = "Assertation Passed"
        total_failed = self.failed
        total_failed_text = "Assertations Failed"
        total_inderterminate = self.inderteminated
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
                if col == 2 and value == "FAILED":
                    bg_color = "red"
                label = HoverLabel(self.table_frame, text=value, background=bg_color, padding=(10,20), borderwidth=1,
                relief="solid",
                font=("Helvetica", 10), link=item[-1] if col == 2 else None)
                label.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                label.bind("<Button-1>", self.open_link)

         # Display summary label
        total_failed_label = ttk.Label(self, text=f"{total_failed} {total_failed_text}", font=("Helvetica", 18), background="white", borderwidth=1, relief="flat",padding=(30,30) )
        total_failed_label.place(x=100, y= 500)        
        #total_failed_label_1 = ttk.Label(self, text=total_failed_text, font=("Helvetica", 20, "bold"))
        #total_failed_label_1.place(x=500, y=350)
        
        total_passed_label = ttk.Label(self, text=f"{total_passed} {total_passed_text}", font=("Helvetica", 18), background="white", borderwidth=1, relief="flat",padding=(30,30) )
        total_passed_label.place(x=100, y=650)        
        #total_passed_label_1 = ttk.Label(self, text=total_passed_text, font=("Helvetica", 20))
        #total_passed_label_1.place(x=500, y=500 )
        
        total_inderterminated_label = ttk.Label(self, text=f"{total_inderterminate} {total_inderterminate_text}", font=("Helvetica", 18), background="white", borderwidth=1, relief="flat",padding=(20,30) )
        total_inderterminated_label.place(x=100, y=800)
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
            self.data = [row for row in self.data if filter_text.lower() in " ".join(row).lower()]
        else:
            self.data = self.data.copy()
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