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

# merge all files in file_items_list to pdf file
def mergeFiles():
    #ask for save path
    try:
        save_file_path  =  fd.asksaveasfilename(
            title = "save merged file as...",
            initialdir = getLastDirectory(),
            initialfile = "merged_file.pdf",
            defaultextension=".pdf",
            filetypes = (("pdf file", "*.pdf"), ("All Files", "*.*")))
        if (save_file_path != ''):
            FileItem.mergeFilesToPdf(save_file_path)
            setLastDirectory(save_file_path)
    except Exception as e:
        showSomethingWentWrong("merge files failed!", e)

def openFile(file_item):
    try:
        # if file_type == ".pdf": open in tkinter ???
        file_item.openFile()
    except Exception as e:
        file_name = FileItem.getFileName(file_item)
        showSomethingWentWrong("openning " + file_name + "failed!" , e)

def sortItemsDisplay():
    try:
        FileItem.sortFileItemsList()
        updateDisplay()
    except Exception as e:
        showSomethingWentWrong("failed to sort." , e)

def reverseItemsDisplay():
    try:
        FileItem.reverseFileItemsList()
        updateDisplay()
    except Exception as e:
        showSomethingWentWrong("failed to reverse." , e)

def deleteFileItem(file_item):
    try:
        FileItem.deleteFileItems(file_item)
        updateDisplay()
    except Exception as e:
        file_name = FileItem.getFileName(file_item)
        showSomethingWentWrong("failed to delete " + file_name , e)

def upFileItem(file_item):
    try:
        FileItem.forewardFileItems(file_item)
        updateDisplay()
    except Exception as e:
        showSomethingWentWrong("error up!", e)

def downFileItem(file_item):
    try:
        FileItem.backwardFileItems(file_item)
        updateDisplay()
    except Exception as e:
        showSomethingWentWrong("error down!", e)

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
# pack displayes



# pack canvas and scrollbar, and return the srollable frame
def getScrollableContainer(container):
    # create frame for canvas and scrollbar
    both_frame = tk.Frame(container)
    both_frame.pack(fill=tk.BOTH, expand=True)

    # create a canvas
    my_canvas = Canvas(both_frame, highlightthickness=0)
    setFrameColor(my_canvas)

    # create a scrollbar
    my_scrollbar = ttk.Scrollbar(both_frame, orient=tk.VERTICAL, command=my_canvas.yview)

    # pack canvas and scrollbar
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    # create the scrollable frame
    scrollable_frame = tk.Frame(my_canvas)
    setFrameColor(scrollable_frame)

    # pack the scrollable frame to my_canvas
    #scrollable_frame.pack(fill=tk.BOTH, expand=True)

    # add the scrollable freame to a window in the canvas
    my_canvas.create_window((0,0), window=scrollable_frame, anchor=tk.CENTER)

    # return the scrollable frame
    return scrollable_frame

# ====================================================================================================





# pack single file item frame
def packSingleFileItemFrame(container, file_item):
    createFileItemFrame(container, file_item
        ).pack(fill=tk.Y, expand=True, pady=50)

# ====================================================================================================

# pack controller with style
def packController(container, text, func=selectFiles):
    button = tk.Button(container, text=text, command=func)
    setControllerStyle(button)
    button.pack(fill=tk.X, side=tk.LEFT, expand=True)

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

# convert index to row, column
def getRowAndColumn(index):
    columns_num = 1
    return int(index / columns_num), index % columns_num

def getControledContainer(container, file_item, index):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    controled_container = tk.Frame(container, bg=background_color, bd=0)

    row, column = getRowAndColumn(index)
    # pady to determine the space between two frames
    # padx to determine the space between the controled_container and the edge
    controled_container.grid(row=row, column=column, pady=5, padx=5, sticky=tk.EW)

    # item up button
    Button(controled_container, 
        image=getAsset("item-frame-up"),
        bd=0,
        text="up", 
        bg=background_color, 
        activebackground=background_color,
        fg=foreground_color, 
        activeforeground=foreground_color,
        command=lambda: upFileItem(file_item)
        ).grid(row=0, column=0, sticky=tk.S)

    # item down button
    Button(controled_container, 
        image=getAsset("item-frame-down"),
        bd=0,
        text="down", 
        bg=background_color, 
        activebackground=background_color,
        fg=foreground_color, 
        activeforeground=foreground_color,
        command=lambda: downFileItem(file_item)
        ).grid(row=1, column=0, sticky=tk.N)

    # item delete button
    Button(controled_container, 
        image=getAsset("delete-file"),
        bd=0,
        text="delete", 
        bg=background_color, 
        activebackground=background_color,
        fg=foreground_color, 
        activeforeground=foreground_color,
        command=lambda: deleteFileItem(file_item)
        ).grid(row=2, column=0, sticky=tk.EW)

    return controled_container

