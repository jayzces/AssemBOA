from Tkinter import *

class MyApp:
    def __init__(self, parent):
        self.top_left_label = Label(parent, text="Top Left")
        self.top_left_label.grid(row=0, column=0, padx=2, pady=2, sticky=N+S+W)

        self.top_right_label = Label(parent, text="Top Right")
        self.top_right_label.grid(row=0, column=1, padx=2, pady=2, sticky=N+S+E)

        self.text_box = Text(parent, height=5, width=40)
        self.text_box.grid(row=1, column=0, columnspan=2)

root = Tk()
root.title("Test UI")
myapp = MyApp(root)
root.mainloop()