from tkinter import *
from populator import Populator
from models import *


class TableWindow():
    def __init__(self, master):
        self.master = master
        n = ttk.Notebook(self.master)
        table_names = ["Applicant", "City", "Mentor", "InterviewSlot", "School"]
        tables = []

        for table in table_names:
            tables.append(ttk.Frame(n))
            n.add(tables[-1], text=table)
        n.pack()

        table = Applicant.select().tuples()
        self.table_filler(table, tables[0], Applicant._meta.sorted_field_names)
        table = City.select().tuples()
        self.table_filler(table, tables[1], City._meta.sorted_field_names)
        table = Mentor.select().tuples()
        self.table_filler(table, tables[2], Mentor._meta.sorted_field_names)
        table = InterviewSlot.select().tuples()
        self.table_filler(table, tables[3], InterviewSlot._meta.sorted_field_names)
        table = School.select().tuples()
        self.table_filler(table, tables[4], School._meta.sorted_field_names)

    def table_filler(self, table, parent, header):

        maximum_lengths = [max(len(str(value)) for value in column) for column in zip(*table)]
        maximum_lengths = [value if value > 6 else 6 for value in maximum_lengths]
        self.rows = []
        for column in range(len(table[0])):
            e = Entry(parent, width=maximum_lengths[column]+2)
            e.insert(END, header[column])
            e.grid(column=column, row=0)

        for row in range(len(table)):
            self.cols = []
            for column in range(len(table[row])):
                e = Entry(parent, width=maximum_lengths[column]+2)
                e.grid(column=column, row=row+1)
                e.insert(END, str(table[row][column]))
                self.cols.append(e)
            self.rows.append(self.cols)
        Button(parent, text='Fetch', command=self.onPress).grid()

    def onPress(self):
        for row in self.rows:
            for col in row:
                print(col.get()),
            print
