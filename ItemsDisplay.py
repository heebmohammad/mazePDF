import tkinter as tk
from tkinter import ttk
from AppPreferences import AppPreferences
from BrowseFiles import isImageType
from FileItem import FileItem

# pack controller with style
def packController(container, text, func):
    button = tk.Button(container, text=text, command=func)
    AppPreferences.setControllerStyle(button)
    button.pack(fill=tk.X, side=tk.LEFT, expand=True)
    return button

def createFileItemFrame(container, file_item):
        if file_item.file_type == ".pdf":
            return createPDFItemFrame(container, file_item)
        elif isImageType(file_item.file_type):
            return createImageItemFrame(container, file_item)
        else:
            pass

# ****************************************************************************************************

class MultipleFilesDisplay(tk.Frame):
    def __init__(self, container, window, columns_num=1):
        super().__init__(container)
        self.window = window
        self.columns_num = columns_num
        self.getScrollableContainer()
        self.gridFileItemsList(self.scrollable_container)


# ====================================================================================================

    # pack canvas and scrollbar, and return the srollable frame
    def getScrollableContainer(self):
        # create frame for canvas and scrollbar
        both_frame = tk.Frame(self)
        both_frame.pack(fill=tk.BOTH, expand=True)

        # create a canvas
        my_canvas = tk.Canvas(both_frame, highlightthickness=0)
        self.window.style.setFrameColor(my_canvas)

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
        self.window.style.setFrameColor(scrollable_frame)

        # pack the scrollable frame to my_canvas
        #scrollable_frame.pack(fill=tk.BOTH, expand=True)

        # add the scrollable freame to a window in the canvas
        my_canvas.create_window((0,0), window=scrollable_frame, anchor=tk.CENTER)

        # save the scrollable frame
        self.scrollable_container = scrollable_frame

# ====================================================================================================

    def gridFileItemsList(self, container):
        i = 0
        for file_item in FileItem.file_items_list:
            controled_container = getControledContainer(container, file_item, i)
            frame = createFileItemFrame(controled_container, file_item)
            # padx to determine the space between the frame controllers and the FileItem frame
            frame.grid(row=0, column=1, rowspan=3, sticky=tk.NS, padx=5) 
            i += 1 

    # convert index to row, column
    def getRowAndColumn(self, index):
        return int(index / self.columns_num), index % self.columns_num

    def getControledContainer(self, container, file_item, index):
        
        controled_container = tk.Frame(container, bd=0)
        self.window.style.setFrameColor(controled_container)

        row, column = self.getRowAndColumn(index)
        # pady to determine the space between two frames
        # padx to determine the space between the controled_container and the edge
        controled_container.grid(row=row, column=column, pady=5, padx=5, sticky=tk.EW)

        # item up button
        up_button = self.getFrameControlButton(controled_container, "up", "item-frame-up", 
            lambda: upFileItem(file_item)).grid(row=0, column=0, sticky=tk.S)

        # item down button
        down_button = self.getFrameControlButton(controled_container, "down", "item-frame-down", 
            lambda: downFileItem(file_item)).grid(row=1, column=0, sticky=tk.N)

        # item delete button
        delete_button = self.getFrameControlButton(controled_container, "delete", "delete-file", 
            lambda: deleteFileItem(file_item)).grid(row=2, column=0, sticky=tk.EW)

        # item edit button ???

        return controled_container

    def getFrameControlButton(self, container, text, key_asset, func):
        button = tk.Button(container, 
            image=self.window.style.getAsset(key_asset),
            text=text,
            command=func
        )
        self.window.style.setFrameControlStyle(button)

# ====================================================================================================

    def packMultipleFilesControllers(self, container):
        controllers_frame = tk.Frame(container, bd=0)
        self.window.style.setFrameColor(controllers_frame)
        controllers_frame.pack(fill=tk.X, pady=3)

        # merge files button
        packController(controllers_frame, "Merge Files", mergeFiles)

        # merge pages button
        packController(controllers_frame, "Merge Pages", mergeFiles).config(state=tk.DISABLED)

        # sort files button
        packController(controllers_frame, "Sort", sortItemsDisplay)

        # reverse files button
        packController(controllers_frame, "Reverse", reverseItemsDisplay)                

# ****************************************************************************************************

    # merge all files in file_items_list to pdf file
    def mergeFiles(self):
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
            FileItem.showSomethingWentWrong("merge files failed!", e)

    def openFile(file_item):
        try:
            # if file_type == ".pdf": open in tkinter ???
            file_item.openFile()
        except Exception as e:
            file_name = FileItem.getFileName(file_item)
            FileItem.showSomethingWentWrong("openning " + file_name + "failed!" , e)

    def sortItemsDisplay():
        try:
            FileItem.sortFileItemsList()
            updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to sort." , e)

    def reverseItemsDisplay():
        try:
            FileItem.reverseFileItemsList()
            updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("failed to reverse." , e)

    # ****************************************************************************************************

    def deleteFileItem(file_item):
        try:
            FileItem.deleteFileItems(file_item)
            updateDisplay()
        except Exception as e:
            file_name = FileItem.getFileName(file_item)
            FileItem.showSomethingWentWrong("failed to delete " + file_name , e)

    def upFileItem(file_item):
        try:
            FileItem.forewardFileItems(file_item)
            updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error up!", e)

    def downFileItem(file_item):
        try:
            FileItem.backwardFileItems(file_item)
            updateDisplay()
        except Exception as e:
            FileItem.showSomethingWentWrong("error down!", e)
