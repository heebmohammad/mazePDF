import os
import tkinter as tk
from tkinter import TclError

# Initial Preferences

# modes of mazePDF display
DISPLAY_MODES = ("DARK", "LIGHT")

# theme colors
THEME_COLORS = {
    "DEFAULT_GREEN" : "#4CAF50",
    "DEFAULT_RED" : "#F40F02",
    "DEFAULT_BLACK" : "#000000",
}

# mazePDF assets
MAIN_ICON_PATH = './assets/icons/maze_pdf_icon.ico'
ASSETS_DIR_PATH = './assets/'
ASSETS_DICTIONARY = {
    "main-logo" : {"path": 'images/maze_pdf_logo.png'},
    "white-browse-files" : {"path": 'images/Folder-Open-icon.png'},
    "any-file-icon" : {"path": 'soft_icons/document_icons/Document-icon.png'},
    "pdf-file-icon" : {"path": 'soft_icons/document_icons/Adobe-PDF-Document-icon.png'},
    "png-file-icon" : {"path": 'soft_icons/document_icons/Image-PNG-icon.png'},
    "bmp-file-icon" : {"path": 'soft_icons/document_icons/Image-BMP-icon.png'},
    "gif-file-icon" : {"path": 'soft_icons/document_icons/Image-GIF-icon.png'},
    "jpeg-file-icon" : {"path": 'soft_icons/document_icons/Image-JPEG-icon.png'},
    "tiff-file-icon" : {"path": 'soft_icons/document_icons/Image-TIFF-icon.png'},
    "item-frame-up" : {"path": 'soft_icons/button_icons/Button-Upload-icon.png'},
    "item-frame-down" : {"path": 'soft_icons/button_icons/Button-Download-icon.png'},
    "delete-file" : {"path": 'soft_icons/button_icons/Button-Delete-icon.png'},
    "add-file-gray" : {"path": 'soft_icons/button_icons/Button-Blank-Gray-icon.png'},
    "lock-lock" : {"path": 'soft_icons/state_icons/Lock-Lock-icon.png'},
    "lock-unlock" : {"path": 'soft_icons/state_icons/Lock-Unlock-icon.png'}
}

# ****************************************************************************************************

class AppPreferences():
    
    def __init__(self):
        # last opened directory
        self.last_directory = '/'

        # default display mode
        self.display_mode = DISPLAY_MODES[0]

        # theme color
        self.theme_color = THEME_COLORS["DEFAULT_GREEN"]

        # prepare assets
        self.assets_dict = ASSETS_DICTIONARY
        self.initialAssets()

    def initialAssets(self):
        for key, image_dict in self.assets_dict.items():
            try:
                image_dict["src"] = tk.PhotoImage(file= ASSETS_DIR_PATH + image_dict.get("path"))
            except TclError as e:
                print("could not load " + key + "asset")
                # the tcl equivalent to None is ""
                image_dict["src"] = ""

    def getAsset(self, key_asset):
        image_dict = self.assets_dict.get(key_asset)
        if image_dict == None:
            return ""
        else:
            return image_dict.get("src", "")

    def getFileIconAsset(self, file_type):
        if file_type == ".pdf":
            return self.getAsset("pdf-file-icon")
        elif file_type == ".png":
            return self.getAsset("png-file-icon")
        elif file_type == ".jpg" or file_type == ".jpeg":
            return self.getAsset("jpeg-file-icon")
        elif file_type == ".bmp":
            return self.getAsset("bmp-file-icon")
        elif file_type == ".tiff":
            return self.getAsset("tiff-file-icon")
        elif file_type == ".gif":
            return self.getAsset("gif-file-icon")
        else:
            return self.getAsset("any-file-icon")

    def getLastDirectory(self):
        return self.last_directory

    def setLastDirectory(self, file_path):
        self.last_directory = os.path.dirname(file_path)

    @staticmethod
    def getAnalogousColor(color):
        if (color == THEME_COLORS["DEFAULT_GREEN"]):
            return "#3E8E41"
        else:
            return color #???

    def getBackgroundColor(self):
        if self.display_mode == "DARK":
            return "#000000"
        elif self.display_mode == "LIGHT":
            return "#FFFFFF"

    def getForegroundColor(self):
        if self.display_mode == "DARK":
            return "#FFFFFF"
        elif self.display_mode == "LIGHT":
            return "#000000"

    # set frame background color
    def setFrameColor(self, frame):
        frame.config(bg=self.getBackgroundColor())

    # set button color
    def setButtonColor(self, button, follow_theme=False):
        background_color = "#000000"
        foreground_color = "#FFFFFF"
        if follow_theme:
            background_color = self.theme_color
            foreground_color = "#FFFFFF" #???
        elif self.display_mode == "DARK":
            background_color = THEME_COLORS["DEFAULT_BLACK"]
            foreground_color = "#FFFFFF"
        elif self.display_mode == "LIGHT":
            background_color = THEME_COLORS["DEFAULT_RED"]
            foreground_color = "#FFFFFF"

        button.config(bg=background_color, activebackground=background_color,
            fg=foreground_color, activeforeground=foreground_color)

        # hover effect
        AppPreferences.changeOnHover(button, 
            AppPreferences.getAnalogousColor(background_color),
            background_color,
            AppPreferences.getAnalogousColor(foreground_color),
            foreground_color)

    # set style of button to red and gray
    def setControllerStyle(self, button):
        button.config(bd=0,
            bg="#E7E7E7",
            activebackground="#E7E7E7",
            fg="black",
            activeforeground="black",
            font = ("Century Gothic", 16, "bold"))
        
        # hover effect
        AppPreferences.changeOnHover(button, "#F44336", "#E7E7E7", "white", "black")

    # set style of button simple style
    def setFrameControlStyle(self, button):
        foreground_color = self.getForegroundColor()
        background_color = self.getBackgroundColor()
        button.config(bd=0,
            bg=background_color, 
            activebackground=background_color,
            fg=foreground_color, 
            activeforeground=foreground_color,
            font = ("Century Gothic", 10, "bold"))

    # function to change properties of button on hover
    @staticmethod
    def changeOnHover(button :tk.Button,
        background_color_on_hover,
        background_color_on_leave,
        foreground_color_on_hover,
        foreground_color_on_leave):  
        # background on entering widget
        button.bind("<Enter>", func=lambda e: button.config(
            background=background_color_on_hover, foreground=foreground_color_on_hover))
    
        # background color on leving widget
        button.bind("<Leave>", func=lambda e: button.config(
            background=background_color_on_leave, foreground=foreground_color_on_leave)) 


    # initial stats and settings ???
    # initial language dictionary ???
