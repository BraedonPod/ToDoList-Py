# File: ToDo.py
# Date: 2015-04-09
from ToDoList import *

class ToDo:
    #Used to store the index number of a selected item
    selectedItem = ""
    #This method makes and returns the tkinter GUI window
    #starts off by creating the main menu
    #ListBox where tasks will be displayed
    #The inputs, labels and Entry boxes to the user can enter information for the tasks
    #The buttons are made last
    def makeWindow(self):
        #global variables used to store and hold input of tasks
        global taskNameVar, descriptionVar, priorityVar, dateVar, select
        #button variables
        global b1, b2, b3, b4

        self.todolist = ToDoList()
        window = Tk()
        window.geometry("300x240")#set size
        window.title("Task Manager")#set title for application

        #Main Menu start
        menubar = Menu(window)
        window.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open from Database", command=self.loadDB)
        fileMenu.add_command(label="Save to Database", command=self.saveDB)
        fileMenu.add_separator()
        fileMenu.add_command(label="Open from File", command=self.loadFile)
        fileMenu.add_command(label="Save to File", command=self.saveFile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=window.destroy)
        menubar.add_cascade(label="File", menu=fileMenu)
        viewMenu = Menu(menubar)
        viewMenu.add_command(label="View Completed Tasks", command=self.viewCompleteTasks)
        viewMenu.add_command(label="View Current Tasks", command=self.viewCurrentTasks)
        menubar.add_cascade(label="View", menu=viewMenu)

        #Main Menu End

        #List View Start
        listFrame = Frame(window)
        listFrame.pack()
        scroll = Scrollbar(listFrame, orient=VERTICAL)
        select = Listbox(listFrame, yscrollcommand=scroll.set, height=6, width=40)
        #select.bind('<ButtonRelease-1>', self.viewWindow)
        select.bind('<Double-1>', self.viewWindow)
        scroll.config (command=select.yview)
        scroll.pack(side=RIGHT, fill=Y)
        select.pack(side=LEFT,  fill=BOTH, expand=1)
        #List View End

        #Input Start
        #task input start
        inputFrame = Frame(window)
        inputFrame.pack()
        Label(inputFrame, text="Task Name").grid(row=0, column=0, sticky=W+S+N+E)
        taskNameVar = StringVar()
        taskName = Entry(inputFrame, textvariable=taskNameVar)
        taskName.grid(row=1, column=0, sticky=W+S+N+E, padx=5)
        #task input end

        #description input start
        Label(inputFrame, text="Description").grid(row=2, column=0, sticky=W+S+N+E)
        descriptionVar= StringVar()
        desc= Entry(inputFrame, textvariable=descriptionVar)
        desc.grid(row=3, column=0, sticky=W+S+N+E, padx=5)
        #description input end

        #date input start
        Label(inputFrame, text="Due Date(YYYY-MM-DD)").grid(row=0, column=1, sticky=W+S+N+E)
        dateVar= StringVar()
        date= Entry(inputFrame, textvariable=dateVar)
        date.grid(row=1, column=1, sticky=W+S+N+E, padx=5)
        #date input end

        #priority input start
        Label(inputFrame, text="Priority").grid(row=2, column=1, sticky=W+S+N+E)
        priorityVar= StringVar()
        priorityVar.set('')#default option
        priority= OptionMenu(inputFrame, priorityVar, 'low', 'medium', 'high')
        priority.grid(row=3, column=1, sticky=W+S+N+E, padx=5)
        #priority input end
        #Input End

        #Button Start
        buttonFrame = Frame(window)
        buttonFrame.pack()
        b1 = Button(buttonFrame,text=" Add  ",command=self.addTask)
        b2 = Button(buttonFrame,text="Mark Complete",command=self.markAsComplete)
        b3 = Button(buttonFrame,text="Update",command=self.updateTask)
        b4 = Button(buttonFrame,text="Delete",command=self.deleteTask)
        b1.pack(side=LEFT, padx=5, pady=5); b2.pack(side=LEFT, padx=5, pady=5)
        b3.pack(side=LEFT, padx=5, pady=5); b4.pack(side=LEFT, padx=5, pady=5)
        #Button End
        self.addState()
        return window


    #calls the markAsComplete function insideof todolist
    #calls setSelect() function
    #calls clearInput() function
    def markAsComplete(self):
        try:
            self.todolist.markAsComplete(self.whichSelected())
            self.setSelect()
            self.clearInput()
        except:
           print()

    #Checks to make sure that there are actually items in the listbox
    #gets the selected item from taskList and stores it into a object variable
    #checks to see if it's in the complete or normal state
    #Normal state allows the item to be edited
    #Complete state doesnt allow item to be edited
    def viewWindow(self, event):
        if len(self.todolist.taskList) != 0:
            item = self.todolist.taskList[self.whichSelected()]

            if b1['state'] == DISABLED and b2['state'] == DISABLED and b3['state'] == DISABLED and b4['state'] == DISABLED:
                message = "Title: %s \nDescription: %s \nPriority: %s \nDue Date: %s \nCreation Date: %s" % (str(item.TaskTitle), str(item.TaskDescription), str(item.TaskPriority), str(item.TaskDueDate), str(item.CreationDate))
                messagebox.showinfo("Task View", message)
            else:
                message = "Title: %s \nDescription: %s \nPriority: %s \nDue Date: %s \nCreation Date: %s \n\nWould you like to edit the task?" % (str(item.TaskTitle), str(item.TaskDescription), str(item.TaskPriority), str(item.TaskDueDate), str(item.CreationDate))
                if messagebox.askyesno("Task View", message):
                    self.editTask()

    #Calls the loadDB function
    #Calls setSelect()
    #sets state to normal
    def viewCurrentTasks(self):
        self.loadDB()
        self.setSelect()
        self.normalState()


    #Calls viewCompleteTasks() in todolist
    #Calls setSelect()
    #sets state to complete
    def viewCompleteTasks(self):
        self.todolist.viewCompleteTasks()
        self.setSelect()
        self.completeState()

    #Checks to see if all input have data in it, if missing data a messagebox will appear
    #calls the addTask function in todolist(ToDoList) and passes values to it
    #calls the setSelect() function
    #calls the clearInput() function
    #sets program state to normal
    def addTask(self):
        if taskNameVar.get() == "" or descriptionVar.get() == "" or dateVar.get() == "" or priorityVar.get() == "":
            messagebox.showwarning("Invalid Input", "Please fill in every output")
        else:
            self.todolist.addTask(taskNameVar.get(), descriptionVar.get(), dateVar.get(), priorityVar.get())
            self.setSelect()
            self.clearInput()
            self.normalState()

    #Checks to see if all input have data in it, if missing data a messagebox will appear
    #calls the updateTask function in todolist(ToDoList) and passes values to it
    #calls the setSelect() function
    #calls the clearInput() function
    #sets program state to normal
    def updateTask(self):
        if taskNameVar.get() == "" or descriptionVar.get() == "" or dateVar.get() == "" or priorityVar.get() == "":
            messagebox.showwarning("Invalid Input", "Please fill in every output")
        else:
            #self.todolist.updateTask(taskNameVar.get(), descriptionVar.get(), dateVar.get(), priorityVar.get(), self.whichSelected())
            self.todolist.updateTask(taskNameVar.get(), descriptionVar.get(), dateVar.get(), priorityVar.get(), self.selectedItem)
            self.setSelect()
            self.clearInput()
            self.normalState()
            self.selectedItem = ""

    #Messagebox asks the user if they are sure they want to delete a task
    #if yes, calls the deleteTask function in todolist(ToDoList) and passes values to it
    #calls the setSelect() function
    #calls the clearInput() function
    def deleteTask(self):
        try:
            if messagebox.askyesno("Delete Task", "Are you sure you want to delete the selected task?"):
                self.todolist.deleteTask(self.whichSelected())
            self.setSelect()
            self.clearInput()
            if len(self.todolist.taskList) == 0:
                self.addState()
        except:
            messagebox.showerror("Delete Error", "Please select an item to delete")

    #stores it item retried from taskList at the selected index number in todolist(ToDoList) and stores it into item
    #the data from the item is then set into the input boxes entities
    #and it then set to the input textvariables
    #calls setSelect() function
    #sets the program state to edit
    def editTask(self):
        try:
            self.selectedItem = self.whichSelected()
            item = self.todolist.taskList[self.whichSelected()]
            taskName = item.TaskTitle
            priority = item.TaskPriority
            date = item.TaskDueDate
            desc = item.TaskDescription
            taskNameVar.set(taskName)
            priorityVar.set(priority)
            dateVar.set(date)
            descriptionVar.set(desc)
        except:
            print()
        self.setSelect()
        self.editState()

    #calls the function saveFile() in todolist(ToDoList)
    #calls setSelect() function
    #sets the program state to normal
    def loadDB(self):
        self.todolist.loadDB()
        self.setSelect()
        self.normalState()

    #calls the function saveDB() in todolist(ToDoList)
    def saveDB(self):
        self.todolist.saveDB()

    #calls the function loadFile() in todolist(ToDoList)
    #calls setSelect() function
    #sets the program state to normal
    def loadFile(self):
        self.todolist.loadFile()
        self.setSelect()
        self.normalState()

    #calls the function saveFile() in todolist(ToDoList)
    def saveFile(self):
        self.todolist.saveFile()

    #Clears the listbox so duplicated or older data are gone
    #loops through the todolist.taskList array and insers the TaskTitle to the listbox
    def setSelect(self):
        select.delete(0, END)
        self.todolist.sortTasks()
        for item in self.todolist.taskList:
            select.insert(END, item.TaskTitle)

    #When a user picks a task to edit it displays which task they have selected out of the list to console
    #sample: pick task 2 out of 5 tasks, "Selected 2 of 5"
    def whichSelected(self):
        try:
            return int(select.curselection()[0])
        except:
            print("")

    #This method clears the input of each of the input boxes
    def clearInput(self):
        taskNameVar.set("")
        descriptionVar.set("")
        priorityVar.set("")
        dateVar.set("")

    #The following functions act as a way to have the program in different states
    #The add state is activated when the program is started up
    def addState(self):
        b1.config(state=NORMAL)
        b2.config(state=DISABLED)
        b3.config(state=DISABLED)
        b4.config(state=DISABLED)
    #The edit state is activated when the user presses the edit button on the GUI
    def editState(self):
        b1.config(state=DISABLED)
        b2.config(state=DISABLED)
        b3.config(state=NORMAL)
        b4.config(state=NORMAL)
    #The normal state is activated when the user has a task added and the user is not adding or editing an item
    def normalState(self):
        b1.config(state=NORMAL)
        b2.config(state=NORMAL)
        b3.config(state=NORMAL)
        b4.config(state=NORMAL)
    def completeState(self):
        b1.config(state=DISABLED)
        b2.config(state=DISABLED)
        b3.config(state=DISABLED)
        b4.config(state=DISABLED)

#Program Start
#calls the makewindowdow() method to create the tkinter GUI
#calls setSelect() which sorts the taskList, clears everything from the listBox
#then populates certain items from taskList to be displayed in the listBox
#window.mainloop() keeps the windowdow displaying
todo = ToDo()
window = todo.makeWindow()
window.mainloop()