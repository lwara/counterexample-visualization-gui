from pathlib import Path
from tkinter import Toplevel, Tk, Canvas, Button,StringVar, PhotoImage
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
        self.configure(bg="#0F4A63")
        self.title("UCLID5 GUI- Simple way of presenting Counterexamples")
        self.current_window = None 
        #self.current_window_label = StringVar()
        
        self.canvas = Canvas(
            self,
            bg="#0F4A63",
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

        self.canvas.create_text(
            1050.0,
            2000.0,
            anchor="nw",
            text="Copyright-University of edinburgh Project",
            fill="#428EA6",
            font=("MontserratRoman Bold", 32 * -1)
        )

        self.canvas.create_text(
            34.0,
            33.0,
            anchor="nw",
            text="UCLID5",
            fill="#FFFFFF",
            font=("Montserrat Bold", 24 * -1)
        )

        button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_1_click("upload"),
            relief="flat"
        )
        self.button_1.place(
            x=37.0,
            y=1924.0,
            width=157.0,
            height=57.0
        )

        self.canvas.create_text(
            1077.0,
            14.0,
            anchor="nw",
            text="ABOUT THE DASHBOARD",
            fill="#0F4A63",
            font=("MontserratRoman Bold", 32 * -1)
        )

        self.canvas.create_text(
            650.0,
            278.0,
            anchor="nw",
            text="This is a Uclid5 Graphic User Interface (GUI). "
                 "It has two main functionalities :\n\n"
                 "You can run code directly on the Gui by clicking ‘Run Code’\n"
                 "You can upload a file\n",
            fill="#6F6C6C",
            font=("MontserratRoman Bold", 24 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_1_click("upload"),
            relief="flat"
        )
        self.button_2.place(
            x=0.0,
            y=288.0,
            width=405.0,
            height=100.0
        )

        self.button_image_3 = PhotoImage(
            file=self.relative_to_assets("button_3.png"))
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

        self.button_image_4 = PhotoImage(
            file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print(""),
            relief="flat"
        )
        self.button_4.place(
            x=0.0,
            y=388.0,
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
        
  
        #print("button_1 clicked")

    def on_button_2_click(self):
        print("button_2 clicked")

    def on_button_3_click(self):
        print("button_3 clicked")

    def on_button_4_click(self):
        print("button_4 clicked")


