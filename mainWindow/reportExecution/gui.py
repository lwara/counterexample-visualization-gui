import csv
import json
import os
import re
import tkinter as tk
from tkinter import END, Canvas, LabelFrame, Menu, Menubutton, Scrollbar, Text, ttk
from tkinter import filedialog
from tkinter import Frame
from tkinter import messagebox as msg

import orjson
import time 
#from checker.run_bmc import ProcessUclidResults, UclidRunner
from checker.run_ltl import ProcessUclidResults, UclidRunner

#TODO:

#1. edit the pop up window
#2. the uploaded file must open and be displayed on the text area -DONE
#3. the run code button must be working DONE
#4. Write an email. DONE
#5. Show which counterexample corresponds to which assertion. DONE
#6. when there are multiple counterexamples, the code is multiplying the times. eg cex is appearing more than once DONE
#7. when thr run command it clicked, it should clear the 'file uploaded variable' and text widget
#8. when there is no file selected, then  a window must appear DONE
#9. Have a sample basic code for uclid5, DONE
#10. if the user is on the text area, bind command to run the code. e.g <ctl> +r, to run, ctl_s to save etc
#11. SAVE code button not working DONE
#12. find a way of displaying the error


def counterExampleReport():
    Report()
    
class Report(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        #self.master.geometry("2095x2000")
        self.configure(bg="#D9D9D9")  
        
        
        self._file_upload_ = None   # this keeps the directory of the uploaded file. 
        self._file_saved_from_text_area_ = None # this keeps the temporary directory for written code.    
        self.passed = 0
        self.failed = 0
        self.inderteminated = 0
        
         
        self.data = []
        self.original_data = self.data # this will keep the orignal data
        # Display Heading of the Report
        heading_label = ttk.Label(self, text="CounterExample Visualization GUI", font=("Helvetica", 24, "bold"))
        heading_label.place(x=600, y= 10)
        
        # Draw a horizontal line
        line_header_canvas = Canvas(self, width=1250, height=3, bg="black")
        line_header_canvas.create_line(0, 0, 100, 0, width=2)
        line_header_canvas.place(x=500, y=60)
               
        # for showing uploaded file
        self.uploaded_file = ttk.Label(self, text="Uploaded file is : ", font=("Helvetica", 12))
         
        
        # Define a custom style for the save button
        self.style = ttk.Style()
        self.style.configure("Run.TButton", background="#dfe2e8")
         
        
        #clear and save buttons
        # Create labels that function like buttons
         
        self.clear_code_label = ttk.Label(self, text="Clear", cursor="hand2")
        self.clear_code_label.place(x=700, y=160)
        self.clear_code_label.bind("<Button-1>", lambda event: self.clear_code_editor())
        
        self.boilerplate_code_label = ttk.Label(self, text="Boilerplate", cursor="hand2")
        self.boilerplate_code_label.place(x=500, y=160)
        self.boilerplate_code_label.bind("<Button-1>", lambda event: self.load_boilerplate())
        

        self.run_code_label = ttk.Button(self, text="Run", command=self.run_uclid, style="Run.TButton", cursor="hand2") #ttk.Label(self, text="Run", cursor="hand2")
        self.run_code_label.place(x=970, y=155)
        #run_code_label.bind("<Button-1>", lambda event: self.run_uclid())
        ###############TEXT EDITOR FOR CODE###############
        #### The following creates a menu for the text editor
        self.file_menu_button = Menubutton(self, text="File", direction="below", cursor="hand2", background="#E5E4E2", width=10)
        self.file_menu_button.place(x=10, y=150)
        self.file_menu = tk.Menu(self.file_menu_button, tearoff=0)
        self.file_menu_button["menu"] = self.file_menu

        self.file_menu.add_command(label="Open File", command=self.get_uploaded_file)
        self.file_menu.add_command(label="Boilerplate", command=self.load_boilerplate)
        self.file_menu.add_command(label="Save", command=self.save_code)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Run Code", command=self.run_uclid)
        # Create a Edit menu button
        menubutton = Menubutton(self, text="Edit", direction="below", cursor="hand2", width=10, background="#E5E4E2")
        # Create pull down menu
        menubutton.menu = Menu(menubutton, tearoff = 0)
        menubutton["menu"] = menubutton.menu
        # Add some commands
        menubutton.menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        menubutton.menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        menubutton.menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        menubutton.menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        menubutton.place(x=250, y=150)

        # ####Here is the text-area code 
        self.line_numbers = Text(self, width=4,height=30, takefocus=0, border=0,
                                 background='#C0C0C0', state='disabled')
        self.line_numbers.place(x=1, y=200)        

        self.result_text = Text(self, wrap="none", width=70, height=30)         
        # Calculate the height of the Text widget in terms of lines
        text_height_in_lines = int(self.result_text.cget("height"))
        self.result_text.place(x=85, y=200) 
        
        # create a label frame
        # This will create a LabelFrame for Terminal
        self.label_frame_terminal = LabelFrame(self, text='TERMINAL')
        self.label_frame_terminal.place(x=1240, y=150, width=1050, height=1050)
        
        # This will create a LabelFrame for Code editor
        self.label_frame_code_editor = LabelFrame(self, text='CODE EDITOR')
        #self.label_frame_code_editor.place(x=10, y=100, width=1200, height=1200)
 
 
        # This will create a LabelFrame for Counter example 
        self.label_frame_terminal = LabelFrame(self, text='COUNTER EXAMPLE TRACE')
        self.label_frame_terminal.place(x=50, y=1200, width=2200, height=890)
 
        # this text area is for showing errors, or if no counter examples were found 
        self. terminal_uclid5= Text(self, wrap="word", width=60, height=30, background="dark grey")      
        self.terminal_uclid5.place(x=1280, y=200) 
        
        
        # Calculate the height of one line of text in the Text widget
        line_height = self.result_text.tk.call("font", "metrics", self.result_text.cget("font"), "-linespace")

        # Calculate the height of the Text widget in terms of pixels
        self.text_height_in_pixels = text_height_in_lines * line_height

        # Create the Scrollbar widget- vertical
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.result_text.yview)
        self.scrollbar.place(x=1210, y=200, height=self.text_height_in_pixels)  # Set the height to match the Text widget
        
        # create the Scroll widget - Horizontal
        self.scrollbar_horizontal = Scrollbar(self, orient="horizontal", command=self.result_text.xview)
        self.scrollbar_horizontal.place(x=85, y=1160, width=1125)  # Set the height to match the Text widget
        
        # Create the Scrollbar for line number- vertical
        self.scrollbar_line_number = Scrollbar(self, orient="vertical", command=self.line_numbers.yview)
        self.scrollbar_line_number.place(x=70, y=200, height=self.text_height_in_pixels)  # Set the height to match the Text widget
        
        # create the Scroll terminal - Horizontal
        self.scrollbar_terminal = Scrollbar(self, orient="vertical", command=self.terminal_uclid5.yview)
        self.scrollbar_terminal.place(x=2245, y=200, height=self.text_height_in_pixels)  # Set the height to match the Text widget
        
        # Configure the Scrollbar to work with the Text widget
        self.result_text.config(yscrollcommand=self.scrollbar.set)
        self.result_text.config(xscrollcommand=self.scrollbar_horizontal.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar_line_number.set)
        self.terminal_uclid5.config(yscrollcommand=self.scrollbar_terminal.set)

        self.result_text.bind("<KeyRelease>", self.update_line_numbers)
        self.result_text.bind("<MouseWheel>", self.update_line_numbers)
        self.result_text.bind("<Button-1>", self.update_line_numbers)
        self.result_text.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
        self.result_text.bind("<Control-x>", self.cut_text)
        self.result_text.bind("<Control-c>", self.copy_text)
        self.result_text.bind("<Control-v>", self.paste_text)
        self.result_text.bind("<Control-a>", self.select_all)

        # Configure tags for different sections
        self.terminal_uclid5.tag_configure("output", foreground="green")
        self.terminal_uclid5.tag_configure("error", foreground="red")
        self.terminal_uclid5.tag_configure("nofile", foreground="#7393B3")
        self.terminal_uclid5.tag_configure("exception", foreground="red")
        ############################
        
         
        # Page settings
        self.page_size = 5
        self.current_page = 0
        
         
        # Create pagination buttons
        self.prev_button = ttk.Button(self, text="<Prev", command=self.show_previous_page)
        self.prev_button.place(x=350, y=1310)
        self.next_button = ttk.Button(self, text="Next>", command=self.show_next_page)
        self.next_button.place(x=550, y=1310)

        # Create filter entry
        self.filter_label = ttk.Label(self, text="Filter:")
        self.filter_label.place(x=890, y=1310)
        self.filter_entry = ttk.Entry(self)
        self.filter_entry.bind("<Return>", lambda event: self.apply_filter())
        self.filter_entry.place(x=980, y=1310)
        self.filter_button = ttk.Button(self, text="Apply Filter", command=self.apply_filter)
        self.filter_button.place(x=1340, y=1310)

               
        # Create a frame to hold the table
        self.table_frame = ttk.Frame(self)
        self.table_frame.place(x=130, y=1400, width=1400)
        
        #self.scrollbar_table_frame = Scrollbar(self, orient="vertical", command=self.table_frame.yview)
        #self.scrollbar_table_frame.place(x=2245, y=200, height=self)  # Set the height to match the Text widget
        
        # Configure the Scrollbar to work with the tableframe
        #self.table_frame.config(yscrollcommand=self.scrollbar.set)
        self.summary_label = ttk.Label(self, text="Counterexample Summary", font=("Helvetica", 12, "bold") )
        self.summary_label.place(x=1750, y=1310)
        
        self.passed_label = ttk.Label(self, text="Assertions Passed :", font=("Helvetica", 10) )
        self.passed_label.place(x=1750, y=1400)
        self.passed_label_figure = ttk.Label(self, text="0", font=("Helvetica", 10, "bold") )
        self.passed_label_figure.place(x=2000, y=1400)
        
        self.failed_label = ttk.Label(self, text="Assertion Failed :", font=("Helvetica", 10) )
        self.failed_label.place(x=1750, y=1500)
        self.failed_label_figure = ttk.Label(self, text="0", font=("Helvetica", 10, "bold") )
        self.failed_label_figure.place(x=2000, y=1500)
        
        self.inderterminated_label = ttk.Label(self, text="Assertion Indeterminated :", font=("Helvetica", 10) )
        self.inderterminated_label.place(x=1750, y=1600)
        self.inderterminated_label_figure = ttk.Label(self, text="0", font=("Helvetica", 10, "bold") )
        self.inderterminated_label_figure.place(x=2100, y=1600)
        # here is canvas that will cover the Frame 
        
        table_text_area = Text(self,
            bd=0,
            bg="#E5E4E2",
            fg="#000716",
            highlightthickness=0,
            state='disabled'  # Set the state to 'disabled'
            )
        table_text_area.place(
            x=100.0,
            y=1270.0,
            width=1500.0,
            height=750.0
            )
        self.table_frame.lift()
        self.filter_button.lift()
        self.prev_button.lift()
        self.next_button.lift()
        self.filter_label.lift()
        self.filter_entry.lift()
         
        
        # Add a tooltip to the button
        Tooltip(self.boilerplate_code_label, "Click to load a basic UCLID 5 code structure")
        Tooltip(self.file_menu_button, "Click to open file options e.g, upload and more")
        Tooltip(self.run_code_label, "Click to run code / file uploaded")
        Tooltip(menubutton, "Click to copy, cut, paste code ")
        Tooltip(self.result_text, "Write code here. For a quick start, click Boilerplate button above")
        Tooltip(self.prev_button, "Click to view previous counterexamples")
        Tooltip(self.next_button, "Load next counterexamples")
        Tooltip(self.table_frame, "Click on any row to view the specific traces")
        Tooltip(self.filter_entry, "Type what you want to filter and then click 'Filter'")
        
        self.master.resizable(False, False)
         
    def cut_text(self, event=None):
        self.result_text.event_generate(("<<Cut>>"))

    def copy_text(self, event=None):
        self.result_text.event_generate(("<<Copy>>"))

    def paste_text(self, event=None):
        self.result_text.event_generate(("<<Paste>>"))

    def select_all(self, event=None):
        self.result_text.tag_add("sel", "1.0", "end")
        return 'break'
        
        # Create an instance of the Uclid5GUI class
    def update_line_numbers(self, event=None):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)

        line_count = int(self.result_text.index('end-1c').split('.')[0])
        line_number_string = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.insert(1.0, line_number_string)

        self.line_numbers.config(state=tk.DISABLED)
        
    def on_shift_mouse_wheel(self, event):
        if event.state & 0x1:  # Check if the shift key is held down
            self.result_text.xview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
    # load boilerplate 
    def load_boilerplate(self):
        
        uclid_code = "module <module_name> { \n"\
                    "   // Declarations of variables, types, and functions\n"\
                    "   // Initial states and assignments\n"\
                    "   init {\n"\
                    "       // Initialize variables\n"\
                    "       // Example:\n"\
                    "       // variable = initial_value;\n}\n"\
                    "       // Transition rules\n"\
                    "   next {\n"\
                    "       // Describe how variables change between states\n"\
                    "       // Example:\n"\
                    "       // if (condition) {\n"\
                   "        //     variable' = new_value;\n"\
                   "        // } else {\n"\
                    "       //     variable' = old_value;\n"\
                    "       // }\n}"\
                "   // Assertion checks\n"\
               "    control {\n"\
                    "   // Specify properties or assertions to check\n"\
                    "   // Example:\n"\
                    "   // assert(property_to_check);\n"\
                "   }\n}"
        if self.is_textarea_empty():
            self.result_text.insert(tk.END, uclid_code)
            self.update_line_numbers()
        else:
            if msg.askyesno("Confirmation", "The code editor is not empty. Do you want to clear the written code?"):
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, uclid_code)  
                self.update_line_numbers()     
            
        # Clear code editor
    def clear_code_editor(self):
        if self.is_textarea_empty():
            self.result_text.delete(1.0, tk.END)
        else:
            if msg.showwarning("Confirmation", "The code editor is not empty. Do you want to clear the written code?"):
                self.result_text.delete(1.0, tk.END)

            
        
    def save_code(self):
        code = self.result_text.get("1.0", "end")
        # Ask user to select a file location for saving
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ucl",
            filetypes=[("ucl files", "*.ucl"), ("All files", "*.*")]
        )
        if file_path:
            if os.path.exists(file_path):
                # File already exists, ask user if they want to overwrite
                response = msg.askyesno(
                    "File Exists",
                    "The file already exists. Do you want to overwrite it?"
                )
                if not response:
                    return  # Cancel saving
            # Save data to the selected CSV file
            with open(file_path, "w") as file:
                 file.write(code)
            # Notify the user that the file has been saved
            msg.showinfo("Success ", f"Your code has been saved to:\n{file_path}")
        
    
    def get_uploaded_file(self):
        """_summary_
        """
        #print("select the file")
        file_path = filedialog.askopenfilename(title="Select a UCLID5 file", filetypes=[("UCLID5 Files", "*.ucl")])
        if file_path:
            if self.is_textarea_empty():
                self.result_text.delete(1.0, tk.END)
            else:
                if msg.showwarning("Confirmation", "The code editor is not empty. Do you want to clear the written code?"):
                    self.result_text.delete(1.0, tk.END)

            #self._file_upload_ = file_path
            self.place_word_on_canvas(file_path)
            self.place_code_on_code_editor(file_path)
            
    def place_code_on_code_editor(self, code_file_path):
        # Read content of the selected file
        if code_file_path:
            with open(code_file_path, "r") as file:
                content = file.read()
                # Clear the text widget before inserting new content
                self.result_text.delete(1.0, tk.END)
                # Insert the content into the text widget
                self.result_text.insert(tk.END, content)
        
            
    # This is to show which file has been uploaded                 
    def place_word_on_canvas(self, word):
        # Clear the canvas first   
        self.uploaded_file.pack_forget()     
        # for showing uploaded file
        self.uploaded_file = ttk.Label(self, text=f"Uploaded file is : {word}", font=("Helvetica", 12))
        self.uploaded_file.place(x=200, y=100) 
        self._file_upload_ = word
        
        self.result_text.delete(1.0, END)  # Clear previous content
        self.result_text.insert(END, word, "code_uclid")
                
    def get_text_area_code(self):
        # Get the content of the text widget
        
        print("that means there is something on the text area")
        code = self.result_text.get(1.0, tk.END) # get the code 
        #print(f"this is is the code \n{code}")
        # Write the code to a temporary file
        with open("temp/uclid5-code.ucl", "w") as file:
            file.write(code)
        self._file_upload_="temp/uclid5-code.ucl"      
            
        
    def is_textarea_empty(self):
        # Get the content of the textarea
        content = self.result_text.get("1.0", "end-1c")  # "1.0" is the start position, "end-1c" excludes the newline at the end
    
        # Check if the content is empty
        if not content:
            return True
        else:
            return False
        
    def validate_and_parse_json(self,json_string):
        try:
            print("THis is the json file to validate :")
            print(json_string)
            print("********************")
            decoded_string = json_string.decode('utf8')
            print("decoding done ")
            print(decoded_string)
            print("********************")
            preprocessed_string = decoded_string.replace("'", '"')
            print("preprocessing done")
            print(preprocessed_string)
            print("*********************")
            # Preprocess the JSON string
            
        
            # Attempt to load the JSON string
            parsed_json = orjson.loads(preprocessed_string) # pylint: disable=maybe-no-member
            return parsed_json
        except json.JSONDecodeError as e:
            return ({"exception": str(e)})
        
     
    
    def run_uclid(self):
        """_summary_
        """
        global start_time
        start_time = time.time()  # Start the timer
        
        print("printing start time ")
        print(start_time )
        self.clear_table()
        self.terminal_uclid5.delete(1.0, END) # clear the whole terminal
        self.clear_update_label_for_summary(0,0,0) # clear the summary content.
        checker = self.is_textarea_empty()
        if checker is False : # or self._file_upload_ is not None: # that means either there is code or the file has been uploaded
            # simply get what is in the text area
            self.get_text_area_code()
            # Create an instance of the UclidRunner class
            uclid_runner = UclidRunner()
            result = uclid_runner.run_uclid5_command(self._file_upload_)  
            #check for errors     
            json_result = self.validate_and_parse_json(result)
            
            
            #decoded_result=result.decode('utf8').replace("'", '"')         
                         #TODO
            
            # Display the result in the custom text widget
            #self.result_text.delete(1.0, END)  # Clear previous content
            if json_result.get("exception", ""):
                self.terminal_uclid5.delete(1.0, END)
                self.terminal_uclid5.insert(END, json_result.get("exception", ""), "exception")
                                        
            # Uclid5 sections
            output_text = json_result.get("output", "")
            error_text = json_result.get("error", "")
            #print(output_text)
            #Check if there are any errors in the scripts
            if error_text :
                
                self.terminal_uclid5.delete(1.0, END)
                self.terminal_uclid5.insert(END, error_text, "error")
                
            if "Syntax error" in output_text:
                #self.result_text.pack_forget()
                #self.scrollbar.pack_forget()
                self.terminal_uclid5.delete(1.0, END)  # Clear previous content                
                self.terminal_uclid5.insert(END, f"\n{output_text}", "syntaxerror")
                
            if output_text:  
                # Display the result in the custom text widget
                #self.result_text.delete(1.0, END)  # Clear previous content
                
                # Check the summary if it is there.           
                
                uclid_summary = ProcessUclidResults()
                #passed,failed,inderteminated = uclid_summary.get_summary(output_text)
                #print(passed,failed,inderteminated)
                
                # with the json results, check if the file contains Counterexamples
                if_counterexample = uclid_summary.check_for_CEX(output_text)
                if if_counterexample:
                    cex_steps = uclid_summary.get_CEX(output_text, self._file_upload_)
                    passed,failed,inderteminated = uclid_summary.get_summary(output_text)
                    self.data = cex_steps
                    self.passed = passed
                    self.failed = failed
                    self.inderteminated = inderteminated                    
                     
                     
                    # Display column labels
                    self.create_column_labels()

                    # Display data for the current page
                    self.display_current_page()
                    
                    # keep the original data for the sake of filters
                    self.original_data = self.data
                    
                else:                    
                    self.when_no_cex(output_text)
                    
                    
        elif checker is True and self._file_upload_ is  None:
            #self.result_text.pack_forget()
            #self.scrollbar.pack_forget()
            #print("it seems file is none Prof")
            # Clear previous content
            #self.result_text.delete(1.0, END)  # Clear previous content
            self.result_text.insert(END, "Please Upload file first or write some uclid 5 code ", "nofile")
            #self.result_text.place(x=200, y=400)
           # self.scrollbar.place(x=1680, y=400, height=self.text_height_in_pixels)  # Set the height to match the Text widget
        elif checker is True and self._file_upload_ is not None:
            self.result_text.insert(END, "Please do not delete here after uploading your file.", "nofile")
        end_time = time.time()  
        print("Processing time ")
        difference_time=end_time-start_time
         # Display totals for counterexamples
        time_take_label = ttk.Label(self, text=f" {difference_time:.2f} seconds to run your code ", font=("Helvetica", 10) )
        time_take_label.place(x=200, y=2050) 
        
                   
    def when_no_cex(self, word):
        ##############################
         # Clear previous content
        self.terminal_uclid5.delete(1.0, END)  # Clear previous content
        #self.terminal_uclid5.insert(END, "Output: \n")
        self.terminal_uclid5.insert(END, word, "reportWithoutCEX")  
        # Configure tags for different sections
        self.terminal_uclid5.tag_configure("output", foreground="green")
        self.terminal_uclid5.tag_configure("error", foreground="red")
        self.terminal_uclid5.tag_configure("nofile", foreground="#7393B3")
        self.terminal_uclid5.tag_configure("exception", foreground="red")                     
            
    def create_column_labels(self):
        # Create column labels
        columns = ["Counter-example","Assertion"]
        for col, column_name in enumerate(columns):
            label = ttk.Label(self.table_frame, text=column_name, font=("Helvetica", 15, "bold"), padding=(10,20), borderwidth=1,    relief="solid")
            label.grid(row=0, column=col, sticky="nsew" )

    def display_current_page(self):
        # Clear previous data from the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
                   
        # Display column labels
        self.create_column_labels()

        # Display data for the current page
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.data))
        # how many counterexamples are there ?
        counterexample_total = len(self.data)
         
        # Display only the first column
        for row, item in enumerate(self.data[start_index:end_index], start=1):
            for col, value in enumerate(item):
                # Choose background color based on row number and status
                bg_color = "lightgray" if row % 2 == 0 else "white"
                if col == 2 and value == "FAILED":
                    bg_color = "red"
                label_column_1 = HoverLabel(self.table_frame, text=item[0], background=bg_color, padding=(10,20), borderwidth=1,
                                relief="solid", font=("Helvetica", 10), link=item[-1] if col == 2 else None)
                label_column_1.grid(row=row, column=0, sticky="nsew", padx=1, pady=1)
                label_column_1.bind("<Button-1>", lambda event, row=row: self.open_trace(row))

                label_column_2 = HoverLabel(self.table_frame, text=item[1], background=bg_color, padding=(10,20), borderwidth=1,
                                relief="solid", font=("Helvetica", 10), link=item[-1] if col == 2 else None)
                label_column_2.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)
                label_column_2.bind("<Button-1>", lambda event, row=row: self.open_trace(row))

         
 
        self.clear_update_label_for_summary(self.passed, self.failed, self.inderteminated)
        
         # Display totals for counterexamples
        total_counterexample_label = ttk.Label(self, text=f" {start_index+1}-{end_index} of {counterexample_total}", font=("Helvetica", 10) )
        total_counterexample_label.place(x=120, y=1310)    
         
        # Configure row and column weights to make the grid resizable
        for i in range(min(len(self.data) - self.current_page * self.page_size, self.page_size) + 1):
            self.table_frame.grid_rowconfigure(i, weight=1)

    def clear_update_label_for_summary(self, passed, failed, inderteminated):
        # Clear the label's text
        self.passed_label_figure.config(text=passed)
        self.failed_label_figure.config(text=failed)
        self.inderterminated_label_figure.config(text=inderteminated)
        
    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        
    def show_previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

    def show_next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_current_page()

    def apply_filter(self):
        filter_text = self.filter_entry.get().strip().lower()  # Ensure lowercase for case-insensitive comparison
        if filter_text:
            filtered_data = []
            for cex, assertion, data in self.data:
                if filter_text in cex.lower() or filter_text in assertion.lower():
                    print("found match : ")
                    filtered_data.append((cex, assertion, data))
                    
            if not filtered_data:
                tk.messagebox.showinfo("No Matches", "No matching text found.")
            else:
                self.data = filtered_data
        else:
            self.data = self.original_data
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
                response = msg.showwarning.askyesno(
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
            msg.showinfo("File Saved", f"The data has been saved to:\n{file_path}")
         
    

    def open_trace(self, row):
         
        
        
        # Get the data for the selected row
        selected_row_data = self.data[row - 1]  # Adjust for zero-based indexing
        
        #print(selected_row_data)
        selected_row_data = list(selected_row_data[2:])
        """data= [['\nStep #0\n  a : 0\n  b : 1\n  c : 2\n  d : 3\n  e : 4\n  f : 5\n', 
             '\nStep #1\n  a : 1\n  b : 0\n  c : 4\n  d : 1\n  e : 7\n  f : 2\n',
             '\nStep #2\n  a : 2\n  b : -1\n  c : 6\n  d : -1\n  e : 10\n  f : -1\n',
             '\nStep #2\n  a : 2\n  b : -1\n  c : 6\n  d : -1\n  e : 10\n  f : -1\n',
             '\nStep #2\n  a : 2\n  b : -1\n  c : 6\n  d : -1\n  e : 10\n  f : -1\n',
             '\nStep #2\n  a : 2\n  b : -1\n  c : 6\n  d : -1\n  e : 10\n  f : -1\n',
             '\nStep #2\n  a : 2\n  b : -1\n  c : 6\n  d : -1\n  e : 10\n  f : -1\n',]]""" 
        CounterexamplePopup(self, selected_row_data)
        
class CounterexamplePopup(tk.Toplevel):
    def __init__(self, master, data):
        super().__init__(master)
        self.data = data
        self.title("Counterexample Trace Table")
        self.geometry("1000x1000+600+600")
        self.resizable(False,False)         
        
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # Add padding here
        

        # Pagination variables
        self.current_page = 0
        self.page_size = 3  # Number of records per page

        # Navigation buttons
        self.prev_button = tk.Button(self, text="Previous", command=self.prev_page)
        self.next_button = tk.Button(self, text="Next", command=self.next_page)

        self.prev_button.pack(side=tk.LEFT)
        self.next_button.pack(side=tk.RIGHT)

        # Display data
        self.display_current_page()

    def display_current_page(self):
        # Clear previous data from the table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Define columns
        columns = ["Step", "Details"]
        for col, column_name in enumerate(columns):
            label = ttk.Label(self.table_frame, text=column_name, font=("Helvetica", 10, "bold"))
            label.grid(row=0, column=col + 1, sticky="nsew", padx=1, pady=1)  # Adjust column index

        # Add an empty column on the left for padding
        self.table_frame.grid_columnconfigure(0, minsize=20)

        # Get data for the current page
        start_index = self.current_page * self.page_size
        end_index = min(start_index + self.page_size, len(self.data[0]))

        selected_row_data = self.data[0][start_index:end_index]

        for row, item in enumerate(selected_row_data, start=1):
            step, details = item.split('\n', 1)

            step_label = HoverLabel(
                self.table_frame, text=f"Step #{start_index + row - 1}", background="white", padding=(10, 20), borderwidth=1,
                relief="solid", font=("Helvetica", 10)
            )
            step_label.grid(row=row, column=1, sticky="nsew", padx=1, pady=1)  # Adjust column index

            details_label = HoverLabel(
                self.table_frame, text=re.sub(r'\nStep #\d+\n', '\n', item), background="white", padding=(10, 20), borderwidth=1,
                relief="solid", font=("Helvetica", 10)
            )
            details_label.grid(row=row, column=2, sticky="nsew", padx=1, pady=1)  # Adjust column index
         # Display totals for counterexamples
        total_counterexample_label = ttk.Label(self, text=f" Displaying :{start_index+1}-{end_index} of {len(self.data[0])}", font=("Helvetica", 10) )
        total_counterexample_label.place(x=400, y=950)    
         
        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        # Enable/Disable navigation buttons based on the current page
        self.prev_button.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if (self.current_page + 1) * self.page_size < len(self.data[0]) else tk.DISABLED)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data[0]):
            self.current_page += 1
            self.display_current_page()

class Tooltip:
    def __init__(self, widget, text=''):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify='left',
                         background='#ffffe0', relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


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