from email.policy import default
from glob import glob
from operator import truth
from textwrap import fill
import tkinter as tk
from tkinter import Button, Canvas, Label, filedialog as fd
from tkinter.messagebox import showerror, showinfo
from tkinter import CENTER, TclError, ttk
from typing import Container
from FileItem import FileItem, PDFItem

# light or dark display mode
display_mode = "DARK"

# list of FileItem packed frames
file_item_frames = []

SUPPORTED_FILE_TYPES = (
    ("pdf files", "*.pdf"),
    ("pdf files", "*.PDF"),
    ("png files", "*.png"),
    ("All files", "*.*")
)

def isSupportedFileType(file_type):
    return (any([("*" + file_type) in tup for tup in SUPPORTED_FILE_TYPES]))

def packMultipleFilesControlers(container):
    # merge files button
    try:
        browse_files_image = tk.PhotoImage(file='./assets/images/0000.png')
    except TclError as e: 
        merge_files_button = tk.Button(container, 
            text="Merge Files",
            bd=0,
            bg="#E7E7E7",
            activebackground="#E7E7E7",
            fg="black",
            activeforeground="black",
            font = ("Times new roman", 24),
            height=2,
            width=18,
            command=mergeFiles)
    else:
        #fix???
        merge_files_button = tk.Button(container, 
            text=" Browse...",
            bd=0,
            bg="#4CAF50",
            activebackground="#4CAF50",
            fg="white",
            activeforeground="white",
            font = ("Times new roman", 50),
            height=350,
            width=500,
            command=selectFiles,
            image=browse_files_image)

    # hover effect
    changeOnHover(merge_files_button, "#F44336", "#E7E7E7", "white", "black")
    merge_files_button.pack()

#==================================================================================================    



# ****************************************************************************************************
# show messages functions

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
    filenames = fd.askopenfilenames(
        title = "select files...",
        initialdir='/',
        filetypes=SUPPORTED_FILE_TYPES)
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
        showSomethingWentWrong("Failed creating item file of \"" + file_path + "\"", e)

# merge all files in file_items_list to pdf file
def mergeFiles():
    #ask for save path
    try:
        FileItem.mergeFilesToPdf()
    except Exception as e:
        showSomethingWentWrong("merge files failed!", e)

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

# set main window color
def setFrameColor(frame):
    frame.config(bg=getBackgroundColor(display_mode))

# set main logo color
def setMainLogoColor(color):
    main_logo_button.config(bg=color, activebackground=color)

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

    file_items_cnt = len(FileItem.file_items_list)
    if file_items_cnt == 0:
        packMainDisplay()
    elif file_items_cnt > 1:
        packMultipleFilesDisplay()
    elif FileItem.file_items_list[0].file_type == ".pdf":
        # single pdf display
        pass

# Main Display
def packMainDisplay():
    packTopMainLogo(root_frame, getThemeColor())
    packMainBrowseButton(root_frame, getThemeColor())

# Multiple Files Display    
def packMultipleFilesDisplay():
    setFrameColor(root_frame)
    packTopMainLogo(root_frame, getThemeColor(display_mode))

    # pack a scrollable frame and return it 
    scrollable_container = getScrollableContainer(root_frame)
    packFileItemsList(scrollable_container)
    packMultipleFilesControlers(root_frame)

#Single PDF Display
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
    global main_logo_button
    global logo_image
    try:
        logo_image = tk.PhotoImage(file='./assets/images/maze_pdf_logo.png')
    except TclError as e:
        main_logo_button = tk.Button(container,
            text="mazePDF",
            font = ("Arial Rounded MT Bold", 70, "bold"),
            bd=0,
            bg=background_color,
            activebackground=background_color,
            fg="white", 
            activeforeground="white",
            command=showProgramInfo)
    else:
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
    
    main_logo_button.pack(fill=tk.X, side=tk.TOP)

# pack main browse files button
def packMainBrowseButton(container, background_color):
    global main_browse_button
    global browse_files_image
    try:
        browse_files_image = tk.PhotoImage(file='./assets/images/Folder-Open-icon.png')
    except TclError as e: 
        main_browse_button = tk.Button(container, 
            text="Browse...",
            bd=0,
            bg=background_color,
            activebackground=background_color,
            fg="white",
            activeforeground="white",
            font = ("Times new roman", 50),
            height=2,
            width=18,
            command=selectFiles)
    else:
        main_browse_button = tk.Button(container, 
            text=" Browse...",
            bd=0,
            bg=background_color,
            activebackground=background_color,
            fg="white",
            activeforeground="white",
            font = ("Times new roman", 50),
            height=350,
            width=500,
            command=selectFiles,
            image=browse_files_image)

    # hover effect
    changeOnHover(main_browse_button, getAnalogousColor(background_color),
        background_color, "white", "white")
    main_browse_button.pack(expand=True, fill=tk.BOTH)

# ====================================================================================================

def packFileItemsList(container):
    file_item_frames.clear()
    for file_item in FileItem.file_items_list:
        frame = createFileItemFrame(container, file_item)
        file_item_frames.append(frame)
        
def createFileItemFrame(container, file_item: FileItem):
    if file_item.file_type == ".pdf":
        return createPDFItemFrame(container, file_item)
    else:
        pass

def createPDFItemFrame(container, pdf_item: PDFItem):
    foreground_color = getForegroundColor(display_mode)
    background_color = getBackgroundColor(display_mode)
    pdf_frame = tk.Frame(container, bg=background_color)
    
    # file icon
    Button(pdf_frame, text="icon", bg=background_color, activebackground=background_color,
    fg=foreground_color, activeforeground=foreground_color).grid(row=0, column=0, rowspan=3, sticky=tk.NS)

    # file name
    file_name = pdf_item.file_name + pdf_item.file_type
    Label(pdf_frame, text=file_name, background=background_color,
    foreground=foreground_color).grid(row=0, column=1, columnspan=2, sticky=tk.W)

    # file size
    file_size = str(pdf_item.size) + " bytes"
    Label(pdf_frame, text=file_size, background=background_color,
    foreground=foreground_color).grid(row=1, column=1, columnspan=2, sticky=tk.W)

    # file number of pages
    file_num_pages = str(pdf_item.num_pages) + " pages"
    Label(pdf_frame, text=file_num_pages, background=background_color,
    foreground=foreground_color).grid(row=2, column=1, columnspan=2, sticky=tk.W)

    pdf_frame.pack(fill=tk.X, expand=True)
    return pdf_frame

# ****************************************************************************************************

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

root_frame = tk.Frame(root)
updateDisplay()

# fixing the blur UI on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()