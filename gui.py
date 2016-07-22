from tkinter import *
import populator
from models import *
from tabulate import tabulate
from tkinter.ttk import *
from tkinter import ttk
from gui_stories import *

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        self.logo = PhotoImage(file='./logo.gif')
        master.geometry("400x400")
        master.title("Application system")
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
        self.admin_button = Button(self.canvas, text="Handle new applications (story 1)", command=lambda: self.first())
        self.admin_button.place(x=75, y=200, width=250, height=25)
        self.applicant_button = Button(self.canvas, text="Assign interview slot to applicants (story 2)", command=lambda: self.second())
        self.applicant_button.place(x=75, y=230, width=250, height=25)
        self.mentor_button = Button(self.canvas, text="Application detail (story 6)", command=lambda: self.sixth())
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
                                   command=lambda: self.third())
        self.admin_button.place(x=75, y=200, width=250, height=25)
        self.applicant_button = Button(self.canvas, text="Interview details (story 4)",
                                       command=lambda: self.fourth())
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


    def first(self):
        self.top = Toplevel(self.master)
        self.first_window = FirstWindow(self.top)

    def second(self):
        self.top = Toplevel(self.master)
        self.second_window = SecondWindow(self.top)

    def third(self):
        self.top = Toplevel(self.master)
        self.third_window = ThirdWindow(self.top)

    def fourth(self):
        self.top = Toplevel(self.master)
        self.fourth_window = FourthWindow(self.top)


    def show_tables(self):
        self.top = Toplevel(self.master)
        self.table_window = TableWindow(self.top)

class FirstWindow():
    def __init__(self, master):
        self.master = master
        master.geometry("700x400")
        master.title("First user story")
        populator.establish_connection()
        populator.populate_tables()
        self.head = Canvas(self.master, width=700, height=60)
        self.head.place(x=0, y=0)
        self.head.create_text(350, 15, text="Here you can automate the process of incoming applications.")
        self.head.create_text(350, 40, text="These are the applicants without an assigned id or school in the database:")
        self.upperside = Canvas(self.master, width=700, height=240)
        self.upperside.place(x=0, y=61)

        table = FirstStory.new_applicants(self)
        TableWindow.table_filler(self, table, self.upperside,
                                 ["ID", "First name", "Last name", "Email", "City"])
        self.downside = Canvas(self.master, width=700, height=100)
        self.downside.place(x=0, y=300)
        self.update_button = Button(self.downside, text="Create ID", command=lambda: self.update_id())
        self.update_button.place(x=245, y=30, width=100, height=25)
        # self.close_button = Button(self.downside, text="Close", command=self.master.quit)
        # self.close_button.place(x=355, y=30, width=100, height=25)

    def update_id(self):
        self.head.destroy()
        self.upperside.destroy()
        #self.update_button.destroy()
        self.downside.destroy()
        self.downside = Canvas(self.master, width=700, height=150)
        self.downside.place(x=0, y=250)
        self.head = Canvas(self.master, width=700, height=80)
        self.head.place(x=0, y=0)
        self.head.create_text(350, 40, text="Updated application informations:")

        self.upperside = Canvas(self.master, width=500, height=170)
        self.upperside.place(x=120, y=81)
        table = FirstStory.create_id(self)
        TableWindow.table_filler(self, table, self.upperside,
                                 ["First name", "Last name", "Application code", "School city"])
        # self.close_button = Button(self.downside, text="Close table", command=lambda: self.first_window.destroy())
        # self.close_button.place(x=245, y=30, width=100, height=25)


