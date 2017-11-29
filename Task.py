# File: Task.py
# Date: 2015-04-09
class Task:
    def __init__(self, TaskTitle, TaskDescription, TaskPriority, TaskDueDate, CreationDate):
        self.TaskTitle = TaskTitle
        self.TaskDescription = TaskDescription
        self.TaskPriority = TaskPriority
        self.TaskDueDate = TaskDueDate
        self.CreationDate = CreationDate
    def __repr__(self):
        return "%s|%s|%s|%s|%s" % (self.TaskTitle, self.TaskDescription, self.TaskPriority, self.TaskDueDate, self.CreationDate)