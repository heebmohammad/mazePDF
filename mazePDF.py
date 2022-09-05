import tkinter as tk
from tkinter import CENTER, TclError, ttk

def selectNewFile():
    return

# ****************************************************************************************************

root = tk.Tk()
root.title("mazePDF")
# set mazePDF icon
root.iconbitmap('./assets/icons/maze_pdf_icon.ico')
# enable resizing
root.resizable(True, True)

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# set root dimension
WINDOW_WIDTH = int(screen_width * 0.5)
WINDOW_HEIGHT = int(screen_height * 0.95)

# find the center point
center_x = int(screen_width / 2 - WINDOW_WIDTH / 2)
center_y = int(screen_height / 2 - WINDOW_HEIGHT / 2)

# set the position of the window to the center of the screen
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")

# maze pdf main logo
try:
    logo_image = tk.PhotoImage(file='./assets/images/maze_pdf_logo.png')
except TclError as e: 
    logo_label = ttk.Label(root, 
        text="mazePDF", 
        padding=5, 
        anchor=CENTER,
        foreground="white",
        background="#f40f02",
        font = ("Arial Rounded MT Bold", 70, "bold"))
else:
    logo_label = ttk.Label(root, image=logo_image, padding=5)
logo_label.pack()



# fixing the blur UI on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()