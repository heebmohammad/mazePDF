# mazePDF - Graphical user interface to work with pdf files
# by: Mohammad Heeb
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# import
import tkinter as tk
from tkinter import Button, Canvas, Label, filedialog as fd
from tkinter.messagebox import showerror, showinfo
from tkinter import CENTER, TclError, ttk, font
from FileItem import FileItem, PDFItem

# ****************************************************************************************************
# initial 

# light or dark display mode
display_mode = "DARK"

ASSETS_DIR_PATH = './assets/'
# dictionary of assets
assets_dict = {"main-logo" : {"path": 'images/maze_pdf_logo.png'},
            "white-browse-files" : {"path": 'images/Folder-Open-icon.png'},
            "pdf-file-icon" : {"path": 'soft_icons/document_icons/Adobe-PDF-Document-icon.png'},
            "any-file-icon" : {"path": 'soft_icons/document_icons/Document-icon.png'},
            "png-file-icon" : {"path": 'soft_icons/document_icons/Image-PNG-icon.png'},
            "item-frame-up" : {"path": 'soft_icons/button_icons/Button-Upload-icon.png'},
            "item-frame-down" : {"path": 'soft_icons/button_icons/Button-Download-icon.png'},
            "delete-file" : {"path": 'soft_icons/button_icons/Button-Delete-icon.png'},
            "add-file-gray" : {"path": 'soft_icons/button_icons/Button-Blank-Gray-icon.png'},
            "lock-lock" : {"path": 'soft_icons/state_icons/Lock-Lock-icon.png'},
            "lock-unlock" : {"path": 'soft_icons/state_icons/Lock-Unlock-icon.png'}
            }

def initialAssets():
    for key, image_dict in assets_dict.items():
        try:
            image_dict["src"] = tk.PhotoImage(file= ASSETS_DIR_PATH + image_dict.get("path"))
        except TclError as e:
            # the tcl equivalent to None is ""
            image_dict["src"] = ""

def getAsset(key_asset):
    image_dict = assets_dict.get(key_asset)
    if image_dict == None:
        return ""
    else:
        return image_dict.get("src", "")

# initial stats and settings ???
# initial language dictionary ???

SUPPORTED_FILE_TYPES = (
    ("pdf files", "*.pdf"),
    ("pdf files", "*.PDF"),
    ("png files", "*.png"),
    ("All Files", "*.*")
)

def isSupportedFileType(file_type):
    return (any([("*" + file_type) in tup for tup in SUPPORTED_FILE_TYPES]))

# last opened directory
last_directory = '/'

def getLastDirectory():
    global last_directory
    return last_directory

def setLastDirectory(new_dir_path='/'):
    global last_directory
    if not(new_dir_path == ''):
        last_directory = new_dir_path

# ****************************************************************************************************
# show messages functions

# show Libs used, name, install command, url ???

def showProgramInfo():
    showinfo(title="about mazePDF", message="M.HEEB!")

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

def showSomethingWentWrong(message, exception):
    showerror("something went wrong", 
        message + "\n\nDetails:\n" + str(exception))

# ****************************************************************************************************
# controlers functions
# try methods of FileItem and catch if something went wrong

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
                createFileItem(filename, file_type)
            else:
                unsupported_files.append((filename, file_type))
        else:
            invalid_paths.append(filename)
    showErrorSelectingFiles(unsupported_files, invalid_paths)

def selectFiles():
    global last_directory
    filenames = fd.askopenfilenames(
        title = "select files...",
        initialdir=getLastDirectory(),
        filetypes=SUPPORTED_FILE_TYPES)
    setLastDirectory(FileItem.getDirectoryPath(filenames))
    addFileItems(filenames)

    updateDisplay()

# create FileItem objects according to file type
def createFileItem(file_path, file_type):
    try:
        if (file_type == ".pdf"):
            PDFItem(file_path)
        else:
            FileItem(file_path)
    except Exception as e:
        showSomethingWentWrong("Failed creating file item of \"" + file_path + "\"", e)

# merge all files in file_items_list to pdf file
def mergeFiles():
    #ask for save path
    try:
        save_file_path  =  fd.asksaveasfilename(
            title = "save merged file as...",
            initialdir = getLastDirectory(),
            initialfile = "merged_file.pdf",
            defaultextension=".txt",
            filetypes = (("pdf file", "*.pdf"), ("All Files", "*.*")))
        FileItem.mergeFilesToPdf(save_file_path)
    except Exception as e:
        showSomethingWentWrong("merge files failed!", e)

