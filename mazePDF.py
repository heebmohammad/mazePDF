# mazePDF - Graphical user interface to work with pdf files
# by: Mohammad Heeb
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# import
import tkinter as tk
from AppDisplays import MainWindow

# ****************************************************************************************************

def openPopupWindow(title):
    popup_window = tk.Toplevel()
    popup_window.title(title)
    popup_window.config(width=300, height=200)
    # get focus automatically
    popup_window.focus()
    # modal window (disable user from using the main window while the popup window is visible)
    popup_window.grab_set()

# ****************************************************************************************************

# when mazePDF starts
def startMaze():
    root = MainWindow()
    root.updateDisplay()
    # fixing the blur UI on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        root.mainloop()

# when mazePDF ends
def endMaze():
    # save stats ???
    print("Thank you for using mazePDF!")

# ====================================================================================================

startMaze()
endMaze()