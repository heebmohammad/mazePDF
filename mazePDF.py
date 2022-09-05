import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import CENTER, TclError, ttk

files_queue = []

def showProgramInfo():
    showinfo(title="about mazePDF", message="M.HEEB!")

def addFilesToQueue(filenames):
    for filename in filenames:
        files_queue.append(filename)
    print(files_queue)

FILE_TYPES = (
    ("pdf files", "*.pdf"),
    ("png files", "*.png"),
    ("All files", "*.*")
)

def selectFiles():
    filenames = fd.askopenfilenames(
        title = "select files...",
        initialdir='/',
        filetypes=FILE_TYPES)
    addFilesToQueue(filenames)

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

#red= #f40f02
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

main_browse_button.pack(expand=True, fill=tk.BOTH)

# hover effect
changeOnHover(main_browse_button, "#3e8e41", "#4CAF50", "white", "white")

# fixing the blur UI on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()