def openFile(file_item):
    try:
        # if file_type == ".pdf": open in tkinter ???
        FileItem.open_file(file_item.file_path)
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

# ****************************************************************************************************
# style functions

def getAnalogousColor(color):
    if (color == DEFAULT_GREEN):
        return "#3E8E41"
    else:
        return "#000000" #????

def getBackgroundColor(mode):
    if mode == "DARK":
        return "#000000"
    else:
        return "#FFFFFF"

def getForegroundColor(mode):
    if mode == "DARK":
        return "#FFFFFF"
    else:
        return "#000000"

DEFAULT_GREEN = "#4CAF50"
DEFAULT_RED = "#F40F02"
DEFAULT_BLACK = "#000000"
def getThemeColor(mode=""):
    # check if saved theme exist
    if False:
        pass
    elif mode == "":
        return DEFAULT_GREEN
    elif mode == "DARK":
        return DEFAULT_BLACK
    else:
        return DEFAULT_RED

# set frame background color
def setFrameColor(frame):
    frame.config(bg=getBackgroundColor(display_mode))

# set main logo color
def setMainLogoColor(color):
    main_logo_button.config(bg=color, activebackground=color)

# set style of button to red and gray
def setControlerStyle(button):
    button.config(bd=0,
        bg="#E7E7E7",
        activebackground="#E7E7E7",
        fg="black",
        activeforeground="black",
        font = ("Century Gothic", 16, "bold"))
    # hover effect
    changeOnHover(button, "#F44336", "#E7E7E7", "white", "black")

# function to change properties of button on hover
def changeOnHover(button :Button,
    background_color_on_hover,
    background_color_on_leave,
    foreground_color_on_hover,
    foreground_color_on_leave):  
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        background=background_color_on_hover, foreground=foreground_color_on_hover))
  
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        background=background_color_on_leave, foreground=foreground_color_on_leave)) 

# ****************************************************************************************************
# pack displayes

# clear previous display
def clearDisplay():
    global root_frame
    root_frame.destroy()
    root_frame = tk.Frame(root)
    root_frame.pack(fill=tk.BOTH, expand=True) 

# update main window display
def updateDisplay():
    clearDisplay()
    setFrameColor(root_frame)

    file_items_cnt = len(FileItem.file_items_list)
    if file_items_cnt == 0:
        packMainDisplay()
    elif file_items_cnt > 1:
        packMultipleFilesDisplay()
    elif FileItem.file_items_list[0].file_type == ".pdf":
        packSinglePDFDisplay()
    elif FileItem.file_items_list[0].file_type == ".png":
        # single png display
        pass

# Main Display
def packMainDisplay():
    packTopMainLogo(root_frame, getThemeColor())
    packMainBrowseButton(root_frame, getThemeColor())

# Multiple Files Display    
def packMultipleFilesDisplay():
    packTopMainLogo(root_frame, getThemeColor(display_mode))

    # pack a scrollable frame and return it 
    scrollable_container = getScrollableContainer(root_frame)
    gridFileItemsList(scrollable_container)
    packMultipleFilesControlers(root_frame)

# Single PDF Display
def packSinglePDFDisplay():
    packTopMainLogo(root_frame, getThemeColor(display_mode))
    packAddFilesButton(root_frame)

#Single PNG Display

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

# pack maze pdf main logo
def packTopMainLogo(container, background_color):
    # to enable setting theme
    global main_logo_button

    logo_image = getAsset("main-logo")
    if logo_image != "":
        main_logo_button = tk.Button(container,
        text=" mazePDF",
        font = ("Arial Rounded MT Bold", 70, "bold"),
        pady= 5,
        bd=0,
        bg=background_color,
        activebackground=background_color,
        fg="white", 
        activeforeground="white",
        height=96,
        width=96,
        command=showProgramInfo,
        image=logo_image,
        compound="left")
    else:
        main_logo_button = tk.Button(container,
        text="mazePDF",
        font = ("Arial Rounded MT Bold", 70, "bold"),
        bd=0,
        bg=background_color,
        activebackground=background_color,
        fg="white", 
        activeforeground="white",
        command=showProgramInfo)
    
    main_logo_button.pack(fill=tk.X, side=tk.TOP)

