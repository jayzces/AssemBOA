import tkFileDialog, tkSimpleDialog
from Tkinter import *

from syntactic_analyzer import *
from semantic_analyzer import *
from code_translator import *
from computer import *

class Assemboa(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.syntactic_analyzer = SyntacticAnalyzer()
        self.semantic_analyzer = SemanticAnalyzer(self.syntactic_analyzer.token_dictionary)
        # initially, code translator will be empty so you will need to call this line again
        self.code_translator = CodeTranslator(self.syntactic_analyzer.token_dictionary, self.semantic_analyzer.symbol_table)
        self.computer = Computer()
        self.entry = None
        self.label = None
        self.value = 0
        # self.centerWindow()
        self.parent.geometry('+50+50')
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
        # self.img3 = PhotoImage(file="run.gif")
        self.new_btn = Button(self, text="New", command=self.new, padx=10,
            image=self.img, compound="top")
        self.new_btn.pack(side=LEFT)
        self.open_btn = Button(self, text="Open", command=self.open, padx=10,
            image=self.img2, compound="top")
        self.open_btn.pack(side=LEFT)


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


        # Start of actual translation
        self.syntactic_analyzer.analyze('input.in')
        self.semantic_analyzer = SemanticAnalyzer(self.syntactic_analyzer.token_dictionary)
        self.semantic_analyzer.analyze('input.in')
        self.code_translator = CodeTranslator(self.syntactic_analyzer.token_dictionary, self.semantic_analyzer.symbol_table)
        self.code_translator.translate('output.out')


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
        self.text2 = Text(self.f2, width=10, height=15, padx=10, pady=10)

        if not self.computer.stack:
            for x in range(0,5):
                self.text2.insert(END, '[' + str(x) + ']: Empty\n')


        self.text2.grid(row=1, column=1, padx=13)

        var3 = StringVar()
        self.title3 = Label(self.f2, textvariable=var3, relief=RAISED, bd=0)
        var3.set("Array")
        self.title3.grid(row=0, column=2)
        self.text3 = Text(self.f2, width=20, height=15, padx=10, pady=10)
        self.text3.grid(row=1, column=2, padx=13)

        if self.computer.address_space is not None:
            for address in self.computer.address_space:
                self.text3.insert(INSERT, '[' + str(address) + ']\n')

        self.f3 = Frame(self)
        self.f3.pack()

        var4 = StringVar()
        self.title4 = Label(self.f3, textvariable=var4, relief=RAISED, bd=0)
        var4.set("Log")
        self.title4.pack()
        self.text4 = Text(self.f3, width=76, height=7, padx=10, pady=10,
            bg="black", fg="white")
        self.text4.pack()

        self.f4 = Frame(self)
        self.f4.pack(pady=10)
        self.f5 = Frame(self)
        self.f5.pack()

        self.img = PhotoImage(file="run_all.gif")
        self.img2 = PhotoImage(file="run_step.gif")
        self.run_all = Button(self.f4, text="Run All", command=self.runAll,
            padx=5, image=self.img, compound="top")
        self.run_all.pack(side=LEFT)
        # self.run_step = Button(self.f4, text="Run Step",
        #     command=self.runStep, image=self.img2, compound="top")
        # self.run_step.pack(side=LEFT)

        self.img3 = PhotoImage(file="view_code.gif")
        self.img4 = PhotoImage(file="view_ml.gif")
        self.img5 = PhotoImage(file="new2.gif")
        self.img6 = PhotoImage(file="open2.gif")
        self.view_code = Button(self.f5, text="View Code",
            command=self.viewCode, padx=5, image=self.img3, compound="top")
        self.view_code.pack(side=LEFT)
        self.view_ml = Button(self.f5, text="Machine Code",
            command=self.viewML, padx=5, image=self.img4, compound="top")
        self.view_ml.pack(side=LEFT)
        self.new_btn = Button(self.f5, text="New", command=self.new, padx=5,
            image=self.img5, compound="top")
        self.new_btn.pack(side=LEFT)
        self.open_btn = Button(self.f5, text="Open", command=self.open,
            padx=5, image=self.img6, compound="top")
        self.open_btn.pack(side=LEFT)


    def initNewWindow(self):
        self.new_window = Tk()
        self.nw_frame = Frame(self.new_window)
        self.nw_frame.pack()
        self.txt = Text(self.nw_frame, width=50, height=20, padx=10, pady=10)


    def openFileToRead(self, title, fileToRead):
        self.initNewWindow()
        self.new_window.title(title)

        with open(fileToRead, 'rb') as t:
            for line in t:
                self.txt.insert(INSERT, line)

        self.txt.pack(padx=10, pady=10)
        self.new_window.mainloop()


    def viewCode(self):
        self.openFileToRead("View Code", "input.in")


    def viewML(self):
        self.openFileToRead("Machine Code", "output.out")

    def getInput(self):
        self.value = tkSimpleDialog.askinteger('Prompt', 'Enter a value: ')

    def runAll(self):
        # self.hideWidgets()
        self.computer.execute('output.out')
        self.run()
        self.text2.delete("1.0", END)
        print self.computer.stack
        if self.computer.stack:
            for item in self.computer.stack:
                self.text2.insert(INSERT, '[' + str(item) + ']\n')
        else:
            for x in range(0,5):
                self.text2.insert(END, '[' + str(x) + ']: Empty\n')

        self.text3.delete("1.0", END)
        for address in self.computer.address_space:
                self.text3.insert(INSERT, '[' + str(address) + ']\n')

    def runStep(self):
        self.hideWidgets()



root = Tk()
app = Assemboa(root)
root.mainloop()