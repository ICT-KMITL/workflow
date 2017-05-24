from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
from django.db import models

"""
class Arc(models.Model):

    connected_node = Node()
    def action(self):
        return "do something"

class Node(models.Model):
    title = models.CharField(max_length=100)
    arc = Arc()

"""

class StudentModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profileLogo = models.FileField(default='')
    tittle = models.CharField(max_length=50,default='')
    userType = models.CharField(max_length=50, default='')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    dateOfBirth = models.CharField(max_length=50)
    department = models.CharField(max_length=50, default='')
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    loopId = models.CharField(max_length=50,default='')
    facebookAddress = models.CharField(max_length=100)


    def __unicode__(self):
        return self.firstName


class StaffModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profileLogo = models.FileField(default='')
    tittle = models.CharField(max_length=50,default='')
    userType = models.CharField(max_length=50, default='')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    dateOfBirth = models.CharField(max_length=50)
    department = models.CharField(max_length=50, default='')
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    loopId = models.CharField(max_length=50,default='')
    facebookAddress = models.CharField(max_length=100)


class AlumniModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profileLogo = models.FileField(default='')
    tittle = models.CharField(max_length=50,default='')
    userType = models.CharField(max_length=50, default='')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    dateOfBirth = models.CharField(max_length=50)
    department = models.CharField(max_length=50, default='')
    mobile = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    loopId = models.CharField(max_length=50,default='')
    facebookAddress = models.CharField(max_length=100)


class WorkflowTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    xml = models.TextField(default='')
    status = models.CharField(max_length=100,default="Unpublished")
    #start = models.ForeignKey(StartEvent)
    creator = models.ForeignKey(User,default=1)

class ExecutingFlow(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    templateId = models.ForeignKey(WorkflowTemplate, related_name = "template", default=1)
    executor = models.ForeignKey(User, default=1)
    executingDate = models.DateField(default=timezone.now)
    currentFlow = models.CharField(max_length=50,default='')
    xml =  models.TextField(default='')

class PendingTask(models.Model):
    taskId = models.AutoField(primary_key=True)
    assignToUser = models.ForeignKey(User, related_name='assignUser')
    form = models.TextField(max_length=400)
    listener = models.ForeignKey(User,related_name='listener',default = 1)
    belongToWFId = models.ForeignKey(ExecutingFlow,default = 1)
    taskName = models.CharField(max_length=100)
    currentFlow = models.CharField(max_length=50,default='')
    state = models.BooleanField(default=False)

class TimerEventBased(models.Model):
    id = models.AutoField(primary_key=True)
    eventTime =  models.DateField(default=timezone.now)
    currentFlow = models.CharField(max_length=50, default='')
    elementId = models.CharField(max_length=50, default='')
    assignToUser = models.ForeignKey(User, related_name='timerAssignUser')
    belongToWFId = models.ForeignKey(ExecutingFlow,default = 1)

class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=200)


class ChannelJoin(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,default=1)
    channelId = models.ForeignKey(Channel,default=1)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    msg = models.TextField(max_length=200)
    sender = models.ForeignKey(User, related_name = "sender", default=1)
    receiver = models.ForeignKey(User, related_name = "receiver", default=1)
    timestamp = models.TimeField(auto_now=False, auto_now_add=False)
    room = models.ForeignKey(Channel ,default='')










