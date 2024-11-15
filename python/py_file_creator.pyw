import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python File Generator")
        self.root.geometry("400x450")
        self.file_count = 1
        self.directory = None

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))

        self.lbl_directory = ttk.Label(self.root, text="Selected Directory: None")
        self.lbl_directory.pack(pady=10)

        self.btn_select_dir = ttk.Button(self.root, text="Select Directory", command=self.select_directory)
        self.btn_select_dir.pack(pady=10)

        self.lbl_filename = ttk.Label(self.root, text="Enter File Name:")
        self.lbl_filename.pack(pady=5)

        self.entry_filename = ttk.Entry(self.root, width=30)
        self.entry_filename.pack(pady=5)

        self.btn_add_file = ttk.Button(self.root, text="Add New File", command=self.add_file)
        self.btn_add_file.pack(pady=10)

        self.file_listbox = tk.Listbox(self.root, width=50, height=10)
        self.file_listbox.pack(pady=10)

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.lbl_directory.config(text=f"Selected Directory: {self.directory}")
        else:
            self.lbl_directory.config(text="Selected Directory: None")

    def add_file(self):
        if not self.directory:
            messagebox.showwarning("Warning", "Please select a directory first!")
            return

        filename = self.entry_filename.get().strip()
        if not filename:
            messagebox.showwarning("Warning", "Please enter a file name!")
            return

        full_filename = f"{self.directory}/{filename}_{self.file_count}.py"
        try:
            with open(full_filename, 'w') as f:
                f.write("# This is an empty Python file\n")
            self.file_listbox.insert(tk.END, f"File {self.file_count}: {full_filename}")
            self.file_count += 1
        except Exception as e:
            messagebox.showerror("Error", f"Could not create file: {e}")

root = tk.Tk()
app = FileGeneratorApp(root)
root.mainloop()
