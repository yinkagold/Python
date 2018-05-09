'Order table that connects with mysql.cc.puv.fi database and handles data efficiently'
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pymysql.cursors
import Pmw
import time
import datetime
time.strftime('%Y-%m-%m %H:%M:%S')

class App(Frame):

    def __init__(self, master):
        # QueryWindow COnstructor
        # init method will always run when the class is called ( in the method are things you want loaded by default)
        Frame.__init__(self)
        Pmw._initialise()
        self.pack(expand=YES, fill=BOTH)
        frame = tk.Frame(master)
        frame.pack()
        self.button = Pmw.ButtonBox(self, padx =0)
        self.button.grid(columnspan = 2)
        self.button.add("Open DB", fg="green", command = self.open)
        self.button.add("Create Table", command= self.execute)
        self.button.add("Insert Data", command=self.insert)
        self.button.add("Modify Data", command=self.modify)
        self.button.add("Delete Data", command=self.delete)
        self.button.add("Search", command=self.search)
        self.button.add("Display All", command=self.list)
        self.button.add("Close DB",fg="red", command=self.close)

        # data entry field depends on the number of fields required

        label = Label(self, text= "Order Date")  # label is the object of the class Label
        label.grid(row=1, column =0)
        self.a = Entry(self,name="Order Date".lower(), font= "courier 12")
        self.a.grid(row=1, column=1, sticky = W + E + N + S, padx=5)  # gird has to be specified(geometry manager)

        label = Label(self, text="CustomerID")
        label.grid(row=2, column=0)
        self.b = Entry(self, name="CustomerID".lower(), font="courier 12")
        self.b.grid(row=2, column=1, sticky=W + E + N + S, padx=5)

        label = Label(self, text="ProductID")
        label.grid(row=3, column=0)
        self.c = Entry(self, name="ProductID".lower(), font="courier 12")
        self.c.grid(row=3, column=1, sticky=W + E + N + S, padx=5)

        label = Label(self,text="Product Amount")
        label.grid(row=4, column=0)
        self.d = Entry(self, name="Product Amount".lower(), font="courier 12")
        self.d.grid(row=4, column=1, sticky=W + E + N + S, padx=5)

    try:
        def open(self):
            # open connection, retrieve cursor and execute query
            self.con = pymysql.connect(host='mysql.cc.puv.fi',
                                    user='username',
                                    password='password',
                                    db='dbname',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor
                                     )  # here pymysql connects to the db and return to con
            self.cur = self.con.cursor()  # data sets when working with the db will be assigned to the cur

        def execute(self):#execute user-entered query against database
            self.cur = self.con.cursor()
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS Orders(Order_Date date ,Customer_id varchar(5) not null,Product_id varchar(5), Product_Amount double)")

        def close(self): # this method closes the database connection
            self.con.close()

        def insert(self):

            DT = self.a.get()  # gets all the entry from a and stores in variable
            CID = self.b.get()
            PID = self.c.get()
            PA = self.d.get()

            self.cur.execute("insert into Orders(Order_Date,Customer_id, Product_id,Product_Amount)values(%s,%s, %s, %s)",
                                     (DT,CID,PID,PA))

        def list(self):
            self.cur.execute('SELECT * FROM Orders')
            print(self.cur.fetchall())# Feteches all remaining rows of a query result , returning a list


        def delete(self):
                    CID = self.a.get()
                    self.cur = self.con.cursor()
                    sql = "DELETE FROM Orders WHERE Customer_id = '%s'"%(CID)
                    self.cur.execute(sql)
                    self.con.commit()

        def modify(self):
            DT = self.a.get()
            CID = self.b.get()
            PID = self.c.get()
            PA = self.d.get()
            self.cur = self.con.cursor()
            sql = "UPDATE Orders SET Order_Date = '%s',Product_id = '%s', Product_Amount = '%s' WHERE  Customer_id = '%s'" % (DT,PID,PA,CID)
            self.cur.execute(sql)
            self.con.commit() # this method commits the current transaction
        # search is done based on the ID
        def search(self):
            CID = self.b.get()
            self.cur = self.con.cursor()
            sql = "SELECT * FROM Orders WHERE Customer_id = '%s'" % (CID)
            self.cur.execute(sql)
            print(self.cur.fetchall()) # obtain user-requested information

    except Exception as e:
     print("There was an exception" + str(e))

root = Tk()
root.title("Order Table")
app = App(root)
root.mainloop()
