import imp
import os
import pathlib
from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger

class FileItem:
    # list to store the FileItems created.
    file_items_list = []

    @staticmethod
    def is_valid_file_path(path):
        return (os.path.isfile(path))
    
    @staticmethod
    def get_file_type(path):
        return (pathlib.Path(path).suffix).lower()
    
    def __init__(self, file_paht):
        self.file_path = file_paht
        self.file_name = ""
        self.file_type = FileItem.get_file_type(file_paht)
        self.size = 0

        #add to file_items_list
        FileItem.file_items_list.append(self)
    
    #change FileItem representation to file path
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.file_path}')"

    @classmethod
    def getPdfFilesPaths(cls):
        pdf_paths_list = []
        for file_item in cls.file_items_list:
            if file_item.file_type == ".pdf":
                pdf_paths_list.append(file_item.file_path)
        return pdf_paths_list

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
            merger.write("merged_file.pdf")
            merger.close()

class PDFItem(FileItem):
    def __init__(self, file_paht):
        # call super function
        super().__init__(file_paht)
        
        self.isEncrypted = PdfReader(self.file_path).is_encrypted
        self.user_password = None
        self.owner_password = None