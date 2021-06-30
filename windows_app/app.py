import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg='steel blue')
        self.create_widgets()
        self.canvas = self.create_canvas()
    
    def create_canvas(self):
        canvas = tk.Canvas(self.master, width = 1000, height = 1000, bg='steel blue')
        canvas.pack()
        return canvas

    def create_widgets(self):
        self.hi = tk.Button()
        self.hi["text"] = "CLICK"
        self.hi["command"] = self.say_hi
        self.hi.pack(side="top")
    
    def say_hi(self):
        self.canvas.create_text(500, 500, text='hello retard', font='comicsans 30')

    
root = tk.Tk()
app = Application(master=root)
app.mainloop()