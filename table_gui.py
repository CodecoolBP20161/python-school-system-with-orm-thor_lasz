from tkinter import *
from populator import Populator
from models import *
from tabulate import tabulate


class TableWindow():
    """ Handles the creation of the database tables in the gui and its methods. """

    def __init__(self, master):
        self.master = master
        n = ttk.Notebook(self.master)
        table_names = ["Applicant", "City", "Mentor", "InterviewSlot", "School"]
        tables = []

        for table in table_names:
            tables.append(ttk.Frame(n))
            n.add(tables[-1], text=table)
        tables.append(ttk.Frame(n))
        n.add(tables[-1], text="Query")
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
        self.build_query_page(tables[5])

    def build_query_page(self, parent):
        sql_query_label = Label(parent, text="SQL query: ").grid(column=0, row=0)
        peewee_query_label = Label(parent, text="Peewee query: ").grid(column=0, row=1)
        self.sql_query_entry = Entry(parent, width=100)
        self.sql_query_entry.grid(column=1, row=0)
        self.peewee_query_entry = Entry(parent, width=100)
        self.peewee_query_entry.grid(column=1, row=1)
        sql_query_submit = Button(parent, text='Submit', command=self.send_sql_query).grid(column=2, row=0)
        peewee_query_submit = Button(parent, text='Submit', command=self.onPress).grid(column=2, row=1)

        frame = Frame(parent)
        frame.grid(row=2, column=0, columnspan=3, sticky=W+E+N+S)
        scrollbary = Scrollbar(frame)
        scrollbarx = Scrollbar(frame)
        self.text = Text(frame, wrap=NONE)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.pack(side=BOTTOM, fill=X)
        self.text.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbary.config(command=self.text.yview)
        scrollbarx.config(orient=HORIZONTAL, command=self.text.xview)
        self.text.config(yscrollcommand=scrollbary.set)
        self.text.config(xscrollcommand=scrollbarx.set)
        self.text.config(state=DISABLED)

    def send_sql_query(self):
        message = self.sql_query_entry.get()
        # print(message.split()[-1]._meta.sorted_field_names)
        # get all tables és a listából ami megfelel neki az utolsó szó alapján
        # select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='applicant'
        headers = Populator.run_sql("select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='applicant'")
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(END, tabulate(Populator.run_sql(message), headers=headers))
        self.text.config(state=DISABLED)

    def table_filler(self, table, parent, header):
        """ Prints the header and table contents on its parent in a grid. """
        maximum_lengths = [max(len(str(value)) for value in column) for column in zip(*table)]
        maximum_lengths = [value if value > 4 else 4 for value in maximum_lengths]
        header_lengths = [len(column_name) for column_name in header]
        maximum_lengths = [item1 if item1 > item2 else item2 for item1, item2 in zip(maximum_lengths, header_lengths)]

        self.rows = []
        for column in range(len(table[0])):
            e = Label(parent, text=header[column], width=maximum_lengths[column]+2)
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
