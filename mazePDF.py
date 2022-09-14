# mazePDF - Graphical user interface to work with pdf files
# by: Mohammad Heeb
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# import
import tkinter as tk
from tkinter import Button, Canvas, Label, filedialog as fd
from tkinter.messagebox import showerror, showinfo
from tkinter import ttk
from FileItem import FileItem, PDFItem, ImageItem


# ****************************************************************************************************
# show messages functions

# show Libs used, name, install command, url ???


# ****************************************************************************************************
# controllers functions
# try methods of FileItem and catch if something went wrong



def convertImageToPDF(image_item):
    try:
        save_file_path  =  fd.asksaveasfilename(
            title = "save image as pdf",
            initialdir = getLastDirectory(),
            initialfile = image_item.file_name + ".pdf",
            defaultextension=".pdf",
            filetypes = (("pdf file", "*.pdf"), ("All Files", "*.*")))
        if (save_file_path != ''):
            image_item.saveImageAsPDF(save_file_path)
            setLastDirectory(save_file_path)
    except Exception as e:
        showSomethingWentWrong("error converting " + image_item.file_name + " to pdf", e)

def saveImageAs(image_item):
    try:
        save_file_path  =  fd.asksaveasfilename(
            title = "save image as...",
            initialdir = getLastDirectory(),
            initialfile = image_item.getFileName(),
            defaultextension=image_item.file_type,
            filetypes = SUPPORTED_FILE_TYPES)
        if (save_file_path != ''):
            image_item.saveImageAs(save_file_path)
            setLastDirectory(save_file_path)
    except Exception as e:
        showSomethingWentWrong("error saving " + image_item.file_name, e)

def grayscaleImage(image_item):
    try:
        image_item.grayscaleImage()
    except Exception as e:
        showSomethingWentWrong("error grayscaling " + image_item.file_name, e)

def flipImageVertically(image_item):
    try:
        image_item.flipImageVertically()
    except Exception as e:
        showSomethingWentWrong("failed to flip " + image_item.file_name, e)

def flipImageHorizontally(image_item):
    try:
        image_item.flipImageHorizontally()
    except Exception as e:
        showSomethingWentWrong("failed to flip " + image_item.file_name, e)

# ****************************************************************************************************

# pack single file item frame
def packSingleFileItemFrame(container, file_item):
    createFileItemFrame(container, file_item
        ).pack(fill=tk.Y, expand=True, pady=50)

# ====================================================================================================


# pack custom file item controllers
def packFileItemControllers(container, file_item):
    file_type = file_item.file_type
    if file_type == ".pdf":
        # pack pdf controllers
        pass
    elif isImageType(file_type):
        packImageControllers(container, file_item)

    packAddFilesButton(container)

def packImageControllers(container, image_item):
    background_color = getBackgroundColor(display_mode)
    controllers_frame = tk.Frame(container, bg=background_color, bd=0)
    row_1 = tk.Frame(controllers_frame, bg=background_color, bd=0)
    row_2 = tk.Frame(controllers_frame, bg=background_color, bd=0)
    controllers_frame.pack(fill=tk.X, pady=3)
    row_1.pack(fill=tk.X)
    row_2.pack(fill=tk.X)

    # convert to pdf button
    packController(row_1, "Convert to PDF", lambda: convertImageToPDF(image_item))

    # save as button
    packController(row_1, "Save AS...", lambda: saveImageAs(image_item))

    # grayscale button
    packController(row_1, "Grayscale", lambda: grayscaleImage(image_item))

    # blur button
    packController(row_1, "Blur")

    # resize button
    packController(row_2, "Resize")

    # rotate button
    packController(row_2, "Rotate")

    # flip top-bottom button
    packController(row_2, "Vertical Flip", lambda: flipImageVertically(image_item))

    # flip left-right button
    packController(row_2, "Horizontal Flip", lambda: flipImageHorizontally(image_item))

# ====================================================================================================

# image item frame
def createImageItemFrame(container, image_item):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    image_frame = tk.Frame(container, bg=background_color, bd=0)
    
    # file icon
    Button(image_frame, 
        image=getFileIconAsset(image_item.file_type),
        bd=0,
        text="open image", 
        bg=background_color, 
        activebackground=background_color,
        fg=foreground_color, 
        activeforeground=foreground_color,
        command=lambda: openFile(image_item)
        ).grid(row=0, column=0, rowspan=3, sticky=tk.NS)

    # file name
    getStyleLabel(image_frame, "name: " + image_item.getFileName(), True
        ).grid(row=0, column=1, sticky=tk.SW)

    # image width
    getStyleLabel(image_frame, "width: " + str(image_item.image_width)
        ).grid(row=1, column=1, sticky=tk.SW)

    # image height
    getStyleLabel(image_frame, "height: " + str(image_item.image_height)
        ).grid(row=2, column=1, sticky=tk.NW)

    return image_frame

# ****************************************************************************************************
# popup windows

def openPopupWindow(title):
    popup_window = tk.Toplevel()
    popup_window.title(title)
    popup_window.config(width=300, height=200)
    # get focus automatically
    popup_window.focus()
    # modal window (disable user from using the main window while the popup window is visible)
    popup_window.grab_set()

# ****************************************************************************************************

# when mazePDF starts
def startMaze():
    updateDisplay()

# when mazePDF ends
def endMaze():
    # save stats ???
    print("Thank you for using mazePDF!")

# ====================================================================================================
startMaze()
#print(font.families())

# fixing the blur UI on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()

endMaze()