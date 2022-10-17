from tkinter import *
from tkinter.filedialog import askopenfilename

root = Tk("Computer Security")
filenames = []


def open_file():
    # Ask for path of json file
    filepath = askopenfilename(filetypes=[("Json Files", "*.json")], parent=root)
    root.destroy()
    print('file path:', filepath)

    if filepath:
        filenames.append(filepath)
        return filepath


def center(win):
    # centers a tkinter window
    # win: the main window or Toplevel window to center
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def setup_gui():
    root.title("Computer Security - Group 4")

    root.geometry("400x200")
    root.minsize(300, 150)
    root.maxsize(600, 300)

    center(root)

    frame_label = Frame(master=root)
    frame_btn = Frame(master=root)

    space_label1 = Label(master=frame_label)
    text_label = Label(master=frame_label, text="Select .json file", font=("AppleSystemUIFont", 20))
    space_label2 = Label(master=frame_label)
    open_btn = Button(master=frame_btn, text='Open File', height=2, width=10, command=open_file)

    space_label1.pack()
    text_label.pack()
    space_label2.pack()
    open_btn.pack()

    frame_label.pack()
    frame_btn.pack()

    root.mainloop()
