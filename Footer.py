import tkinter as tk
from tkinter.messagebox import showinfo

from AppPreferences import AppPreferences

# App Preferences
app_style = AppPreferences()

COPYRIGHT_MESSAGE = "Copyright © 2022 Mohammad Heeb. All Rights Reserved."

RESOURCES = ( 
    "Resources:\n"
    + "• tkinter (Python Library) for GUI:\n"
    + "     https://docs.python.org/3/library/tkinter.html" + "\n\n"
    + "• PyPDF2 (Python Library) to support pdf files:\n"
    + "     https://pypdf2.readthedocs.io/en/latest/" + "\n\n"
    + "• PIL (Python Library) to support images:\n"
    + "     https://python-pillow.org/" + "\n\n"
    + "• Soft Icons (assets) by Hopstarter:\n"
    + "     https://iconarchive.com/show/soft-scraps-icons-by-hopstarter.html" + "\n\n"
    )

INFO_MESSAGE = (
    "mazePDF - GUI to work with pdf files \n"
    + "Pre-Alpha Release 09/2022 - 0.1.1a\n"
    + COPYRIGHT_MESSAGE + "\n\n"
    + "check: https://github.com/heebmohammad/mazePDF" + "\n"
    + 60*"─" + "\n"
    + RESOURCES
    )

class Footer(tk.Frame):
    def __init__(self, container, window):
        super().__init__(container)
        self.window = window
        app_style.setFrameColor(self)
        self.bind("<Button-1>", self.tryDisplayMode)
        self.packBottomline()

    def packBottomline(self):
        # copyright label
        self.copyright_label = tk.Label(self, text=COPYRIGHT_MESSAGE)
        app_style.setFooterLabel(self.copyright_label)
        self.copyright_label.bind("<Button-1>", self.showMoreInfo)
        self.copyright_label.pack()
    
    def tryDisplayMode(self, e):
        app_style.changeDisplayMode()
        self.window.updateDisplay()
    
    def showMoreInfo(self, e):
        showinfo(title="mazePDF - © 2022 Mohammad Heeb", message=INFO_MESSAGE)
