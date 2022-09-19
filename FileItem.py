import os
import pathlib
import tkinter as tk
from tkinter.messagebox import showerror
from PyPDF2 import PdfReader, PdfWriter,PdfFileMerger
from AppPreferences import AppPreferences

# App Preferences
app_style = AppPreferences()

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
        self.updateSize()
        
        #add to file_items_list
        FileItem.file_items_list.append(self)
    
    def updateSize(self):
        self.size = FileItem.get_file_size(self.file_path)

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
        frame = FileItemFrame(self, container)
        frame.packDefaultPreview()
        return frame

    def getControllers(self, container, window)-> tk.Frame:
        controllers = FileItemControllers(self, container, window)
        controllers.packDefaultControllers()
        return controllers
# ****************************************************************************************************
    
    # mazePDF metadata for new created pdf files
    @classmethod
    def newCreatedPDF(cls, new_pdf_path):
        reader = PdfReader(new_pdf_path)
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.add_metadata(reader.metadata)
        # mazePDF metadata
        FileItem.mazePDFMetadata(writer)

        with open(new_pdf_path, "wb") as f:
            writer.write(f)

    @classmethod
    def mazePDFMetadata(cls, obj):
        # mazePDF metadata
        obj.add_metadata({"/Producer" : "mazePDF", "/Creator" : "mazePDF"})

    @classmethod
    def mergeFilesToPdf(cls, merged_path="merged_file.pdf"):
        # Create an instance of PdfFileMerger() class
        merger = PdfFileMerger()

        # Iterate over the pdf paths list
        for file_item in FileItem.file_items_list:
            #Append file_item as pdf file
            merger.append(file_item.convertToPDF())
        
        # mazePDF metadata
        FileItem.mazePDFMetadata(merger)

        # Write out the merged PDF file
        output = open(merged_path, "wb")
        merger.write(output)
        merger.close()
        output.close()

    @classmethod
    def mergePDFSFilesToPdf(cls, merged_path="merged_file.pdf"):
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

# File Item Preview:
class FileItemFrame(tk.Frame):

    def __init__(self, file_item:  FileItem, container):
        super().__init__(container)
        self.container = container
        self.file_item = file_item
        app_style.setFrameColor(self)
    
    def packDefaultPreview(self):
        self.destroy()
        super().__init__(self.container)
        app_style.setFrameColor(self)

        # open file button (file icon)
        self.open_file_button = self.getOpenFileButton()
        self.open_file_button.grid(row=0, column=0, rowspan=3, sticky=tk.NS)

        # file name
        self.file_name_label = self.getFileNameLabel()
        self.file_name_label.grid(row=0, column=1, sticky=tk.SW)

        # file size
        self.file_size_label = self.getFileSizeLabel()
        self.file_size_label.grid(row=1, column=1, sticky=tk.SW)

        # file type
        self.file_type_label = self.getFileTypeLabel()
        self.file_type_label.grid(row=2, column=1, sticky=tk.NW)

    def getOpenFileButton(self):
        open_file_button = app_style.getItemControlButton(self, 
            "open file",
            app_style.getFileIconAssetKey(self.file_item.file_type), 
            self.file_item.openFile)
        return open_file_button
    
    def getFileNameLabel(self):
        return app_style.getStyleLabel(self, "name: " + self.file_item.getFileName(), True)

    def getFileTypeLabel(self):
        return app_style.getStyleLabel(self, "file type: " + self.file_item.file_type)

    def getFileSizeLabel(self):
        return app_style.getStyleLabel(self, "size: " + self.file_item.getFormattedSize())

# ****************************************************************************************************

# File Item Controllers
class FileItemControllers(tk.Frame):
    def __init__(self, file_item: FileItem, container, window):
        super().__init__(container)
        self.window = window
        self.container = container
        self.file_item = file_item
        app_style.setFrameColor(self)
    
    def packDefaultControllers(self):
        self.default_label = app_style.getStyleLabel(self, 
            "no controllers available for " + self.file_item.getFileName())
        self.default_label.pack(fill=tk.X, side=tk.TOP, anchor=tk.CENTER, padx=5, pady=10)

    def packRows(self, rows_num):
        rows_list = []
        for i in range(rows_num):
            rows_list.append(tk.Frame(self))
            app_style.setFrameColor(rows_list[i])
            rows_list[i].pack(fill=tk.X, side=tk.TOP)
        return rows_list
    
    def packColumns(self, columns_num):
        columns_list = []
        for i in range(columns_num):
            columns_list.append(tk.Frame(self))
            app_style.setFrameColor(columns_list[i])
            columns_list[i].pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        return columns_list