# pack main browse files button
def packMainBrowseButton(container, background_color):
    browse_files_image = getAsset("white-browse-files")
    main_browse_button = tk.Button(container, 
        text="Browse...",
        bd=0,
        bg=background_color,
        activebackground=background_color,
        fg="white",
        activeforeground="white",
        font = ("Times new roman", 50),
        command=selectFiles,
        image=browse_files_image)

    # hover effect
    changeOnHover(main_browse_button, getAnalogousColor(background_color),
        background_color, "white", "white")
    main_browse_button.pack(expand=True, fill=tk.BOTH)

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
        # padx to determine the space between the frame controlers and the FileItem frame
        frame.grid(row=0, column=1, rowspan=3, sticky=tk.NS, padx=5) 
        i += 1       
        
def createFileItemFrame(container, file_item: FileItem):
    if file_item.file_type == ".pdf":
        return createPDFItemFrame(container, file_item)
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

def createPDFItemFrame(container, pdf_item: PDFItem):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    pdf_frame = tk.Frame(container, bg=background_color, bd=0)
    
    # file icon
    Button(pdf_frame, 
        image=getAsset("pdf-file-icon"),
        bd=0,
        text="open pdf", 
        bg=background_color, 
        activebackground=background_color,
        fg=foreground_color, 
        activeforeground=foreground_color,
        command=lambda: openFile(pdf_item)
        ).grid(row=0, column=0, rowspan=3, sticky=tk.NS)

    # file name
    getStyleLabel(pdf_frame, "name: " + FileItem.getFileName(pdf_item), True
        ).grid(row=0, column=1, columnspan=2, sticky=tk.SW)

    # file size
    getStyleLabel(pdf_frame, "size: " + FileItem.get_formatted_size(pdf_item.size)
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

# ====================================================================================================

def packAddFilesButton(container):
    background_color = getBackgroundColor(display_mode)
    controlers_frame = tk.Frame(container, bg=background_color, bd=0)
    controlers_frame.pack(fill=tk.X, pady=0)

    # add files button
    add_files_button = tk.Button(controlers_frame, 
        text="Add Files",
        command=selectFiles)
    setControlerStyle(add_files_button)
    add_files_button.pack(fill=tk.X, expand=True)

def packMultipleFilesControlers(container):
    background_color = getBackgroundColor(display_mode)
    controlers_frame = tk.Frame(container, bg=background_color, bd=0)
    controlers_frame.pack(fill=tk.X, pady=3)

    # merge files button
    merge_files_button = tk.Button(controlers_frame, 
        text="Merge Files",
        command=mergeFiles)
    setControlerStyle(merge_files_button)
    merge_files_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # merge pages button
    merge_pages_button = tk.Button(controlers_frame, 
        text="Merge Pages",
        command=mergeFiles,
        state=tk.DISABLED)
    setControlerStyle(merge_pages_button)
    merge_pages_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # sort files button
    sort_button = tk.Button(controlers_frame, 
        text="Sort",
        command=sortItemsDisplay)
    setControlerStyle(sort_button)
    sort_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # reverse files button
    reverse_button = tk.Button(controlers_frame, 
        text="Reverse",
        command=reverseItemsDisplay)
    setControlerStyle(reverse_button)
    reverse_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

    packAddFilesButton(container)

# ****************************************************************************************************

# when mazePDF starts
def startMaze():
    initialRoot()
    global root_frame
    root_frame = tk.Frame(root)

    initialAssets()
    #initialStats and thems and lang ???

    updateDisplay()

# when mazePDF ends
def endMaze():
    # save stats ???
    print("Thank you for using mazePDF!")

# ====================================================================================================

def initialRoot():
    global root
    root = tk.Tk()
    root.title("mazePDF")

    # set mazePDF icon
    try:
        root.iconbitmap('./assets/icons/maze_pdf_icon.ico')
    except:
        pass # ignore.

    # enable resizing
    root.resizable(True, True)

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # set root dimension
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 800
    root.minsize(600, 400)
    #WINDOW_WIDTH = int(screen_width * 0.5)
    #WINDOW_HEIGHT = int(screen_height * 0.95)

    # find the center point
    center_x = int((screen_width / 2) - (WINDOW_WIDTH / 4))
    center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

    # set the position of the window to the center of the screen
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")

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