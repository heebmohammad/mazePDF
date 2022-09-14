# mazePDF Project 
# - PDFItem.py by Mohammad Heeb
# - add support to: (.pdf) file types
# - python libraries dependency: PyPDF2
# - Item Preview: X
# - Item Controllers: X
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tkinter as tk
from PyPDF2 import PdfReader
from AppPreferences import AppPreferences
from FileItem import FileItem

# App Preferences
app_style = AppPreferences()

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
    
    def getPreview(self, container)-> tk.Frame:
        return PDFItemFrame(self, container)

    def getFormmatedPagesNumber(self):
        if self.is_encrypted and self.user_password == None:
            return "cannot view pages number"
        elif self.is_encrypted and self.user_password != None:
            # decrypt and get pages number
            return "trying to get pages number"
        else:
            return "pages number: " + str(self.num_pages) + " pages"

# ****************************************************************************************************

# PDF Item Preview:
class PDFItemFrame(tk.Frame):

    def __init__(self, pdf_item: PDFItem, container):
        super().__init__(container)
        self.pdf_item = pdf_item

        self.config(bd=0)
        app_style.setFrameColor(self)
        
        # open file button (file icon)
        self.open_file_button = app_style.getItemControlButton(self, 
            "open pdf",
            app_style.getFileIconAssetKey(self.pdf_item.file_type), 
            self.pdf_item.openFile)
        self.open_file_button.grid(row=0, column=0, rowspan=3, sticky=tk.NS)

        # file name
        self.file_name_label = app_style.getStyleLabel(self, "name: " + self.pdf_item.getFileName(), True)
        self.file_name_label.grid(row=0, column=1, sticky=tk.SW)

        # file size
        self.file_size_label = app_style.getStyleLabel(self, "size: " + self.pdf_item.getFormattedSize())
        self.file_size_label.grid(row=1, column=1, sticky=tk.SW)

        # file number of pages
        self.num_pages_label = app_style.getStyleLabel(self, self.pdf_item.getFormmatedPagesNumber())
        self.num_pages_label.grid(row=2, column=1, sticky=tk.NW)

        # is encrypted file
        self.is_encrypted_label = app_style.getIsEncryptedLabel(self, self.pdf_item.is_encrypted)
        self.is_encrypted_label.grid(row=3, column=0, sticky=tk.EW)
