import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from AppPreferences import AppPreferences
from FileItem import FileItem

# App Preferences
app_style = AppPreferences()

# scrollable container: canvas and scrollbar,
class ScrollableContainer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # self is as frame for canvas and scrollbar

        # create a canvas
        self.my_canvas = tk.Canvas(self, highlightthickness=0)
        app_style.setFrameColor(self.my_canvas)

        # create a scrollbar
        self.my_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.my_canvas.yview)

        # pack canvas and scrollbar
        self.my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # configure the canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion =self. my_canvas.bbox("all")))

        # create the scrollable frame
        self.scrollable_frame = tk.Frame(self.my_canvas)
        app_style.setFrameColor(self.scrollable_frame)

        # add the scrollable freame to a window in the canvas
        self.my_canvas.create_window((0,0), window=self.scrollable_frame, anchor=tk.CENTER)

# ****************************************************************************************************

class MultipleItemsDisplay(tk.Frame):
    def __init__(self, container, window, columns_num=1):
        super().__init__(container)
        self.window = window
        self.columns_num = columns_num

        # get a scrollable container
        self.scrollable_container = ScrollableContainer(self)
        self.scrollable_container.pack(fill=tk.BOTH, expand=True)

        # grid file_items_list into the scrollable container
        self.gridFileItemsList(self.scrollable_container.scrollable_frame)

        # pack multiple files controllers
        self.controllers = MultipleFilesControllers(self, self.window)
        self.controllers.pack(fill=tk.X, pady=3)

# ====================================================================================================

    def gridFileItemsList(self, container):
        i = 0
        for file_item in FileItem.file_items_list:
            item_control_container = ItemControlContainer(container, self.window, file_item)
            row, column = self.getRowAndColumn(i)
            item_control_container.setGrid(row, column)
            
            frame = file_item.getPreview(item_control_container.controled_item_frame)
            frame.pack(fill=tk.BOTH, expand=True)
            i += 1 

    # convert index to row, column
    def getRowAndColumn(self, index):
        return int(index / self.columns_num), index % self.columns_num

# ****************************************************************************************************

# item control container of file_item (with up, down, delete and edit)
class ItemControlContainer(tk.Frame):
    def __init__(self, container, window, file_item):
        super().__init__(container)
        self.window = window
        self.file_item = file_item
        
        self.config(bd=0)
        app_style.setFrameColor(self)

        # item up button
        self.up_button = app_style.getItemControlButton(self, "up", "item-frame-up", 
            lambda: self.upFileItem(file_item))
        self.up_button.grid(row=0, column=0, sticky=tk.S)

        # item down button
        self.down_button = app_style.getItemControlButton(self, "down", "item-frame-down", 
            lambda: self.downFileItem(file_item))
        self.down_button.grid(row=1, column=0, sticky=tk.N)

        # item delete button
        self.delete_button = app_style.getItemControlButton(self, "delete", "delete-file", 
            lambda: self.deleteFileItem(file_item))
        self.delete_button.grid(row=2, column=0, sticky=tk.EW)

        # item edit button ???
        #row=0, column=2

        # container of the controled item frame
        self.controled_item_frame = tk.Frame(self, bd=0)
        app_style.setFrameColor(self.controled_item_frame)

        # padx to determine the space between the item controllers and the FileItem frame
        self.controled_item_frame.grid(row=0, column=1, rowspan=3, padx=5, sticky=tk.NS) 

# ====================================================================================================

    def deleteFileItem(self, file_item):
        try:
            FileItem.deleteFileItems(file_item)
            self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to delete " + file_item.getFileName() , e)

    def upFileItem(self, file_item):
        try:
            FileItem.forewardFileItems(file_item)
            self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error up!", e)

    def downFileItem(self, file_item):
        try:
            FileItem.backwardFileItems(file_item)
            self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error down!", e)

# ====================================================================================================

    def setGrid(self, row, column):
        # pady to determine the space between two containers
        pady = 5
        # padx to determine the space between the ItemControlContainer and the edge
        padx = 5

        self.grid(row=row, column=column, pady=pady, padx=padx, sticky=tk.EW)

# ****************************************************************************************************

class MultipleFilesControllers(tk.Frame):
    def __init__(self, container, window):
        super().__init__(container)
        self.window = window

        self.config(bd=0)
        app_style.setFrameColor(self)

        # merge files button
        self.merge_files_button = app_style.getStyledController(
            self, "Merge Files", self.mergeFiles)
        self.merge_files_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # remove non-pdfs ???
        
        # full display (column_num = 3) ???

        # merge pages button
        self.merge_pages_button = app_style.getStyledController(
            self, "Merge Pages", self.mergeFiles)
        self.merge_pages_button.config(state=tk.DISABLED)
        self.merge_pages_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # sort files button
        self.sort_files_button = app_style.getStyledController(
            self, "Sort", self.sortItemsDisplay)
        self.sort_files_button.pack(fill=tk.X, side=tk.LEFT, expand=True)

        # reverse files button
        self.reverse_files_button = app_style.getStyledController(
            self, "Reverse", self.reverseItemsDisplay)      
        self.reverse_files_button.pack(fill=tk.X, side=tk.LEFT, expand=True)          

# ====================================================================================================

    # merge all files in file_items_list to pdf file
    def mergeFiles(self):
        #ask for save path
        try:
            save_file_path  =  fd.asksaveasfilename(
                title = "save merged file as...",
                initialdir = app_style.getLastDirectory(),
                initialfile = "merged_file.pdf",
                defaultextension=".pdf",
                filetypes = (("pdf file", "*.pdf"), ("All Files", "*.*")))

            if (save_file_path != ''):
                FileItem.mergeFilesToPdf(save_file_path)
                app_style.setLastDirectory(save_file_path)
        except Exception as e:
            FileItem.showSomethingWentWrong("merge files failed!", e)

# ====================================================================================================

    def sortItemsDisplay(self):
        try:
            FileItem.sortFileItemsList()
            self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to sort." , e)

    def reverseItemsDisplay(self):
        try:
            FileItem.reverseFileItemsList()
            self.window.updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to reverse." , e)

# ****************************************************************************************************
