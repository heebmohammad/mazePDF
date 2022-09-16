import tkinter as tk
from AppPreferences import AppPreferences

# App Preferences
app_style = AppPreferences()

class InputWindow(tk.Toplevel):

    def __init__(self, *args, title, fields, description="", callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        #self.title = title
        self.fields_list = fields
        self.description = description
        self.callback = callback
        self.title(title)

        self.styleWindow()
        self.packInputsDisplay()

    def styleWindow(self):
        self.config(width=300, height=200)
        # Disable the button for resizing the window.
        self.resizable(False, False)

        # windows only (remove the minimize/maximize button)
        self.attributes('-toolwindow', True)
        self.attributes('-alpha', 1.0)

        # get focus automatically
        self.focus()

        # modal window (disable user from using the main window while the input window is visible)
        self.grab_set()

    def packInputsDisplay(self):
        # input window display container
        self.display_container = tk.Frame(self)
        self.display_container.pack(fill=tk.BOTH, expand=True)
        app_style.setFrameColor(self.display_container)
        self.gridFields()
        self.gridDoneButton()
        

    def packTest(self):
        tk.Label(self, text="hello world!", font=("Arial", 200)).pack()
    
    def gridFields(self):
        self.fields_dictionary = {}

        row = 0
        for field in self.fields_list:
            label = tk.Label(self.display_container, text=field + ":")
            label.grid(row=row, column=0)

            entry = tk.Entry(self.display_container)
            entry.grid(row=row, column=1)
            if row == 0:
                entry.focus()
            self.fields_dictionary[field] = entry

            row += 1
        
        # first fet focus ???

    
    def getAnswers(self):
        fields_answers = {}
        for field, entry in self.fields_dictionary.items():
            fields_answers[field] = entry.get()
        
        return fields_answers
    
    def getAnswersList(self):
        fields_answers = []
        for field, entry in self.fields_dictionary.items():
            fields_answers.append(entry.get())
        
        return fields_answers
        
    def gridDoneButton(self):
        button = tk.Button(self.display_container, text="Done!", command=self.doneFunction)
        app_style.setControllerStyle(button)
        button.grid(row=100, column=100)
    
    def doneFunction(self):
        self.callback(*(self.getAnswersList()))

    def closeWindow(self):
        # Close the window.
        self.destroy()
