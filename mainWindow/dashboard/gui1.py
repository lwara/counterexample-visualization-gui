from pathlib import Path
from tkinter import Tk, Canvas,Frame, PhotoImage


def dashboard():
    Dashboard()
    
class Dashboard(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master,*args, **kwargs)
        
        self.master =master
        self.configure(bg="#D3D3D3")
        #self.geometry("2095x2000")
        self.canvas = Canvas(
            self,
            bg="#D3D3D3",
            height=2000,
            width=2095,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_text(
            684.0,
            47.0,
            anchor="nw",
            text="ABOUT THE INTERFACE",
            fill="#000000",
            font=("MontserratRoman Bold", 32 * -1)
        )

        self.canvas.create_text(
            200.0,
            460.0,
            anchor="nw",
            text="This is a Uclid5 Graphic User Interface (GUI). It has two main functionalities :\n\n"
                 "1.You can run code directly \n"
                 "2.You can upload a file\n\n"
                 " Please click on 'Run Uclid' button to start\n\n\n"
                 "Happy Coding :)",
            fill="#000000",
            font=("MontserratRoman Bold", 24 * -1)
        )
        # Draw a horizontal line
        line_header_canvas = Canvas(self, width=1250, height=3, bg="black")
        line_header_canvas.create_line(0, 0, 100, 0, width=2)
        line_header_canvas.place(x=500, y=110)
        #self.master.resizable(False, False)

 
