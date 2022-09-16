# mazePDF Project 
# - ImageItem.py by Mohammad Heeb
# - add support to: (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif") file types, types supported by PIL
# - python libraries dependency: PIL
# - Item Preview: V
# - Item Controllers: X
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image
from AppPreferences import AppPreferences
from FileItem import FileItem, FileItemControllers, FileItemFrame
from InputWindow import InputWindow

# App Preferences
app_style = AppPreferences()

class ImageItem(FileItem):
    def __init__(self, file_paht):
        # call super function
        super().__init__(file_paht)
        
        #Load the image
        self.img = Image.open(self.file_path)
        self.updateSize()
    
    def updateSize(self):
        self.image_width = self.img.width
        self.image_height = self.img.height

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

    def rotateImage(self, angel):
        self.img = self.img.rotate(angel, expand=True)
        self.updateSize()

    def flipImageVertically(self):
        self.img = self.img.transpose(method=Image.FLIP_TOP_BOTTOM)

    def flipImageHorizontally(self):
        self.img = self.img.transpose(method=Image.FLIP_LEFT_RIGHT)

# ****************************************************************************************************

# Image Item Preview:
class ImageItemFrame(FileItemFrame):

    def __init__(self, image_item: ImageItem, container):
        super().__init__(image_item, container)
        self.image_item = image_item
        self.packImagePreview()

    def packImagePreview(self):
        # open file button (file icon)
        self.open_file_button = self.getOpenFileButton()
        self.open_file_button.grid(row=0, column=0, rowspan=3, sticky=tk.NS)

        # file name
        self.file_name_label = self.getFileNameLabel()
        self.file_name_label.grid(row=0, column=1, sticky=tk.SW)

        # image width
        self.image_width_label = app_style.getStyleLabel(self, "width: " + str(self.image_item.image_width))
        self.image_width_label.grid(row=1, column=1, sticky=tk.SW)

        # image height
        self.image_height_label = app_style.getStyleLabel(self, "height: " + str(self.image_item.image_height))
        self.image_height_label.grid(row=2, column=1, sticky=tk.NW)

# ****************************************************************************************************

# Image Item Controllers
class ImageItemControllers(FileItemControllers):
    def __init__(self, image_item: ImageItem, container, window):
        super().__init__(image_item, container, window)
        self.image_item = image_item
        self.packImageControllers()

    def packImageControllers(self):
        
        side = tk.LEFT
        expand = True

        self.rows = self.packRows(1)
        # convert to pdf button
        self.convert_to_pdf_button = app_style.getStyledController(
            self.rows[0], "Convert to PDF", self.saveImageAsPDF)
        self.convert_to_pdf_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # save as button
        self.save_as_button = app_style.getStyledController(
            self.rows[0], "Save AS...", self.saveImageAs)
        self.save_as_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
    #....................................................................................................#
        side = tk.TOP
        expand = True

        self.columns = self.packColumns(3)
        # grayscale button
        self.grayscale_button = app_style.getStyledController(
            self.columns[0], "Grayscale", self.grayscaleImage)
        self.grayscale_button.pack(fill=tk.X, side=side, expand=expand)

        # blur button
        self.blur_button = app_style.getStyledController(
            self.columns[0], "Blur")
        self.blur_button.pack(fill=tk.X, side=side, expand=expand)

        # resize button
        self.resize_button = app_style.getStyledController(
            self.columns[1], "Resize")
        self.resize_button.pack(fill=tk.X, side=side, expand=expand)

        # rotate button
        self.rotate_button = app_style.getStyledController(
            self.columns[1], "Rotate", self.rotateImage)
        self.rotate_button.pack(fill=tk.X, side=side, expand=expand)

        # flip top-bottom button
        self.vertical_flip_button = app_style.getStyledController(
            self.columns[2], "Vertical Flip", self.flipImageVertically)
        self.vertical_flip_button.pack(fill=tk.X, side=side, expand=expand)

        # flip left-right button
        self.horizontal_flip_button = app_style.getStyledController(
            self.columns[2], "Horizontal Flip", self.flipImageHorizontally)
        self.horizontal_flip_button.pack(fill=tk.X, side=side, expand=expand)

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

# ====================================================================================================

    def rotateImage(self):
        try:
            self.input_window = InputWindow(title="rotate image", 
                fields=["angel"], 
                description="enter an angel to rotate the image",
                callback=self.validateAndCallRotate)
        except Exception as e:
            FileItem.showSomethingWentWrong("error rotating " + self.image_item.file_name, e)
        
    def validateAndCallRotate(self, angel):
        if (angel.isnumeric()):
            self.image_item.rotateImage(int(angel))
            self.input_window.closeWindow()
            self.window.updateDisplay()

# ====================================================================================================

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
