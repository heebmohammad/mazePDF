# mazePDF Project 
# - ImageItem.py by Mohammad Heeb
# - add support to: (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif") file types, types supported by PIL
# - python libraries dependency: PIL
# - Item Preview: X
# - Item Controllers: X
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image
from AppPreferences import AppPreferences
from FileItem import FileItem

# App Preferences
app_style = AppPreferences()

class ImageItem(FileItem):
    def __init__(self, file_paht):
        # call super function
        super().__init__(file_paht)
        
        #Load the image
        self.img = Image.open(self.file_path)
        self.image_format = self.img.format
        self.image_width = self.img.size[0]
        self.image_height = self.img.size[1]

    def openFile(self):
        self.img.show()
    
    def getPreview(self, container)-> tk.Frame:
        return ImageItemFrame(self, container)

    def getControllers(self, container, window)-> tk.Frame:
        return ImageItemControllers(self, container, window)

    def saveImageAsPDF(self, save_path):
        if (self.img.mode == "RGBA"):
            self.img = self.img.convert('RGB')
        self.img.save(save_path, "PDF")
    
    def saveImageAs(self, save_path):
        try:
            self.img.save(save_path)
        except OSError as e:
            print(str(e) + " --> solution: converting to RGB...")
            self.img = self.img.convert('RGB')
            self.img.save(save_path)

    def grayscaleImage(self):
        self.img = self.img.convert('L')

    def rotateImage(self):
        self.img = self.img.rotate(45)

    def flipImageVertically(self):
        self.img = self.img.transpose(method=Image.FLIP_TOP_BOTTOM)

    def flipImageHorizontally(self):
        self.img = self.img.transpose(method=Image.FLIP_LEFT_RIGHT)

# ****************************************************************************************************

# Image Item Preview:
class ImageItemFrame(tk.Frame):

    def __init__(self, image_item: ImageItem, container):
        super().__init__(container)
        self.image_item = image_item

        app_style.setFrameColor(self)

        # open file button (file icon)
        self.open_file_button = app_style.getItemControlButton(self, 
            "open image",
            app_style.getFileIconAssetKey(self.image_item.file_type), 
            self.image_item.openFile)
        self.open_file_button.grid(row=0, column=0, rowspan=3, sticky=tk.NS)

        # file name
        self.file_name_label = app_style.getStyleLabel(self, "name: " + self.image_item.getFileName(), True)
        self.file_name_label.grid(row=0, column=1, sticky=tk.SW)

        # image width
        self.image_width_label = app_style.getStyleLabel(self, "width: " + str(image_item.image_width))
        self.image_width_label.grid(row=1, column=1, sticky=tk.SW)

        # image height
        self.image_height_label = app_style.getStyleLabel(self, "height: " + str(image_item.image_height))
        self.image_height_label.grid(row=2, column=1, sticky=tk.SW)

# ****************************************************************************************************

# Image Item Controllers
class ImageItemControllers(tk.Frame):
    def __init__(self, image_item: ImageItem, container, window):
        super().__init__(container)
        self.image_item = image_item
        self.window = window

        app_style.setFrameColor(self)

        self.rows = [tk.Frame(self), tk.Frame(self)]
        self.rows[0].pack(fill=tk.X)
        self.rows[1].pack(fill=tk.X)

        # convert to pdf button
        app_style.packController(self.rows[0], "Convert to PDF", self.saveImageAsPDF)

        # save as button
        app_style.packController(self.rows[0], "Save AS...", self.saveImageAs)

        # grayscale button
        app_style.packController(self.rows[0], "Grayscale", self.grayscaleImage)

        # blur button
        app_style.packController(self.rows[0], "Blur", "")

        # resize button
        app_style.packController(self.rows[1], "Resize")

        # rotate button
        app_style.packController(self.rows[1], "Rotate")

        # flip top-bottom button
        app_style.packController(self.rows[1], "Vertical Flip", self.flipImageVertically)

        # flip left-right button
        app_style.packController(self.rows[1], "Horizontal Flip", self.flipImageHorizontally)

# ====================================================================================================

    def saveImageAsPDF(self):
        try:
            save_file_path  =  fd.asksaveasfilename(
                title = "save image as pdf",
                initialdir = app_style.getLastDirectory(),
                initialfile = self.image_item.file_name + ".pdf",
                defaultextension=".pdf",
                filetypes = (("pdf file", "*.pdf"), ("All Files", "*.*")))

            if (save_file_path != ''):
                self.image_item.saveImageAsPDF(save_file_path)
                app_style.setLastDirectory(save_file_path)
        except Exception as e:
            FileItem.showSomethingWentWrong("error converting " + self.image_item.getFileName() + " to pdf", e)

    def saveImageAs(self):
        try:
            save_file_path  =  fd.asksaveasfilename(
                title = "save image as...",
                initialdir = app_style.getLastDirectory(),
                initialfile = self.image_item.getFileName(),
                defaultextension= self.image_item.file_type,
                filetypes = (("png file", "*.png"), ("All Files", "*.*")))

            if (save_file_path != ''):
                self.image_item.saveImageAs(save_file_path)
                app_style.setLastDirectory(save_file_path)
        except Exception as e:
            FileItem.showSomethingWentWrong("error saving " + self.image_item.file_name, e)

    def grayscaleImage(self):
        try:
            self.image_item.grayscaleImage()
        except Exception as e:
            FileItem.showSomethingWentWrong("error grayscaling " + self.image_item.file_name, e)

    def flipImageVertically(self):
        try:
            self.image_item.flipImageVertically()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to flip " + self.image_item.file_name, e)

    def flipImageHorizontally(self):
        try:
            self.image_item.flipImageHorizontally()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to flip " + self.image_item.file_name, e)

# ****************************************************************************************************
