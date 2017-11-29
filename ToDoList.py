# File: ToDoList.py
# Date: 2015-04-09
from tkinter.filedialog import *
from tkinter import messagebox
import pymysql
from datetime import date
from Task import *
from TaskComplete import *

class ToDoList:
    #initializes todays date and taskList list
    def __init__(self):
        self.taskList = list()
        self.today = date.today()

    #creates a new instace object of Task and stores the passes variables to it
    #appends the todoitem object to taskList array
	#CREATES a connection to the database
	#Creates an sql statement to insert a task in the task table
	#Executes the sql statement
	#Commits changes
	#closes off the connection
    def addTask(self, taskNameVar, descriptionVar, dateVar, priorityVar):
        self.todoitem = Task(taskNameVar, descriptionVar, priorityVar, dateVar, self.today)
        self.taskList.append(self.todoitem)

        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
        cur = conn.cursor()

        add_task = ("INSERT INTO task (TaskTitle, TaskDescription, TaskPriority, TaskDueDate, CreationDate) VALUES (%s, %s, %s, %s, %s)")
        task_data = (self.todoitem.TaskTitle, self.todoitem.TaskDescription, self.todoitem.TaskPriority, self.todoitem.TaskDueDate, self.todoitem.CreationDate)
        cur.execute(add_task, task_data)
        conn.commit()

        cur.close()
        conn.close()

    #creates a new instace object of Task and stores the passes variables to it
	#CREATES a connection to the database
	#Creates an sql statement to update a task in the task table
	#Executes the sql statement
	#Commits changes
	#closes off the connection
    #replaces the object in taskList with the newly created instance object
    def updateTask(self, tasktaskNameVar, descriptionVar, dateVar, priorityVar, whichSelected):
        try:
            self.todoitem = Task(tasktaskNameVar, descriptionVar, priorityVar, dateVar, self.today)

            conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
            cur = conn.cursor()
            update_task = "UPDATE task SET TaskTitle=%s, TaskDescription=%s, TaskPriority=%s, TaskDueDate=%s, CreationDate=%s WHERE TaskTitle=%s AND TaskDescription=%s AND TaskPriority=%s AND TaskDueDate=%s AND CreationDate=%s"
            task_data = (self.todoitem.TaskTitle, self.todoitem.TaskDescription, self.todoitem.TaskPriority, self.todoitem.TaskDueDate, self.todoitem.CreationDate,
                         self.taskList[whichSelected].TaskTitle, self.taskList[whichSelected].TaskDescription,
                         self.taskList[whichSelected].TaskPriority, self.taskList[whichSelected].TaskDueDate, self.taskList[whichSelected].CreationDate)
            cur.execute(update_task, task_data)

            conn.commit()

            cur.close()
            conn.close()

            self.taskList[whichSelected] = self.todoitem

        except ValueError:
            print("Please select an task to update")
        except TypeError:
            print("Type Error")

    #deletes the tasks at the index number in the array that has been passed in from ToDo
	#CREATES a connection to the database
	#Creates an sql statement to delete a task in the task table
	#Executes the sql statement
	#Commits changes
	#closes off the connection
    def deleteTask(self, whichSelected):
        try:
            del self.taskList[whichSelected]

            conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
            cur = conn.cursor()

            delete_task = "DELETE FROM task WHERE TaskTitle=%s AND TaskDescription=%s AND TaskPriority=%s AND TaskDueDate=%s AND CreationDate=%s"
            task_data = (self.taskList[whichSelected].TaskTitle, self.taskList[whichSelected].TaskDescription, self.taskList[whichSelected].TaskPriority, self.taskList[whichSelected].TaskDueDate, self.taskList[whichSelected].CreationDate)
            cur.execute(delete_task, task_data)

            conn.commit()

            cur.close()
            conn.close()
        except ValueError:
            print("Please select an task to delete")
        except TypeError:
            print()

    #CREATES a connection to the database
    #executes a select all to retrive all elements from the database
    #it then loops through each item and creates a todoitem and stores the values from the db row into it
    #it then adds the todoitem to the taskList array
    #connection are then closed
    def viewCompleteTasks(self):
        if len(self.taskList) != 0:
            self.saveDB()
        self.taskList = []
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
        cur = conn.cursor()
        cur.execute("SELECT * FROM taskcomplete")

        for task in cur:
            self.todoitem = TaskComplete(task[0],task[1],task[2],task[3],task[4], task[5])
            self.taskList.append(self.todoitem)
        cur.close()
        conn.close()

    #CREATES a connection to the database
    #Creates an sql statement to insert a task into the taskcomplete table
    #deletes the task from the task table
    #commits all changes
    #displays a message box saying a success
    #closes the connections
    #called the deleteTask() function to delete the completed task
    def markAsComplete(self, whichSelected):
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
        cur = conn.cursor()

        task = self.taskList[whichSelected]
        add_task = ("INSERT INTO taskcomplete (TaskTitle, TaskDescription, TaskPriority, TaskDueDate, CreationDate, IsComplete) VALUES (%s, %s, %s, %s, %s, %s)")
        task_data = (task.TaskTitle, task.TaskDescription, task.TaskPriority, task.TaskDueDate, task.CreationDate, 1)
        cur.execute(add_task, task_data)

        self.deleteTask(whichSelected)

        conn.commit()

        messagebox.showinfo("Success","Tasks have been marked as complete!")

        cur.close()
        conn.close()

    #CREATES a connection to the database
    #executes a select all to retrive all elements from the database
    #it then loops through each item and creates a todoitem and stores the values from the db row into it
    #it then adds the todoitem to the taskList array
    #connection are then closed
    def loadDB(self):
        self.taskList = []
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
        cur = conn.cursor()
        cur.execute("SELECT * FROM task")

        for task in cur:
            self.todoitem = Task(task[0],task[1],task[2],task[3],task[4])
            self.taskList.append(self.todoitem)
        cur.close()
        conn.close()

    #CREATES a connection to the database
    #messagebox asks the user if they can delete the entries in the database to prevent from duplicate copies
    #loops through taskList array and creates an insert statement to insert the object to the database
    #once loop is finished, it's commited
    #messagebox displays to show is was a sucess
    #closes the connections
    def saveDB(self):
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='todolist')
        cur = conn.cursor()

        if messagebox.askyesno("Delete Data", "Saving tasks to database will erase all tasks currently in the database, do you wish to continue?"):
            cur.execute("DELETE FROM task")

            for task in self.taskList:
                add_task = ("INSERT INTO task (TaskTitle, TaskDescription, TaskPriority, TaskDueDate, CreationDate) VALUES (%s, %s, %s, %s, %s)")
                task_data = (task.TaskTitle, task.TaskDescription, task.TaskPriority, task.TaskDueDate, task.CreationDate)
                cur.execute(add_task, task_data)
            conn.commit()
            messagebox.showinfo("Success","Tasks have been successfully added to the database!")
        cur.close()
        conn.close()

    #try
    #gets the file name and opens it
    #loop each line of the file
    #splits the line where a | appears and stores it in a array
    #new Task is created and the data from the line is stored inside of the object
    #the object is then added to the array
    #closes the file
    def loadFile(self):
        try:
            self.taskList = []
            filename = askopenfilename(filetypes=[('text files', '.txt')])
            list = open(filename)

            for task in list:
                task = task.split("|")
                self.todoitem = Task(task[0],task[1], task[2], task[3], task[4])
                self.taskList.append(self.todoitem)
            list.close()
        except ValueError:
            print("Please load correct file.")
        except TypeError:
            print()

    #opens a tkinter file save windowdow
    #if the user tried to save without entering a filetaskName the windowdow will close and nothing will be saved.
    #loops through each item in the taskList and writes it to a txt file, each item goes on to a new line
    #the file is then closed
    def saveFile(self):
        try:
            filetaskname = asksaveasfile(mode='w', defaultextension=".txt", filetypes=[('text files', '.txt')])
            if filetaskname is None:
                return
            for item in self.taskList:
                filetaskname.write("%s\n" % item)
            filetaskname.close()
        except:
            print()

    #creates a new list used as a dummy list
    #calls an iterator object and iterates through the taskList sorting it by TaskTitle and then stores it into the dummy list
    #dummy list gets stored into taskList
    def sortTasks(self):
        self.sortedList = list()
        self.sortedList = sorted(self.taskList, key=lambda Task: Task.TaskTitle)
        self.taskList = self.sortedList