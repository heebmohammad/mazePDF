from tkinter.messagebox import showerror
from FileItem import FileItem, ImageItem
from PDFItem import PDFItem

class FileItemFactory:
    # note: the factory does not maintain any of the instances it creates.

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

    @staticmethod
    def isSupportedFileType(file_type):
            return (any([((("*" + file_type) in tup) for tup in row) for row in FileItemFactory.SUPPORTED_FILE_TYPES]))

    @staticmethod
    def isImageType(file_type):
        return file_type in (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")

# ****************************************************************************************************
    # static methods

    # create and return FileItem object according to file type
    @staticmethod
    def createFileItem(file_path, file_type):
        try:
            if (file_type == ".pdf"):
                return PDFItem(file_path)
            elif (FileItemFactory.isImageType(file_type)):
                return ImageItem(file_path)
            else:
                return FileItem(file_path)
        except Exception as e:
            FileItem.showSomethingWentWrong("Failed creating file item of \"" + file_path + "\"", e)

    # add filenames (list of files paths) to mazePDF app
    @staticmethod
    def addFileItems(filenames):
        # list of unsupported files and their types
        unsupported_files = []
        # list of invalid paths
        invalid_paths = []

        for filename in filenames:
            if (FileItem.is_valid_file_path(filename)):
                file_type = FileItem.get_file_type(filename)
                if (FileItemFactory.isSupportedFileType(file_type)):
                    #create file Item
                    FileItemFactory.createFileItem(filename, file_type)
                else:
                    unsupported_files.append((filename, file_type))
            else:
                invalid_paths.append(filename)
        showErrorSelectingFiles(unsupported_files, invalid_paths)

# ****************************************************************************************************

# Show Error Selecting Files Message
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