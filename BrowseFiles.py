import tkinter as tk
from tkinter import filedialog as fd
from AppPreferences import AppPreferences
from FileItemFactory import FileItemFactory

# App Preferences
app_style = AppPreferences()

class BrowseFilesButton(tk.Button):
    def __init__(self, container, window):
        super().__init__(container, command=self.selectFiles)
        self.window = window

    # pack Full browse files button
    def packFull(self):
        browse_files_image = app_style.getAsset("white-browse-files")
        self.config(text="Browse...",
            bd=0,
            font = ("Times new roman", 50),
            image=browse_files_image)
        
        app_style.setButtonColor(self, True)
        self.pack(fill=tk.BOTH, expand=True)

    # pack wide add files button
    def packWide(self):
        self.config(text="Add Files")
        app_style.setControllerStyle(self)
        #app_style.setButtonColor(self, True) ???
        self.pack(fill=tk.X)

    # select files command
    def selectFiles(self):
        filenames = fd.askopenfilenames(
            title = "select files...",
            initialdir=app_style.getLastDirectory(),
            filetypes=FileItemFactory.SUPPORTED_FILE_TYPES)

        if len(filenames) != 0:
            app_style.setLastDirectory(filenames[0])
        FileItemFactory.addFileItems(filenames)

        self.window.updateDisplay()