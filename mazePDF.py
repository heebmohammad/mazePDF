import tkinter as tk
from tkinter import Label, filedialog as fd
from tkinter.messagebox import showerror, showinfo
from tkinter import CENTER, TclError, ttk
from FileItem import FileItem, PDFItem

files_queue = []

SUPPORTED_FILE_TYPES = (
    ("pdf files", "*.pdf"),
    ("pdf files", "*.PDF"),
    ("png files", "*.png"),
    ("All files", "*.*")
)

def isSupportedFileType(file_type):
    return (any([("*" + file_type) in tup for tup in SUPPORTED_FILE_TYPES]))

def showProgramInfo():
    showinfo(title="about mazePDF", message="M.HEEB!")

def packMultipleFilesControlers():
    # merge files button
    try:
        browse_files_image = tk.PhotoImage(file='./assets/images/0000.png')
    except TclError as e: 
        merge_files_button = tk.Button(root, 
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
        merge_files_button = tk.Button(root, 
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

def packFileItemsList():
    #clear
    main_browse_button.pack_forget()
    #pack paths label
    list = FileItem.getPdfFilesPaths()
    str = ""
    for path in list:
        str += path + "\n"

    Label(text=str, foreground="white", background="black").pack(fill=tk.BOTH, expand=True)
    #single pdf pack buttons
    #single png pack buttons
    #multi pdf pack buttons
    packMultipleFilesControlers()

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

def createFileItem(file_path, file_type):
    if (file_type == ".pdf"):
        PDFItem(file_path)
    else:
        FileItem(file_path)

def addFilesToQueue(filenames):
    # list of unsupported files and their types
    unsupported_files = []
    # list of invalid paths
    invalid_paths = []

    for filename in filenames:
        if (FileItem.is_valid_file_path(filename)):
            file_type = FileItem.get_file_type(filename)
            if (isSupportedFileType(file_type)):
                #add file_path and file_type to files_queue
                #files_queue.append((filename, file_type))
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
    addFilesToQueue(filenames)
    # update file items list
    packFileItemsList()

def mergeFiles():
    #ask for save path
    FileItem.mergeFilesToPdf()

# function to change properties of button on hover
def changeOnHover(button,
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

root = tk.Tk()
root.title("mazePDF")
root.config(bg="black")

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

# maze pdf main logo
def packTopMainLogo(background_color):
    global logo_image
    try:
        logo_image = tk.PhotoImage(file='./assets/images/maze_pdf_logo.png')
    except TclError as e:
        logo_button = tk.Button(root,
            text="mazePDF",
            font = ("Arial Rounded MT Bold", 70, "bold"),
            bd=0,
            bg=background_color,
            activebackground=background_color,
            fg="white", 
            activeforeground="white",
            command=showProgramInfo)
    else:
        logo_button = tk.Button(root,
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
    
    logo_button.pack(fill=tk.X, side=tk.TOP)

#red= #F40F02
#green= #4CAF50
packTopMainLogo("#4CAF50")    

# main browse files button
try:
    browse_files_image = tk.PhotoImage(file='./assets/images/Folder-Open-icon.png')
except TclError as e: 
    main_browse_button = tk.Button(root, 
        text="Browse...",
        bd=0,
        bg="#4CAF50",
        activebackground="#4CAF50",
        fg="white",
        activeforeground="white",
        font = ("Times new roman", 50),
        height=2,
        width=18,
        command=selectFiles)
else:
    main_browse_button = tk.Button(root, 
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
changeOnHover(main_browse_button, "#3E8E41", "#4CAF50", "white", "white")
main_browse_button.pack(expand=True, fill=tk.BOTH)

# fixing the blur UI on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()