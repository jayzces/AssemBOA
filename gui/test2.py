import tkFileDialog
from Tkinter import *

class Assemboa(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # self.centerWindow()
        self.parent.geometry('+100+100')
        self.initUI()
        self.start()


    def centerWindow(self):
        w = 700
        h = 500
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


    def initUI(self):
        self.parent.title("Assemboa")
        self.pack(expand=1)


    def hideWidgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        try:
            self.f2.destroy()
        except:
            pass


    def start(self):
        self.hideWidgets()
        self.img = PhotoImage(file="new.gif")
        self.img2 = PhotoImage(file="open.gif")
        self.img3 = PhotoImage(file="run.gif")
        self.new_btn = Button(self, text="New", command=self.new, padx=10,
            image=self.img, compound="top")
        self.new_btn.pack(side=LEFT)
        self.open_btn = Button(self, text="Open", command=self.open, padx=10,
            image=self.img2, compound="top")
        self.open_btn.pack(side=LEFT)
        self.run_btn = Button(self, text="Run", command=self.run, padx=10,
            image=self.img3, compound="top")
        self.run_btn.pack(side=LEFT)


    def new(self):
        self.hideWidgets()
        self.text = Text(self, width=50, height=20, padx=10, pady=10)
        self.text.pack(padx=10, pady=10)
        self.f2 = Frame(self)
        self.f2.pack()
        self.menu_btn = Button(self.f2, text="Back to Menu",
            command=self.start, padx=20)
        self.menu_btn.pack(side=LEFT)
        self.translate_btn = Button(self.f2, text="Translate to Machine Language",
            command=self.translate, padx=20)
        self.translate_btn.pack(side=LEFT)


    def open(self):
        self.file_options = options = {}
        options['multiple'] = False
        options['parent'] = self.parent
        
        t = tkFileDialog.askopenfile(mode='rb', **options)

        if t:
            f = open('input.in', 'wb')

            for line in t:
                f.write(line)

            f.close()

            self.hideWidgets()
            self.text = Text(self, width=50, height=20, padx=10, pady=10)

            with open('input.in', 'rb') as txt:
                for line in txt:
                    self.text.insert(INSERT, line)

            self.text.pack(padx=10, pady=10)
            self.f2 = Frame(self)
            self.f2.pack()
            self.menu_btn = Button(self.f2, text="Back to Menu",
                command=self.start, padx=20)
            self.menu_btn.pack(side=LEFT)
            self.translate_btn = Button(self.f2, text="Translate to Machine Language",
                command=self.translate, padx=20)
            self.translate_btn.pack(side=LEFT)


    def translate(self):
        t = self.text.get("1.0", END)
        f = open('input.in', 'wb')
        f.write(t)
        f.close()

        self.hideWidgets()
        self.text = Text(self, width=50, height=20, padx=10, pady=10)

        with open('output.out', 'rb') as txt:
            for line in txt:
                self.text.insert(INSERT, line)

        self.text.pack(padx=10, pady=10)
        self.f2 = Frame(self)
        self.f2.pack()
        self.menu_btn = Button(self.f2, text="Back to Menu",
            command=self.start, padx=20)
        self.menu_btn.pack(side=LEFT)
        self.run_btn = Button(self.f2, text="Run", command=self.run,
            padx=20)
        self.run_btn.pack(side=LEFT)


    def run(self):
        self.hideWidgets()
        self.pack(fill=BOTH, expand=1)
        self.f2 = Frame(self)
        self.f2.pack(padx=10, pady=10)

        var = StringVar()
        self.title = Label(self.f2, textvariable=var, relief=RAISED, bd=0)
        var.set("Output")
        self.title.grid(row=0, column=0)
        self.text = Text(self.f2, width=34, height=15, padx=10, pady=10)
        self.text.grid(row=1, column=0, padx=13)

        var2 = StringVar()
        self.title2 = Label(self.f2, textvariable=var2, relief=RAISED, bd=0)
        var2.set("Stack")
        self.title2.grid(row=0, column=1)
        self.text2 = Text(self.f2, width=10, heigh=15, padx=10, pady=10)
        self.text2.grid(row=1, column=1, padx=13)

        self.f3 = Frame(self)
        self.f3.pack()

        var3 = StringVar()
        self.title3 = Label(self.f3, textvariable=var3, relief=RAISED, bd=0)
        var3.set("Log")
        self.title3.pack()
        self.text3 = Text(self.f3, width=50, height=7, padx=10, pady=10,
            bg="black", fg="white")
        self.text3.pack()

        self.f4 = Frame(self)
        self.f4.pack(pady=10)

        self.view_code = Button(self.f4, text="View Code",
            command=self.viewCode, padx=20)
        self.view_code.pack(side=LEFT)
        self.view_ml = Button(self.f4, text="View Machine Language Code",
            command=self.viewML, padx=20)
        self.view_ml.pack(side=LEFT)

        self.f5 = Frame(self)
        self.f5.pack(pady=5)

        self.new_btn = Button(self, text="New", command=self.new, padx=10,
            image=self.img, compound="top")
        self.new_btn.pack(side=LEFT)
        self.open_btn = Button(self, text="Open", command=self.open, padx=10,
            image=self.img2, compound="top")
        self.open_btn.pack(side=LEFT)


    def viewCode(self):
        self.hideWidgets()


    def viewML(self):
        self.hideWidgets()



root = Tk()
app = Assemboa(root)
root.mainloop()