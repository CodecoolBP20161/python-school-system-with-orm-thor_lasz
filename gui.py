from tkinter import Tk, Label, Button
from tkinter import *
import populator
from models import *
from stories import *
from tabulate import tabulate


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        self.logo = PhotoImage(file='./logo.gif')
        master.geometry("400x400")
        master.title("Rubik's cube")
        frame = Frame(master)
        frame.place(x=0, y=0, width=500, height=455)
        self.canvas = Canvas(frame, bg='white', width=500, height=455)
        self.canvas.pack()
        self.canvas.create_image(280, 0, anchor=NE, image=self.logo)

        self.admin_button = Button(self.canvas, text="Administrator", command=lambda: self.adminmenu())
        self.admin_button.place(x=150, y=200, width=100, height=25)
        self.applicant_button = Button(self.canvas, text="Applicant", command=lambda: self.applicantmenu())
        self.applicant_button.place(x=150, y=230, width=100, height=25)
        self.mentor_button = Button(self.canvas, text="Mentor", command=lambda: self.mentormenu())
        self.mentor_button.place(x=150, y=260, width=100, height=25)
        self.tables_button = Button(self.canvas, text="Show tables", command=self.show_tables)
        self.tables_button.place(x=150, y=290, width=100, height=25)
        self.close_button = Button(self.canvas, text="Close", command=master.quit)
        self.close_button.place(x=150, y=320, width=100, height=25)

    def show_tables(self):
        self.top = Toplevel(self.master)
        self.table_window = TableWindow(self.top)


class TableWindow():
    def __init__(self, master):
        self.master = master

        populator.establish_connection()
        populator.populate_tables()
        table = (Applicant.select(
                                            Applicant.first_name,
                                            Applicant.last_name,
                                            Applicant.email,
                                            Applicant.city
                                        ).tuples())
        for row in range(len(table)):
            for column in range(len(table[row])):
                Label(self.master, text=table[row][column]).grid(column=column, row=row)


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
