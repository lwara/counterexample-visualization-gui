
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/tiwonge/Documents/School/IPP/build/assets/frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("2095x2000")
window.configure(bg = "#D9D9D9")


canvas = Canvas(
    window,
    bg = "#D9D9D9",
    height = 2000,
    width = 2095,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1213.0,
    y=257.0,
    width=312.9017333984375,
    height=124.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=1704.0,
    y=255.0,
    width=293.78948974609375,
    height=124.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=1803.0,
    y=66.0,
    width=220.0,
    height=82.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=171.0,
    y=263.0,
    width=306.0,
    height=124.0
)

canvas.create_text(
    860.0,
    48.0,
    anchor="nw",
    text="EXECUTION REPORT\n",
    fill="#0F4A63",
    font=("MontserratRoman Bold", 32 * -1)
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=744.0,
    y=263.0,
    width=303.0,
    height=124.0
)

canvas.create_text(
    101.0,
    98.0,
    anchor="nw",
    text="Go Back",
    fill="#0F4A63",
    font=("MontserratRoman Bold", 20 * -1)
)

canvas.create_rectangle(
    101.0,
    495.0,
    1998.0,
    1862.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    802.0,
    567.0,
    anchor="nw",
    text="Here are the details",
    fill="#000000",
    font=("MontserratRoman Bold", 40 * -1)
)

canvas.create_text(
    695.0,
    1937.0,
    anchor="nw",
    text="Copyright-University of edinburgh Project",
    fill="#428EA6",
    font=("MontserratRoman Bold", 32 * -1)
)
window.resizable(False, False)
window.mainloop()
