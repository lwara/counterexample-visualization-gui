from pathlib import Path
from tkinter import Label, Toplevel, Tk, Canvas, Button,StringVar, PhotoImage
from mainWindow.dashboard.gui1 import Dashboard

from mainWindow.fileUpload.gui import Upload
from mainWindow.reportExecution.gui import Report

def mainWindow():  
    
    Uclid5GUI()   
    
class Uclid5GUI(Toplevel):
    
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
          # Lazy import to resolve circular dependency
        
        
        #self.window = window
        #self.setup_gui()
        #self.create_elements()
            

    
        self.geometry("2500x2100")
        self.configure(bg="#E5E4E2")
        self.title("UCLID5 GUI- Simple way of presenting Counterexamples")
        self.current_window = None 
        #self.current_window_label = StringVar()
        
        self.canvas = Canvas(
            self,
            bg="#E5E4E2",
            height=2100,
            width=2500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        self.canvas.create_rectangle(
            405.0,
            0.0,
            2500.0,
            2100.0,
            fill="#D9D9D9",
            outline=""
        )         

         
        # Load the image file
        self.logo_image = PhotoImage(file=self.relative_to_assets("uclid5-image.png"))

        # Create a label to display the logo
        self.logo_label = Label(self, image=self.logo_image)
        self.logo_label.place(
            x=0,
            y=0,
            width=405.0,
            height=200.0
        )
        
        self.university_logo_image = PhotoImage(file=self.relative_to_assets("logo.png"))
        # Create a label to display the logo
        self.university_logo_label = Label(self, image=self.university_logo_image)
        self.university_logo_label.place(
            x=0,
            y=1700,
            width=405.0,
            height=400.0
        )
         
        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        self.button_3 = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_1_click("upload"),
            relief="flat"
        )
        self.button_3.place(
            x=0.0,
            y=488.0,
            width=405.0,
            height=100.0
        )

    
        self.windows = {
            "upload": Report(self),
             "dash" : Dashboard(self),
             "report" : Report(self)
            
             
        }
        self.on_button_1_click("dash")
        

        self.current_window.place(x=405, y=0, width=2095.0, height=2100.0)
        self.current_window.tkraise()
        
        self.resizable(True, False)
        self.mainloop()

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")
        return ASSETS_PATH / Path(path)

    def on_button_1_click(self, name ):
        #print("type of self")
        
        #print(type(self))
        for window in self.windows.values():
            window.place_forget()                       

        #set current window
        self.current_window = self.windows.get(name)
        # show the screen of the button placed
        self.windows[name].place(x=405, y=0, width=2095.0, height=2100.0)
        
  
         


