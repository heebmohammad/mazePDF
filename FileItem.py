import os
import pathlib
from PyPDF2 import PdfReader, PdfWriter, PdfFileMerger
from PIL import Image

class FileItem:
    # list to store the FileItems created.
    file_items_list = []

    @staticmethod
    def getDirectoryPath(filenames):
        if len(filenames) == 0:
            return ''
        else:
            return os.path.dirname(filenames[0])

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

    @staticmethod
    def open_file(path):
        os.startfile(path)

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

    def openFile(self):
        FileItem.open_file(self.file_path)

    def getFileName(self):
        return (self.file_name + self.file_type)

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

class PDFItem(FileItem):
    def __init__(self, file_paht):
        # call super function
        super().__init__(file_paht)
        
        reader = PdfReader(self.file_path)
        self.num_pages = 0
        self.is_encrypted = reader.is_encrypted
        if not(self.is_encrypted):
            self.num_pages = len(reader.pages)
        self.show_password = False
        self.user_password = None
        self.owner_password = None

    @classmethod
    def getFormmatedPagesNumber(cls, pdf_item):
        if pdf_item.is_encrypted and pdf_item.user_password == None:
            return "cannot view pages number"
        elif pdf_item.is_encrypted and pdf_item.user_password != None:
            # decrypt and get pages number
            return "trying to get pages number"
        else:
            return "pages number: " + str(pdf_item.num_pages) + " pages"

# ****************************************************************************************************

class ImageItem(FileItem):
    def __init__(self, file_paht):
        # call super function
        super().__init__(file_paht)
        
        #Load the image
        self.img = Image.open(self.file_path)
        self.image_format = self.img.format
        self.image_mode = self.img.mode
        self.image_width = self.img.size[0]
        self.image_height = self.img.size[1]

    def openFile(self):
        self.img.show()