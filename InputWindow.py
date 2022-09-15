import tkinter as tk
from AppPreferences import AppPreferences

# App Preferences
app_style = AppPreferences()

class InputWindow(tk.Toplevel):

    def __init__(self, *args, title, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.callback = callback
        self.title(title)

        self.config(width=300, height=200)
        # Disable the button for resizing the window.
        self.resizable(False, False)

        # windows only (remove the minimize/maximize button)
        self.attributes('-toolwindow', True)
        self.attributes('-alpha', 0.95)

        # get focus automatically
        self.focus()

        # modal window (disable user from using the main window while the input window is visible)
        self.grab_set()

        # input window display container
        self.display_container = tk.Frame(self)
        self.display_container.pack(fill=tk.BOTH, expand=True)
        app_style.setFrameColor(self.display_container)

    def packTest(self):
        tk.Label(self, text="hello world!", font=("Arial", 200)).pack()
        
    def getDoneButton(self):
        button = tk.Button(self.display_container, text="Done!")
        app_style.setControllerStyle(button)
        self.callback("test")

        # Close the window.
        self.destroy()
