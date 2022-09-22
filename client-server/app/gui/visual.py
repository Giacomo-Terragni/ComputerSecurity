import tkinter as tk
from tkinter.filedialog import askopenfilename


def open_file():
    filepath = askopenfilename(filetypes=[("Json Files", "*.json")])
    if not filepath:
        return

    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Computer Security")

    window.rowconfigure(0, minsize=800, weight=1)
    window.columnconfigure(1, minsize=800, weight=1)

    txt_edit = tk.Text(window)
    frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, text="Open", command=open_file)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    frm_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    window.mainloop()
