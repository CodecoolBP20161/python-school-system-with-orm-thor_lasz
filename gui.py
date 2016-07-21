from tkinter import *
import populator
from models import *
from stories import *
from tabulate import tabulate
from tkinter.ttk import *
from tkinter import ttk

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        self.logo = PhotoImage(file='./logo.gif')
        master.geometry("400x400")
        master.title("Rubik's cube")
        self.frame = Frame(master)
        self.main_menu()

    def main_menu(self):
        self.frame.destroy()
        self.frame = Frame(self.master)
        self.frame.place(x=0, y=0, width=500, height=455)
        self.canvas = Canvas(self.frame, bg='white', width=500, height=455)
        self.canvas.pack()
        self.canvas.create_image(280, 0, anchor=NE, image=self.logo)

        self.admin_button = Button(self.canvas, text="Administrator", command=lambda: self.admin_menu())
        self.admin_button.place(x=150, y=200, width=100, height=25)
        self.applicant_button = Button(self.canvas, text="Applicant", command=lambda: self.applicant_menu())
        self.applicant_button.place(x=150, y=230, width=100, height=25)
        self.mentor_button = Button(self.canvas, text="Mentor", command=lambda: self.mentor_menu())
        self.mentor_button.place(x=150, y=260, width=100, height=25)
        self.tables_button = Button(self.canvas, text="Show tables", command=self.show_tables)
        self.tables_button.place(x=150, y=290, width=100, height=25)
        self.close_button = Button(self.canvas, text="Close", command=self.master.quit)
        self.close_button.place(x=150, y=320, width=100, height=25)
        self.canvas.delete('all')

    def admin_menu(self):
        self.frame.destroy()
        self.frame = Frame(self.master)
        self.frame.place(x=0, y=0, width=500, height=455)
        self.canvas = Canvas(self.frame, bg='white', width=500, height=455)
        self.canvas.pack()
        self.canvas.create_image(280, 0, anchor=NE, image=self.logo)
        self.admin_button = Button(self.canvas, text="Story 1: Handle new applications", command=lambda: self.admin_menu())
        self.admin_button.place(x=75, y=200, width=250, height=25)
        self.applicant_button = Button(self.canvas, text="Story 2: Assign interview slot to applicants", command=lambda: self.applicant_menu())
        self.applicant_button.place(x=75, y=230, width=250, height=25)
        self.mentor_button = Button(self.canvas, text="Story 6: Application detail", command=lambda: self.mentor_menu())
        self.mentor_button.place(x=75, y=260, width=250, height=25)
        self.close_button = Button(self.canvas, text="Back", command=lambda: self.main_menu())
        self.close_button.place(x=75, y=320, width=250, height=25)


    def applicant_menu(self):
        self.frame.destroy()
        self.frame = Frame(self.master)
        self.frame.place(x=0, y=0, width=500, height=455)
        self.canvas = Canvas(self.frame, bg='white', width=500, height=455)
        self.canvas.pack()
        self.canvas.create_image(280, 0, anchor=NE, image=self.logo)
        self.admin_button = Button(self.canvas, text="Application details (story 3)",
                                   command=lambda: self.admin_menu())
        self.admin_button.place(x=75, y=200, width=250, height=25)
        self.applicant_button = Button(self.canvas, text="Interview details (story 4)",
                                       command=lambda: self.applicant_menu())
        self.applicant_button.place(x=75, y=230, width=250, height=25)
        self.close_button = Button(self.canvas, text="Back", command=lambda: self.main_menu())
        self.close_button.place(x=75, y=320, width=250, height=25)

    def mentor_menu(self):
        self.frame.destroy()
        self.frame = Frame(self.master)
        self.frame.place(x=0, y=0, width=500, height=455)
        self.canvas = Canvas(self.frame, bg='white', width=500, height=455)
        self.canvas.pack()
        self.canvas.create_image(280, 0, anchor=NE, image=self.logo)
        self.close_button = Button(self.canvas, text="Back", command=lambda: self.main_menu())
        self.close_button.place(x=75, y=320, width=250, height=25)


    def show_tables(self):
        self.top = Toplevel(self.master)
        self.table_window = TableWindow(self.top)

class TableWindow():
    def __init__(self, master):
        self.master = master
        n = ttk.Notebook(self.master)
        f1 = ttk.Frame(n)   # first page, which would get widgets gridded into it
        f2 = ttk.Frame(n)   # second page
        f3 = ttk.Frame(n)   # second page
        f4 = ttk.Frame(n)   # second page
        f5 = ttk.Frame(n)   # second page
        n.add(f1, text='Applicant')
        n.add(f2, text='City')
        n.add(f3, text='Mentor')
        n.add(f4, text='InterviewSlot')
        n.add(f5, text='School')

        n.pack()
        populator.establish_connection()
        populator.populate_tables()

        table = Applicant.select().tuples()
        self.table_filler(table, f1)
        table = City.select().tuples()
        self.table_filler(table, f2)
        table = Mentor.select().tuples()
        self.table_filler(table, f3)
        table = InterviewSlot.select().tuples()
        self.table_filler(table, f4)
        table = School.select().tuples()
        self.table_filler(table, f5)


    def table_filler(self, table, parent):
        for row in range(len(table)):
            for column in range(len(table[row])):
                Label(parent, text=table[row][column]).grid(column=column, row=row)




root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
        #
        # table = (Applicant.select(
        #                                     Applicant.first_name,
        #                                     Applicant.last_name,
        #                                     Applicant.email,
        #                                     Applicant.city
        #                                 ).tuples())
