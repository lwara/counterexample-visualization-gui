import json
from pathlib import Path
from tkinter import END, Frame, Text, Scrollbar, Tk, Canvas, Button, PhotoImage, filedialog
#from ttkbootstrap import END, Frame, Text, Scrollbar, Canvas, Button, PhotoImage
import orjson

from checker.file_upload import ProcessUclidResults, UclidRunner
#from mainWindow.gui import Uclid5GUI
#from mainWindow.reportExecution.gui import Report
 

def uploadFile():
    Upload()

class Upload(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        #self.master.geometry("2095x2000")
        self.configure(bg="#D9D9D9")
        self._file_upload_ = None

        self.canvas = Canvas(
            self,
            bg="#D9D9D9",
            height=2000,
            width=2095,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        ##############################
        self.result_text = Text(self, wrap="word", width=100, height=30)         
        # Calculate the height of the Text widget in terms of lines
        text_height_in_lines = int(self.result_text.cget("height"))

        # Create the Text widget
        #self.result_text = Text(self, wrap="word", width=80, height=10)
        self.result_text.place(x=200, y=400)

        # Calculate the height of one line of text in the Text widget
        line_height = self.result_text.tk.call("font", "metrics", self.result_text.cget("font"), "-linespace")

        # Calculate the height of the Text widget in terms of pixels
        text_height_in_pixels = text_height_in_lines * line_height

        # Create the Scrollbar widget
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.result_text.yview)
        self.scrollbar.place(x=1680, y=400, height=text_height_in_pixels)  # Set the height to match the Text widget

        # Configure the Scrollbar to work with the Text widget
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Configure tags for different sections
        self.result_text.tag_configure("output", foreground="green")
        self.result_text.tag_configure("error", foreground="red")
        ############################
        self.canvas.create_text(
            407.0,
            199.0,
            anchor="nw",
            text="Click the button below to upload your file and then Click RUN to execute",
            fill="#428EA6",
            font=("MontserratRoman Bold", 20 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.run_uclid(),
            relief="flat"
        )
        self.button_1.place(
            x=1479.0,
            y=289.0,
            width=187.1875,
            height=60.38232421875
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.get_uploaded_file(),
            relief="flat"
        )
        self.button_2.place(
            x=350.0,
            y=289.0,
            width=218.0,
            height=50.0
        )
        
        self.canvas.create_text(
            831.0,
            27.0,
            anchor="nw",
            text="UPLOAD CODE FILE",
            fill="#428EA6",
            font=("MontserratRoman Bold", 32 * -1)
        )

        self.canvas.create_text(
            57.0,
            58.0,
            anchor="nw",
            text="Go Back",
            fill="#0F4A63",
            font=("MontserratRoman Bold", 20 * -1)
        )

        self.canvas.create_text(
            695.0,
            1925.0,
            anchor="nw",
            text="Copyright-University of Edinburgh Project",
            fill="#428EA6",
            font=("MontserratRoman Bold", 32 * -1)
        )

        self.master.resizable(False, False)
        
     
        
    
    def place_word_on_canvas(self, word):
        # Clear the canvas first
        self.canvas.delete("word_text")
    
        self.canvas.create_text(
            500.0,
            350.0,
            anchor="nw",
            text="file uploaded:" + word,
            fill="#428EA6",
            font=("MontserratRoman Bold", 12 * -1),
            tags= "word_text"            
        )
        

    def run_uclid(self):
        """_summary_
        """
         
        if self._file_upload_ is not  None:
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
                self.result_text.insert(END, "\nError: ")
                self.result_text.insert(END, f"UCLID5 failed to run properly, Please fix these Errors\n{error_text}", "error")
                
            elif "Syntax error" in output_text:
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
                    self.save_CEX_to_json(cex_steps,passed,failed, inderteminated)
                    # 
                    
                else:                    
                    self.result_text.insert(END, "Output: \n")
                    self.result_text.insert(END, output_text, "reportWithoutCEX")
                    
                    
        else:
            # Clear previous content
            self.result_text.delete(1.0, END)  # Clear previous content
            self.result_text.insert(END, "\nNo File Chosen: ")
            self.result_text.insert(END, "Please Upload file first", "nofile")
    #TODO : MAY NEED TO CHNAGE THIS SOME
    
    def save_CEX_to_json(self, cex_steps,passed,failed, inderteminated):
        # Save cex, passed, and failed counts to a file
        print("GET THE FOLLOWING TO SAVE ")
        print(cex_steps,passed,failed,inderteminated)
        data = {
                    "cex": cex_steps,
                    "passed": passed,
                    "failed": failed,
                    "inderteminated": inderteminated
                }
                
        file_path = "checker/cex_results.json"  # Path to the file to save the results
        with open(file_path, "w") as file:
            json.dump(data, file)
            
    def get_uploaded_file(self):
        """_summary_
        """
        #print("select the file")
        file_path = filedialog.askopenfilename(title="Select a UCLID5 file", filetypes=[("UCLID5 Files", "*.ucl")])
        if file_path:
            self._file_upload_ = file_path
            self.place_word_on_canvas(file_path)
            
             

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"/home/tiwonge/Documents/School/IPP/counterexample-visualization-gui/mainWindow/assets/frame2")
        return ASSETS_PATH / Path(path)


 