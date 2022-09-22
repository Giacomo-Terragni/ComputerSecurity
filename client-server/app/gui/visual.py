from tkinter import Tk
from tkinter.filedialog import askopenfilename


def open_file():
    # Ask for path of json file
    filepath = askopenfilename(filetypes=[("Json Files", "*.json")], parent=root)
    print('path: ', filepath)

    if filepath:
        return filepath
