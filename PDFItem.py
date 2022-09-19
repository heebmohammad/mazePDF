# mazePDF Project 
# - PDFItem.py by Mohammad Heeb
# - add support to: (.pdf) file types
# - python libraries dependency: PyPDF2
# - Item Preview: X
# - Item Controllers: X
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import tkinter as tk
from tkinter.messagebox import askyesno, showinfo
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DictionaryObject
from AppPreferences import AppPreferences
from FileItem import FileItem, FileItemControllers, FileItemFrame

# App Preferences
app_style = AppPreferences()

class PDFItem(FileItem):
    def __init__(self, file_paht):
        # call super function
        super().__init__(file_paht)
        self.updatePDFProperties()
        self.show_password = False
        self.user_password = None
        self.owner_password = None
    
    def updatePDFProperties(self):
        reader = PdfReader(self.file_path)
        self.meta_data = None
        self.num_pages = 0
        self.is_encrypted = reader.is_encrypted
        if not(self.is_encrypted):
            self.num_pages = len(reader.pages)
            self.meta_data = reader.metadata
    
    def convertToPDF(self):
        return self.file_path
    
    def getPreview(self, container)-> tk.Frame:
        return PDFItemFrame(self, container)
    
    def getControllers(self, container, window)-> tk.Frame:
        return PDFItemControllers(self, container, window)

    def getFormmatedPagesNumber(self):
        if self.is_encrypted and self.user_password == None:
            return "cannot view pages number"
        elif self.is_encrypted and self.user_password != None:
            # decrypt and get pages number
            return "trying to get pages number"
        else:
            return "pages number: " + str(self.num_pages) + " pages"
    
    def getFormmatedMetadata(self):
        SPACE = '\n\n'
        if (self.is_encrypted and self.user_password == None):
            return "cannot view metadata"
        elif self.is_encrypted and self.user_password != None:
            # decrypt and get metadata
            return "trying to get metadata"
        else:
            metadata_str = ""
            if self.meta_data.title != None:
                metadata_str += "Title: " + self.meta_data.title + SPACE
            if self.meta_data.subject != None:
                metadata_str += "Subject: " + self.meta_data.subject + SPACE
            if self.meta_data.author != None:
                metadata_str += "Author: " + self.meta_data.author + SPACE
            if self.meta_data.creator != None:
                metadata_str += "Creator: " + self.meta_data.creator + SPACE
            if self.meta_data.producer != None:
                metadata_str += "Producer: " + self.meta_data.producer + SPACE
            if metadata_str == "":
                metadata_str = "There is no metadata available for \"" + self.getFileName() + "\""
            return metadata_str