def gridFileItemsList(container):
    i = 0
    for file_item in FileItem.file_items_list:
        controled_container = getControledContainer(container, file_item, i)
        frame = createFileItemFrame(controled_container, file_item)
        # padx to determine the space between the frame controllers and the FileItem frame
        frame.grid(row=0, column=1, rowspan=3, sticky=tk.NS, padx=5) 
        i += 1       
        
def createFileItemFrame(container, file_item: FileItem):
    if file_item.file_type == ".pdf":
        return createPDFItemFrame(container, file_item)
    elif isImageType(file_item.file_type):
        return createImageItemFrame(container, file_item)
    else:
        pass

def getStyleLabel(container, label_text, is_bold=False):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    label_font = ("Century Gothic", 12)
    if is_bold:
        label_font = ("Century Gothic", 12, "bold")
    return Label(container,
        text=label_text,
        background=background_color,
        foreground=foreground_color,
        font=label_font)

# pdf item frame
def createPDFItemFrame(container, pdf_item: PDFItem):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    pdf_frame = tk.Frame(container, bg=background_color, bd=0)
    
    # file icon
    Button(pdf_frame, 
        image=getFileIconAsset(pdf_item.file_type),
        bd=0,
        text="open pdf", 
        bg=background_color, 
        activebackground=background_color,
        fg=foreground_color, 
        activeforeground=foreground_color,
        command=lambda: openFile(pdf_item)
        ).grid(row=0, column=0, rowspan=3, sticky=tk.NS)

    # file name
    getStyleLabel(pdf_frame, "name: " + pdf_item.getFileName(), True
        ).grid(row=0, column=1, columnspan=2, sticky=tk.SW)

    # file size
    getStyleLabel(pdf_frame, "size: " + pdf_item.getFormattedSize()
        ).grid(row=1, column=1, columnspan=2, sticky=tk.SW)

    # file number of pages
    getStyleLabel(pdf_frame, PDFItem.getFormmatedPagesNumber(pdf_item)
        ).grid(row=2, column=1, columnspan=2, sticky=tk.NW)

    # is encrypted file
    getIsEncryptedLabel(pdf_frame, pdf_item.is_encrypted
        ).grid(row=3, column=0, sticky=tk.EW)

    return pdf_frame

def getIsEncryptedLabel(container, is_encrypted):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    label_font = ("Century Gothic", 10)
    if is_encrypted:
        lock_image = getAsset("lock-lock")
        return Label(container,
            text=" Encrypted",
            underline=1,
            background=background_color,
            foreground=foreground_color,
            font=label_font,
            image= lock_image,
            compound=tk.LEFT)
    else:
        lock_image = getAsset("lock-unlock")
        return Label(container,
            text=" Decrypted",
            underline=1,
            background=background_color,
            foreground=foreground_color,
            font=label_font,
            image= lock_image,
            compound=tk.LEFT)

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

# ====================================================================================================



def packMultipleFilesControllers(container):
    background_color = getBackgroundColor(display_mode)
    controllers_frame = tk.Frame(container, bg=background_color, bd=0)
    controllers_frame.pack(fill=tk.X, pady=3)

    # merge files button
    merge_files_button = tk.Button(controllers_frame, 
        text="Merge Files",
        command=mergeFiles)
    setControllerStyle(merge_files_button)
    merge_files_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # merge pages button
    merge_pages_button = tk.Button(controllers_frame, 
        text="Merge Pages",
        command=mergeFiles,
        state=tk.DISABLED)
    setControllerStyle(merge_pages_button)
    merge_pages_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # sort files button
    sort_button = tk.Button(controllers_frame, 
        text="Sort",
        command=sortItemsDisplay)
    setControllerStyle(sort_button)
    sort_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # reverse files button
    reverse_button = tk.Button(controllers_frame, 
        text="Reverse",
        command=reverseItemsDisplay)
    setControllerStyle(reverse_button)
    reverse_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    packAddFilesButton(container)

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