'Customer table that connects with mysql.cc.puv.fi database and handles data efficiently'
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pymysql.cursors
import Pmw

class App(Frame):
 # GUI Database Query Frame
 try:
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
        self.button.add("Open DB",fg="green", command = self.open)
        self.button.add("Create Table", command= self.execute)
        self.button.add("Insert Data", command=self.insert)
        self.button.add("Modify Data", command=self.modify)
        self.button.add("Delete Data", command=self.delete)
        self.button.add("Search", command=self.search)
        self.button.add("Display All", command=self.list)
        self.button.add("Close DB",fg="red", command=self.close)

        # data entry field depends on the number of fields required

        label = Label(self, text= "CustomerID")  # label is the object of the class Label
        label.grid(row=1, column =0)
        self.a = Entry(self,name="CustomerID".lower(), font= "courier 12")
        self.a.grid(row=1, column=1, sticky = W + E + N + S, padx=5)# gird has to be specified(geometry manager)

        label = Label(self, text="Name")
        label.grid(row=2, column=0)
        self.b = Entry(self, name="Name".lower(), font="courier 12")
        self.b.grid(row=2, column=1, sticky=W + E + N + S, padx=5)

        label = Label(self, text="Address")
        label.grid(row=3, column=0)
        self.c = Entry(self, name="Address".lower(), font="courier 12")
        self.c.grid(row=3, column=1, sticky=W + E + N + S, padx=5)

        label = Label(self, text="Phone")
        label.grid(row=4, column=0)
        self.d = Entry(self, name="Phone".lower(), font="courier 12")
        self.d.grid(row=4, column=1, sticky=W + E + N + S, padx=5)


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

    def execute(self): #execute user-entered query against database
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Customer( Customer_id varchar(5) not null ,Name varchar(50), Address varchar(50), Phone varchar(25))")
    def close(self): # this method closes the database connection
        self.con.close()

    def insert(self):

        ID = self.a.get()  # gets all the entry from a and stores in variable
        NM = self.b.get()
        AD = self.c.get()
        PH = self.d.get()

        self.cur.execute("insert into Customer(Customer_id,Name, Address,Phone)values(%s,%s, %s, %s)",
                                 (ID,NM,AD,PH))

    def list(self):
        self.cur.execute('SELECT * FROM Customer')
        print(self.cur.fetchall())# Feteches all remaining rows of a query result , returning a list

    def delete(self):
                ID = self.a.get()
                self.cur = self.con.cursor()
                sql = "DELETE FROM Customer WHERE Customer_id = '%s'"%(ID)
                self.cur.execute(sql)
                self.con.commit()

    # here we modify the stored information based on the ID and all field are modified except the ID
    def modify(self):
        ID = self.a.get()
        NM = self.b.get()
        AD = self.c.get()
        PH = self.d.get()
        self.cur = self.con.cursor()
        sql = "UPDATE Customer SET Name = '%s',Address = '%s', Phone = '%s' WHERE  Customer_id = '%s'" % (NM,AD,PH,ID)
        self.cur.execute(sql)
        self.con.commit() # this method commits the current transaction
        # search is done based on the ID
    def search(self):
        ID = self.a.get()
        self.cur = self.con.cursor()
        sql = "SELECT * FROM Customer WHERE Customer_id = '%s'" % (ID)
        self.cur.execute(sql)
        print(self.cur.fetchall())# obtain user-requested information

 except Exception as e:
        print("Error :" + str(e))

root = Tk()
root.title("Customer Table")
app = App(root)
root.mainloop()
