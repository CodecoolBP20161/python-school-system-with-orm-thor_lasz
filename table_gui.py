from tkinter import *
from populator import Populator
from models import *


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
        Populator.establish_connection()
        Populator.populate_tables()

        table = Applicant.select().tuples()
        self.table_filler(table, f1, ["ID", "First name", "Last name", "Email", "City", "Application code", "School", "Interview", "Status"])
        table = City.select().tuples()
        self.table_filler(table, f2, ["ID", "City", "School city"])
        table = Mentor.select().tuples()
        self.table_filler(table, f3, ["ID", "First name", "Last name", "Email", "School"])
        table = InterviewSlot.select().tuples()
        self.table_filler(table, f4, ["ID", "Start", "End", "Reserved", "Mentor"])
        table = School.select().tuples()
        self.table_filler(table, f5, ["ID", "City"])

    def table_filler(self, table, parent, header):
        for column in range(len(header)):
            Label(parent, text=header[column]).grid(column=column, row=0)
        for row in range(len(table)):
            for column in range(len(table[row])):
                Label(parent, text=table[row][column], borderwidth=2, background="yellow").grid(
                    column=column, row=row + 1, sticky="e", padx=5, pady=2
                )

# rows = []
# for i in range(5):
#     cols = []
#     for j in range(4):
#         e = Entry(relief=RIDGE)
#         e.grid(row=i, column=j, sticky=NSEW)
#         e.insert(END, '%d.%d' % (i, j))
#         cols.append(e)
#     rows.append(cols)
#
# def onPress():
#     for row in rows:
#         for col in row:
#             print(col.get()),
#         print
#
# Button(text='Fetch', command=onPress).grid()
# mainloop()
#
#     def table_filler(self, table, parent, header):
#         for column in range(len(header)):
#             Label(parent, text=header[column]).grid(column=column, row=0)
#         for row in range(len(table)):
#             for column in range(len(table[row])):
#                 Label(parent, text=table[row][column], borderwidth=2, background="yellow").grid(
#                     column=column, row=row + 1, sticky="e", padx=5, pady=2
#                 )
