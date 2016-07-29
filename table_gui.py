from tkinter import *
from populator import Populator
from models import *


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
        sql_query_entry = Entry(parent, width=100).grid(column=1, row=0)
        peewee_query_entry = Entry(parent, width=100).grid(column=1, row=1)
        sql_query_submit = Button(parent, text='Submit', command=self.onPress).grid(column=2, row=0)
        peewee_query_submit = Button(parent, text='Submit', command=self.onPress).grid(column=2, row=1)

        frame = Frame(parent)
        frame.grid(row=2, column=0, columnspan=3, sticky=W+E+N+S)
        scrollbar = Scrollbar(frame)
        text = Text(frame)
        scrollbar.pack(side=RIGHT, fill=Y, )
        text.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)

        quote = """HAMLET: To be, or not to be--that is the question:
        Whether 'tis nobler in the mind to suffer
        The slings and arrows of outrageous fortune
        Or to take arms against a sea of troubles
        And by opposing end them. To die, to sleep--
        No more--and by a sleep to say we end
        The heartache, and the thousand natural shocks
        That flesh is heir to. 'Tis a consummation
        Devoutly to be wished."""
        text.insert(END, quote)

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
