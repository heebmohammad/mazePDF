import tkinter as tk
from tkinter.messagebox import showinfo
from AppPreferences import MAIN_ICON_PATH, AppPreferences
from FileItem import FileItem, PDFItem, ImageItem
from BrowseFiles import BrowseFilesButton

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # main window title
        self.title("mazePDF")

        # set main window icon
        try:
            self.iconbitmap(MAIN_ICON_PATH)
        except:
            pass # ignore.

        # enable resizing
        self.resizable(True, True)

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # set main window dimension
        WINDOW_WIDTH = 700
        WINDOW_HEIGHT = 800
        self.minsize(600, 400)
        #WINDOW_WIDTH = int(screen_width * 0.5)
        #WINDOW_HEIGHT = int(screen_height * 0.95)

        # find the center point
        center_x = int((screen_width / 2) - (WINDOW_WIDTH / 4))
        center_y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))

        # set the position of the main window to the center of the screen
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{center_x}+{center_y}")

        # initialize App Preferences
        self.style = AppPreferences()

        # main window container
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # main window header logo
        self.main_logo_button = self.packTopMainLogo(self.main_container)
        self.style.setButtonColor(self.main_logo_button)

        # main window display (pages) container
        self.display_container = tk.Frame(self.main_container)
        self.display_container.pack(fill=tk.BOTH, expand=True)

        # main window footer
        self.is_footer = False
        self.main_footer = tk.Frame(self.main_container)
        self.main_footer.pack(fill=tk.X, expand=True)

# ====================================================================================================

    # clear main window display container
    def clearDisplay(self):
        self.display_container.destroy()
        self.display_container = tk.Frame(self.main_container)
        self.display_container.pack(fill=tk.BOTH, expand=True)
        self.style.setFrameColor(self.display_container)

    # update main window display container
    def updateDisplay(self):
        self.clearDisplay()
        self.style.setButtonColor(self.main_logo_button)

        file_items_cnt = FileItem.getFileItemsCnt()
        if file_items_cnt == 0:
            self.packMainDisplay()
        elif file_items_cnt == 1:
            self.packSingleItemDisplay()
        else:
            self.packMultipleFilesDisplay()

# ====================================================================================================
    
    # Main Display
    def packMainDisplay(self):
        self.style.setButtonColor(self.main_logo_button, True)
        BrowseFilesButton(self.display_container, self, True)
        # footer ???

    # Multiple Files Display    
    def packMultipleFilesDisplay(self):
        self.style.setButtonColor(self.main_logo_button)
        # footer ???

        # pack a scrollable frame and return it 
        #scrollable_container = getScrollableContainer(root_frame)
        #gridFileItemsList(scrollable_container)
        #packMultipleFilesControllers(root_frame)

    # Single Item Display
    def packSingleItemDisplay(self):
        self.style.setButtonColor(self.main_logo_button)
        # footer ???

        file_item = FileItem.getFirstFileItem()
        #packSingleFileItemFrame(root_frame, file_item)
        #packFileItemControllers(root_frame, file_item)

# ====================================================================================================
    
    # pack mazePDF main logo
    def packTopMainLogo(self, container):
        logo_image = self.style.getAsset("main-logo")
        if logo_image != "":
            main_logo_button = tk.Button(container,
            text=" mazePDF",
            font = ("Arial Rounded MT Bold", 70, "bold"),
            pady= 5,
            bd=0,
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
            command=showProgramInfo)
        
        main_logo_button.pack(fill=tk.X, side=tk.TOP)
        return main_logo_button

def showProgramInfo():
    showinfo(title="about mazePDF", message="M.HEEB!")