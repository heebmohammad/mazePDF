# mazePDF - Graphical user interface to work with pdf files
# by: Mohammad Heeb
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# import
import tkinter as tk
from AppDisplays import MainWindow
from InputWindow import InputWindow

# when mazePDF starts
def startMaze():
    root = MainWindow()
    root.updateDisplay()
    # InputWindow(title="test").packTest()
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