class SecondWindow():
    def __init__(self, master):
        self.master = master
        master.geometry("700x400")
        master.title("Second user story")
        self.head = Canvas(self.master, width=700, height=60)
        self.head.place(x=0, y=0)
        self.head.create_text(350, 15, text="Here you can assign interview slots to applicants.")
        self.head.create_text(350, 40,
                              text="These are the applicants without interview in the database:")
        self.upperside = Canvas(self.master, width=700, height=240)
        self.upperside.place(x=0, y=61)

        table = SecondStory.new_applicants(self)
        TableWindow.table_filler(self, table, self.upperside,
                                 ["ID", "First name", "Last name", "Email", "City"])
        self.downside = Canvas(self.master, width=700, height=100)
        self.downside.place(x=0, y=300)
        self.update_button = Button(self.downside, text="Create interview slot", command=lambda: self.update_iw())
        self.update_button.place(x=245, y=30, width=100, height=25)
        # self.close_button = Button(self.downside, text="Close", command=self.master.quit)
        # self.close_button.place(x=355, y=30, width=100, height=25)

    def update_iw(self):
        self.head.destroy()
        self.upperside.destroy()
        # self.update_button.destroy()
        self.downside.destroy()
        self.downside = Canvas(self.master, width=700, height=100)
        self.downside.place(x=0, y=300)
        self.head = Canvas(self.master, width=700, height=80)
        self.head.place(x=0, y=0)
        self.head.create_text(350, 40, text="Updated application informations:")

        self.upperside = Canvas(self.master, width=500, height=220)
        self.upperside.place(x=120, y=81)
        table = SecondStory.add_interview(self)
        TableWindow.table_filler(self, table, self.upperside, ["ID", "First name", "Last name", "Email", "City", "Application code", "School", "Interview", "Status"])

class ThirdWindow():
    def __init__(self, master):
        self.master = master
        master.geometry("500x500")
        master.title("First user story")
        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.place(x=0, y=0)
        self.app_id = Entry(self.canvas, width= 10)
        self.app_id.place(x=240, y=300)
        self.canvas.create_text(150, 310, text="Enter your application code")
        self.search_button = Button(self.canvas, text="Seach", command=lambda: self.search())
        self.search_button.place(x=200, y=360, width=100, height=25)

    def search(self):
        id = self.app_id.get()
        print (id)
        self.canvas.destroy()
        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.place(x=0, y=0)
        table = ThirdStory.search(self, id)
        print (table)
        TableWindow.table_filler(self, table, self.canvas,
                                 [""])

class FourthWindow():
    def __init__(self, master):
        self.master = master
        master.geometry("500x500")
        master.title("First user story")
        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.place(x=0, y=0)
        self.app_id = Entry(self.canvas, width= 10)
        self.app_id.place(x=240, y=300)
        self.canvas.create_text(150, 310, text="Enter your application code")
        self.search_button = Button(self.canvas, text="Seach", command=lambda: self.search())
        self.search_button.place(x=200, y=360, width=100, height=25)

    def search(self):
        id = self.app_id.get()
        print (id)
        self.canvas.destroy()
        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.place(x=0, y=0)
        table = FourthStory.search(self, id)
        TableWindow.table_filler(self, table, self.canvas,
                                 [""])

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
        self.table_filler(table, f1, ["ID", "First name", "Last name", "Email", "City", "Application code", "School", "Interview", "Status"])
        table = City.select().tuples()
        self.table_filler(table, f2, ["ID", "City", "School city"])
        table = Mentor.select().tuples()
        self.table_filler(table, f3, ["ID", "First name", "Last name", "Email", "School"])
        table = InterviewSlot.select().tuples()
        self.table_filler(table, f4, ["ID", "Start", "End", "Reserved", "Mentor"])
        table = School.select().tuples()
        self.table_filler(table, f5 ["ID", "City"])

    def table_filler(self, table, parent, header):
        for column in range(len(header)):
            Label(parent, text=header[column]).grid(column=column, row=0)
        for row in range(len(table)):
            for column in range(len(table[row])):
                Label(parent, text=table[row][column], borderwidth=2, background="yellow").grid(
                    column=column, row=row + 1, sticky="e", padx=5, pady=2
                )




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
