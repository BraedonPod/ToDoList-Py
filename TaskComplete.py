# File: TaskComplete.py
# Date: 2015-04-09
from Task import *
class TaskComplete(Task):
    def __init__(self, TaskTitle, TaskDescription, TaskPriority, TaskDueDate, CreationDate, IsComplete):
        Task.__init__(self, TaskTitle, TaskDescription, TaskPriority, TaskDueDate, CreationDate)
        self.IsComplete = IsComplete
    def __repr__(self):
        return "%s|%s|%s|%s|%s|%s" % (self.TaskTitle, self.TaskDescription, self.TaskPriority, self.TaskDueDate, self.CreationDate, self.IsComplete)





