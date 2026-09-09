import os
import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox, simpledialog
from dbimporter import check_structure

LARGEFONT = ("Verdana", 24) # Reduced slightly for better scaling

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")

        self.content = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.frames = {}
        for page in (All,):
            frame = page(self.content, self, None)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(All)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class All(tk.Frame):
    def __init__(self, parent, controller, file_data):
        tk.Frame.__init__(self, parent)
        self.file_data = None
        
        label = ttk.Label(self, text ="DBImporter", font = LARGEFONT)
        label.grid(row = 0, column = 0, padx = 10, pady = 10)

        label = ttk.Label(self, text="Select file...")
        label.grid(row = 1, column = 0, padx = 10, pady = 10)

        file_btn = ttk.Button(
            self, 
            text="File", 
            command=self.open_file_dialogue)
        
        file_btn.grid(row = 1, column = 1, pady = 10)

        self.output_box = Output(self, controller)
        self.output_box.grid(row = 2, column = 0, padx = 10, pady = 10, sticky="nsew")

        fix_button = ttk.Button(
            self, 
            text="Fix", 
            command = self.fix_file)

        fix_button.grid(row = 3, column = 0, pady = 10)

    def trigger_text_change(self, text):
        self.output_box.update_display_text(text)

    def get_log_files(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

    def ask_user(self, question):
        answer = simpledialog.askstring("DBImporter", question, parent=self)
        return (answer or "N").strip().upper()

    def open_file_dialogue(self):
        base_path = os.getcwd()
        file_path = filedialog.askopenfilename(
        title="Select a file")

        
        if file_path:
            print(f"Selected file: {file_path}")
            if file_path == base_path+"/testfile.txt":
                file_path = base_path+"/src/dbimporter/data/find_unit_test.xlsx"
        else:
            print("No file selected.")
            #file_path = base_path+"/src/dbimporter/data/find_unit_test.xlsx"

        file_data = check_structure.Check(filename = file_path,
                            no_restructure=True,
                            file_type = "default",
                            automatic_start=True)

        self.file_data = file_data

        with open(base_path+"/dbimporter.logger.details.log", "r", encoding="utf-8") as file:
            content = file.read()

        self.trigger_text_change(content)

    def fix_file(self):
        if self.file_data is None:
            messagebox.showerror(
                "No file selected",
                "Please select a file before fixing."
            )
            return

        self.file_data.start_fix(gui=True, prompt_func=self.ask_user)




class Output(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(relief="groove", borderwidth=2)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text_widget = tk.Text(
            self,
            wrap="word",
            height=12,
            state="disabled",
            font=("Arial", 10)
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.text_widget.yview
        )
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)
        self.scrollbar.grid(row=0, column=1, sticky="ns", pady=5)

    def update_display_text(self, new_text):
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", new_text)
        self.text_widget.configure(state="disabled")


def start_gui():
    app = Application()
    app.geometry("1000x500")
    app.mainloop()
