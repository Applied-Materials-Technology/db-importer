import os
import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from dbimporter import check_structure

LARGEFONT = ("Verdana", 24) # Reduced slightly for better scaling

# class Application(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
        
#         container = tk.Frame(self)
#         container.pack(side = "top", fill = "both", expand = True)

#         container.grid_rowconfigure(0, weight = 1)
#         container.grid_columnconfigure(0, weight = 1)

#         self.frames = {}

#         for page in (All,): 
#             frame = page(container, self)
#             self.frames[page] = frame
#             frame.grid(row = 0, column = 0, sticky ="nsew")

#         self.show_frame(All)

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
            frame = page(self.content, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(All)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class All(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
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
            command=self.open_file_dialogue)

        fix_button.grid(row = 3, column = 0, pady = 10)

        output_box2 = Output(self, controller)
        output_box2.grid(row = 4, column = 0, padx = 10, pady = 10, sticky="nsew")

        # text_widget = scrolledtext.ScrolledText(
        # #self.frames[All], 
        # self,
        # wrap=tk.WORD, 
        # font=("Arial", 10),
        # height=10
        # )

        # text_widget.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def trigger_text_change(self, text):
        self.output_box.update_display_text(text)

    def get_log_files(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content

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

        with open(base_path+"/dbimporter.logger.details.log", "r", encoding="utf-8") as file:
            content = file.read()

        self.trigger_text_change(content)


# class Output(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.config(relief="groove", borderwidth=2) 

#         frame_canvas = tk.Frame(self)
#         frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
#         frame_canvas.grid_rowconfigure(0, weight=1)
#         frame_canvas.grid_columnconfigure(0, weight=1)
#         frame_canvas.grid_propagate(False)
        
#         self.display_text = tk.StringVar()
#         self.display_text.set(" ")
        
#         label = ttk.Label(self, textvariable=self.display_text, wraplength=900)
#         label.grid(row = 0, column = 0, padx = 10, pady = 10)

#     def update_display_text(self, new_text):
#         self.display_text.set(new_text)

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
