from pathlib import Path
from tkinter import Tk, Canvas,Frame, PhotoImage


def dashboard():
    Dashboard()
    
class Dashboard(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master,*args, **kwargs)
        
        self.master =master
        self.configure(bg="#D9D9D9")
        #self.geometry("2095x2000")
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

        self.canvas.create_text(
            684.0,
            47.0,
            anchor="nw",
            text="ABOUT THE DASHBOARD",
            fill="#0F4A63",
            font=("MontserratRoman Bold", 32 * -1)
        )

        self.canvas.create_text(
            594.0,
            460.0,
            anchor="nw",
            text="This is a Uclid5 Graphic User Interface (GUI). It has two main functionalities :\n\n"
                 "You can run code directly on the Gui by clicking ‘Run Code’\n"
                 "You can upload a file\n",
            fill="#6F6C6C",
            font=("MontserratRoman Bold", 24 * -1)
        )

        #self.master.resizable(False, False)

 
