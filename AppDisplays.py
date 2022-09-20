import tkinter as tk
from tkinter.messagebox import showinfo
from AppPreferences import MAIN_ICON_PATH, AppPreferences
from FileItem import FileItem
from BrowseFiles import BrowseFilesButton
from MultipleItemsDisplay import MultipleItemsDisplay
from Footer import Footer

MAIN_MESSAGE = (
    "mazePDF\n\n"
    + "Graphical user interface to work with pdf files\n"
    + "by: Mohammad Heeb\n\n"
    + "■ visit: https://github.com/heebmohammad/mazePDF"
    )

# App Preferences
app_style = AppPreferences()

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize App Preferences
        AppPreferences.initializeDefaultPreferences()
        
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

        # main window display (pages) container
        self.display_container = tk.Frame(self)

        # main window footer
        self.is_footer = False
        #self.main_footer = tk.Frame(self)
        #self.main_footer.pack(fill=tk.X, expand=True)

# ====================================================================================================

    # clear main window display container
    def clearDisplay(self):
        self.display_container.destroy()
        self.display_container = tk.Frame(self)
        self.display_container.pack(fill=tk.BOTH, expand=True)
        app_style.setFrameColor(self.display_container)

    # update main window display container
    def updateDisplay(self):
        self.clearDisplay()

        file_items_cnt = FileItem.getFileItemsCnt()
        if file_items_cnt == 0:
            self.packMainDisplay()
        elif file_items_cnt == 1:
            self.packSingleItemDisplay()
        else:
            self.packMultipleItemsDisplay()

# ====================================================================================================
    
    # Main Display
    def packMainDisplay(self):
        self.packTopMainLogo(self.display_container, True)
        BrowseFilesButton(self.display_container, self).packFull()
        # footer ???
        Footer(self.display_container, self).pack(fill=tk.X)

    # Multiple Files Display    
    def packMultipleItemsDisplay(self):
        self.packTopMainLogo(self.display_container)
        multiple_files_display = MultipleItemsDisplay(self.display_container, self, 1)
        multiple_files_display.pack(fill=tk.BOTH, expand=True)
        BrowseFilesButton(self.display_container, self).packWide()
        Footer(self.display_container, self).pack(fill=tk.X)

    # Single Item Display
    def packSingleItemDisplay(self):
        self.packTopMainLogo(self.display_container)
        file_item = FileItem.getFirstFileItem()
        self.packItemPreviewAndControllers(file_item)
        BrowseFilesButton(self.display_container, self).packWide()
        Footer(self.display_container, self).pack(fill=tk.X)

    # preview an item and its controllers
    def packItemPreviewAndControllers(self, file_item):
        self.file_item_preview = file_item.getPreview(self.display_container)
        self.file_item_preview.pack(fill=tk.Y, expand=True, pady=50)
        self.file_item_controllers = file_item.getControllers(self.display_container, self)
        self.file_item_controllers.pack(fill=tk.X, pady=3)

# ====================================================================================================
    
    # pack mazePDF main logo
    def packTopMainLogo(self, container, follow_theme=False):
        logo_image = app_style.getAsset("main-logo")
        if logo_image != "":
            self.main_logo_button = tk.Button(container,
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
            self.main_logo_button = tk.Button(container,
            text="mazePDF",
            font = ("Arial Rounded MT Bold", 70, "bold"),
            bd=0,
            command=showProgramInfo)
        
        app_style.setButtonColor(self.main_logo_button, follow_theme)
        self.main_logo_button.pack(fill=tk.X, side=tk.TOP)

def showProgramInfo():
    showinfo(title="about mazePDF", message=MAIN_MESSAGE)