# ====================================================================================================
    def removeMetadata(self):
        reader = PdfReader(self.file_path)
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)

        # change info object in PyPDF2.PdfWriter.__init__ to an empty dictionary object
        writer._info = writer._add_object(DictionaryObject())

        with open(self.file_path, "wb") as f:
            writer.write(f)
        
        self.updateSize()
        self.updatePDFProperties()

    def launchPrintWindow(self):
        reader = PdfReader(self.file_path)
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.add_js("this.print(" + "{" + "bUI:true,bSilent:false,bShrinkToFit:true});")

        writer.add_metadata(reader.metadata)
        # mazePDF metadata
        FileItem.mazePDFMetadata(writer)
        with open(self.file_path, "wb") as f:
            writer.write(f)
        
        self.updateSize()
        self.updatePDFProperties()

    def rewritePDF(self):
        reader = PdfReader(self.file_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        
        writer.add_metadata(reader.metadata)
        # mazePDF metadata
        FileItem.mazePDFMetadata(writer)
        with open(self.file_path, "wb") as f:
            writer.write(f)
        
        self.updateSize()
        self.updatePDFProperties()
    
    def removeImages(self):
        reader = PdfReader(self.file_path)
        writer = PdfWriter()
        writer.append_pages_from_reader(reader)

        writer.remove_images(True)

        writer.add_metadata(reader.metadata)
        # mazePDF metadata
        FileItem.mazePDFMetadata(writer)
        with open(self.file_path, "wb") as f:
            writer.write(f)
        
        self.updateSize()
        self.updatePDFProperties()
    
    def compressPDF(self):
        reader = PdfReader(self.file_path)
        writer = PdfWriter()

        for page in reader.pages:
            page.compress_content_streams()  # This is CPU intensive!
            writer.add_page(page)
        
        writer.add_metadata(reader.metadata)
        # mazePDF metadata
        FileItem.mazePDFMetadata(writer)
        with open(self.file_path, "wb") as f:
            writer.write(f)
        
        self.updateSize()
        self.updatePDFProperties()

# ****************************************************************************************************

# PDF Item Preview:
class PDFItemFrame(FileItemFrame):

    def __init__(self, pdf_item: PDFItem, container):
        super().__init__(pdf_item, container)
        self.pdf_item = pdf_item
        self.packPDFPreview()
    
    def packPDFPreview(self):
        # open file button (file icon)
        self.open_file_button = self.getOpenFileButton()
        self.open_file_button.grid(row=0, column=0, rowspan=3, sticky=tk.NS)

        # file name
        self.file_name_label = self.getFileNameLabel()
        self.file_name_label.grid(row=0, column=1, sticky=tk.SW)

        # file size
        self.file_size_label = self.getFileSizeLabel()
        self.file_size_label.grid(row=1, column=1, sticky=tk.SW)

        # file number of pages
        self.num_pages_label = app_style.getStyleLabel(self, self.pdf_item.getFormmatedPagesNumber())
        self.num_pages_label.grid(row=2, column=1, sticky=tk.NW)

        # is encrypted file
        self.is_encrypted_label = app_style.getIsEncryptedLabel(self, self.pdf_item.is_encrypted)
        self.is_encrypted_label.grid(row=3, column=0, sticky=tk.EW)

# ****************************************************************************************************

# PDF Item Controllers
class PDFItemControllers(FileItemControllers):
    def __init__(self, pdf_item: PDFItem, container, window):
        super().__init__(pdf_item, container, window)
        self.pdf_item = pdf_item
        self.packPDFControllers()

    def packPDFControllers(self):
        
        side = tk.LEFT
        expand = True

        self.rows = self.packRows(2)
        # quick compress button
        self.quick_compress_button = app_style.getStyledController(
            self.rows[0], "Quick Compress", self.quickCompressPDF)
        self.quick_compress_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # hard compress button
        self.hard_compress_button = app_style.getStyledController(
            self.rows[0], "Hard Compress", self.hardCompressPDF)
        self.hard_compress_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # remove images button
        self.remove_images_button = app_style.getStyledController(
            self.rows[0], "Remove Images (beta)", self.removeImageFromPDF)
        self.remove_images_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # show metadata button
        self.show_metadata_button = app_style.getStyledController(
            self.rows[1], "Show Metadata", self.showPDFMetadata)
        self.show_metadata_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # clear metadata button
        self.clear_metadata_button = app_style.getStyledController(
            self.rows[1], "Clear Metadata", self.clearPDFMetadata)
        self.clear_metadata_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # ready to print button
        self.ready_to_print_button = app_style.getStyledController(
            self.rows[1], "Ready to Print", self.readyToPrintPDF)
        self.ready_to_print_button.pack(fill=tk.X, side=tk.LEFT, expand=True)
    #....................................................................................................#

# ====================================================================================================
    def showPDFMetadata(self):
        try:
            showinfo(title=self.pdf_item.getFileName() + " Metadata",
                message=self.pdf_item.getFormmatedMetadata())
        except Exception as e:
            FileItem.showSomethingWentWrong("error viewing " + self.pdf_item.getFileName() + " metadata", e)
    
    def clearPDFMetadata(self):
        try:
            answer = askyesno(title="Remove Metadata from PDF", 
                message="Are you sure that you want to remove metadata from \"" + self.pdf_item.getFileName() + "\"?")            
            if answer:
                self.pdf_item.removeMetadata()
                self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error removing metadata from " + self.pdf_item.getFileName(), e)

    def readyToPrintPDF(self):
        try:
            answer = askyesno(title="Ready to Print PDF", 
                message="Are you sure that you want to launch the print window when \"" + self.pdf_item.getFileName() + "\" is opened?"
                +"\nNote: javascript code injection.")
            if answer:
                self.pdf_item.launchPrintWindow()
                self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error preparing " + self.pdf_item.getFileName() + " to print!", e)
    
    def removeImageFromPDF(self):
        try:
            answer = askyesno(title="Remove Images from PDF", 
                message="Are you sure that you want to remove images from \"" + self.pdf_item.getFileName() + "\"?"
                +"\nbe CAUTIOUS: removes much more than merely images!")
            if answer:
                self.pdf_item.removeImages()
                self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error removing images from " + self.pdf_item.getFileName(), e)

    def quickCompressPDF(self):
        try:
            answer = askyesno(title="PDF Quick Compress", 
                message="compress \"" + self.pdf_item.getFileName() + "\" by rewriting it, to replace duplication with referencing?")
            if answer:
                self.pdf_item.rewritePDF()
                self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("Compression Error with " + self.pdf_item.getFileName(), e)
    
    def hardCompressPDF(self):
        try:
            answer = askyesno(title="PDF Hard Compress", 
                message="apply lossless compression to \"" + self.pdf_item.getFileName() + "\"?"
                + "\nNote: might be CPU intensive!")
            if answer:
                self.pdf_item.compressPDF()
                self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("Compression Error with " + self.pdf_item.getFileName(), e)