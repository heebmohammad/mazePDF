import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror
from FileItem import FileItem, PDFItem, ImageItem

# file types supported by mazePDF
SUPPORTED_FILE_TYPES = (
    ("pdf files", ("*.pdf", "*.PDF")),
    ("png files", ("*.png", "*.PNG")),
    ("jpeg files", ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG")),
    ("bmp files", ("*.bmp", "*.BMP")),
    ("tiff files", ("*.tiff", "*.TIFF")),
    ("gif files", ("*.gif", "*.GIF")),
    ("All Files", ("*.*"))
)

def isSupportedFileType(file_type):
        return (any([((("*" + file_type) in tup) for tup in row) for row in SUPPORTED_FILE_TYPES]))
    
def isImageType(file_type):
    return file_type in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")

# ****************************************************************************************************

class BrowseFilesButton(tk.Button):
    def __init__(self, container, window, full_display=False):
        super().__init__(container, command=self.selectFiles)
        self.window = window
        if full_display:
            self.packFullBrowseFilesButton()
        else:
            self.packAddFilesButton()

    # pack main browse files button
    def packFullBrowseFilesButton(self):
        browse_files_image = self.window.style.getAsset("white-browse-files")
        self.config(text="Browse...",
            bd=0,
            font = ("Times new roman", 50),
            image=browse_files_image)
        
        self.window.style.setButtonColor(self, True)
        self.pack(fill=tk. BOTH, expand=True)

    # wide add files button
    def packAddFilesButton(self):
        self.config(text="Add Files")
        self.window.style.setControllerStyle(self)
        self.pack(fill=tk.X, expand=True)
    
# ====================================================================================================

    @staticmethod
    def addFileItems(filenames):
        # list of unsupported files and their types
        unsupported_files = []
        # list of invalid paths
        invalid_paths = []

        for filename in filenames:
            if (FileItem.is_valid_file_path(filename)):
                file_type = FileItem.get_file_type(filename)
                if (isSupportedFileType(file_type)):
                    #create file Item
                    BrowseFilesButton.createFileItem(filename, file_type)
                else:
                    unsupported_files.append((filename, file_type))
            else:
                invalid_paths.append(filename)
        showErrorSelectingFiles(unsupported_files, invalid_paths)

    def selectFiles(self):
        global last_directory
        filenames = fd.askopenfilenames(
            title = "select files...",
            initialdir=self.window.style.getLastDirectory(),
            filetypes=SUPPORTED_FILE_TYPES)

        if len(filenames) != 0:
            self.window.style.setLastDirectory(filenames[0])
        BrowseFilesButton.addFileItems(filenames)

        self.window.updateDisplay()

    # create FileItem objects according to file type
    @staticmethod
    def createFileItem(file_path, file_type):
        try:
            if (file_type == ".pdf"):
                PDFItem(file_path)
            elif (isImageType(file_type)):
                ImageItem(file_path)
            else:
                FileItem(file_path)
        except Exception as e:
            FileItem.showSomethingWentWrong("Failed creating file item of \"" + file_path + "\"", e)

# ****************************************************************************************************

# Error Selecting Files Message
def showErrorSelectingFiles(unsupported_files, invalid_paths):
    if (not(unsupported_files) and not(invalid_paths)):
        return
    
    # sort according to file type
    unsupported_files.sort(key=lambda x: x[1])
    unsupported_str = ""
    for tup in unsupported_files:
        unsupported_str += "the file: \"" + tup[0] + "\" of type (" + tup[1] + ") not supported yet.\n"
    
    invalid_str = ""
    for path in invalid_paths:
        invalid_str += "\"" + path + "\" is an invalid file path."
    
    error_message = ""
    show_error = False

    if len(unsupported_files) !=0:
        show_error = True
        error_message += "Unsupported File Types: \n" + unsupported_str + "\n"
    
    if len(invalid_paths) !=0:
        show_error = True
        error_message += "Invalid Paths: \n" + invalid_str + "\n"
    
    if show_error:
        showerror("Error Selecting Files", error_message)