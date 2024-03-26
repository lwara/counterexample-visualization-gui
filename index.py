import tkinter as tk
from mainWindow.gui import mainWindow
 
 
 # a temporary tkinter window to start the application
root =tk.Tk()
root.withdraw()

if __name__ == "__main__":
    # call the main window
    mainWindow()
    root.mainloop()