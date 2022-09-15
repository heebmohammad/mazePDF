from cgitb import text
from distutils.command.config import config
import os
import tkinter as tk
from tkinter import TclError

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

# Singleton App Preferences Class
class AppPreferences():
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(AppPreferences, cls).__new__(cls)
        return cls.__instance

    @classmethod
    def initializeDefaultPreferences(cls):
        self = cls.__instance
        
        # last opened directory
        self.last_directory = '/'

        # default display mode
        self.display_mode = DISPLAY_MODES[0]

        # theme color
        self.theme_color = THEME_COLORS["DEFAULT_GREEN"]

        # prepare assets
        self.assets_dict = ASSETS_DICTIONARY
        self.initializeAssets()

    def initializeAssets(self):
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

    def getFileIconAssetKey(self, file_type):
        if file_type == ".pdf":
            return ("pdf-file-icon")
        elif file_type == ".png":
            return ("png-file-icon")
        elif file_type == ".jpg" or file_type == ".jpeg":
            return ("jpeg-file-icon")
        elif file_type == ".bmp":
            return ("bmp-file-icon")
        elif file_type == ".tiff":
            return ("tiff-file-icon")
        elif file_type == ".gif":
            return ("gif-file-icon")
        else:
            return ("any-file-icon")

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
        frame.config(bd=0, bg=self.getBackgroundColor())

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

    def getItemControlButton(self, container, text, key_asset, func):
        button = tk.Button(container, 
            image=self.getAsset(key_asset),
            text=text,
            command=func
        )
        self.setFrameControlStyle(button)
        return button

    # get styled controller
    def getStyledController(self, container, text, func=""):
        button = tk.Button(container, text=text, command=func)
        self.setControllerStyle(button)
        return button

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

    # get styled label
    def getStyleLabel(self, container, label_text, is_bold=False):
        foreground_color = self.getForegroundColor()
        background_color = self.getBackgroundColor()
        label_font = ("Century Gothic", 12)
        if is_bold:
            label_font = ("Century Gothic", 12, "bold")
        return tk.Label(container,
            text=label_text,
            background=background_color,
            foreground=foreground_color,
            font=label_font)

    def getIsEncryptedLabel(self, container, is_encrypted):
        foreground_color = self.getForegroundColor()
        background_color = self.getBackgroundColor()
        label_font = ("Century Gothic", 10)
        label = tk.Label(container,
            underline=1,
            background=background_color,
            foreground=foreground_color,
            font=label_font,
            compound=tk.LEFT)
        if is_encrypted:
            lock_image = self.getAsset("lock-lock")
            lock_text=" Encrypted"
            label.config(text=lock_text, image=lock_image)
        else:
            lock_image = self.getAsset("lock-unlock")
            lock_text=" Decrypted"
            label.config(text=lock_text, image=lock_image)

        return label

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
