import tkinter as tk 
from tkinter import ttk

LARGEFONT =("Verdana", 35)

class Application(tk.Tk):
	
	# __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
        self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
        for page in (All, All2):

            frame = page(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
            self.frames[page] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(All)

	# to display the current frame passed as
	# parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class All(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
        label = ttk.Label(self, text ="All characters", font = LARGEFONT)
		
		# putting the grid in its place by using
		# grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

class All2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
        label = ttk.Label(self, text ="All characters", font = LARGEFONT)
		
		# putting the grid in its place by using
		# grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

def start_gui():
    app = Application()
    app.geometry("1000x500")
    app.mainloop()


