import os
import pathlib
import tkinter as tk
from tkinter.messagebox import showerror
from PyPDF2 import PdfFileMerger
from PIL import Image

class FileItem:
    # static methods to work with files

    @staticmethod
    def showSomethingWentWrong(message, exception):
        showerror("something went wrong", message + "\n\nDetails:\n" + str(exception))

    @staticmethod
    def is_valid_file_path(path):
        return (os.path.isfile(path))
    
    @staticmethod
    def get_file_type(path):
        return (pathlib.Path(path).suffix).lower()

    @staticmethod
    def get_file_name(path):
        return (pathlib.Path(path).stem)
    
    @staticmethod
    def get_file_size(path):
        return (os.path.getsize(path))
    
    @staticmethod
    def open_file_by_path(path):
        os.startfile(path)

# ****************************************************************************************************
    # class methods to work with file items list

    # list to store the FileItems created.
    file_items_list = []

    @classmethod
    def getFileItemsCnt(cls):
        return len(cls.file_items_list)
    
    @classmethod
    def getFirstFileItem(cls):
        return FileItem.file_items_list[0]

    @classmethod
    def sortFileItemsList(cls):
        FileItem.file_items_list.sort(key=FileItem.getFileName)

    @classmethod
    def reverseFileItemsList(cls):
        FileItem.file_items_list.reverse()

    @classmethod
    def deleteFileItems(cls, file_item):
        FileItem.file_items_list.remove(file_item)

    @classmethod
    def forewardFileItems(cls, file_item):
        index = FileItem.file_items_list.index(file_item)
        if (index == 0):
            return
        # swap
        FileItem.file_items_list[index], FileItem.file_items_list[index - 1] = FileItem.file_items_list[index - 1], FileItem.file_items_list[index]

    @classmethod
    def backwardFileItems(cls, file_item):
        index = FileItem.file_items_list.index(file_item)
        if (index == len(FileItem.file_items_list) - 1):
            return
        # swap
        FileItem.file_items_list[index], FileItem.file_items_list[index + 1] = FileItem.file_items_list[index + 1], FileItem.file_items_list[index]

    @classmethod
    def getPdfFilesPaths(cls):
        pdf_paths_list = []
        for file_item in cls.file_items_list:
            if file_item.file_type == ".pdf":
                pdf_paths_list.append(file_item.file_path)
        return pdf_paths_list

# ****************************************************************************************************

    def __init__(self, file_paht):
        self.file_path = file_paht
        self.file_name = FileItem.get_file_name(file_paht)
        self.file_type = FileItem.get_file_type(file_paht)
        self.size = FileItem.get_file_size(file_paht)

        #add to file_items_list
        FileItem.file_items_list.append(self)
    
    #change FileItem representation to file path
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.file_path}')"

    def getFormattedSize(self):
        size = self.size 
        power = 2**10
        n = 0
        power_labels = {0 : 'bytes', 1: 'KB', 2: 'MB', 3: 'GB', 
            4: 'TB', 5: 'PB', 6: 'EB', 7: 'ZB', 8: 'YB'}
        while size > power:
            size /= power
            n += 1
        return str("%.2f" % size) + " " + power_labels[n]

    def getFileName(self):
        return (self.file_name + self.file_type)

# ****************************************************************************************************
    # implement for each subclass of FileItem:

    def convertToPDF(self):
        FileItem.showSomethingWentWrong("cannot convert " + self.getFileName() + " to pdf",
            "convertToPDF Function not implemented in class " + type(self).__name__)

    def openFile(self):
        try:
            FileItem.open_file_by_path(self.file_path)
        except Exception as e:
            FileItem.showSomethingWentWrong("openning " + self.getFileName() + "failed!" , e)

    def getPreview(self, container)-> tk.Frame:
        pass

    def getControllers(self, container)-> tk.Frame:
        pass
# ****************************************************************************************************

    @classmethod
    def mergeFilesToPdf(cls, merged_path="merged_file.pdf"):
        pdf_paths_list = FileItem.getPdfFilesPaths()
        # if all the files of type pdf
        if (len(pdf_paths_list) == len(FileItem.file_items_list)):
            #Create an instance of PdfFileMerger() class
            merger = PdfFileMerger()

            #Iterate over the pdf paths list
            for pdf_file in pdf_paths_list:
                #Append PDF files
                merger.append(pdf_file)

            #Write out the merged PDF file
            merger.write(merged_path)
            merger.close()

# ****************************************************************************************************

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
