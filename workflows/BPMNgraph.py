class Flow:
    def __init__(self, id, name, source, target):
        self.id = id
        self.name = name
        self.source = source
        self.target = target

    def notify(self):
        print(self)

    def __str__(self):
        return "Flow id: " + str(self.id)+ " Flow name: " + str(self.name)

class SequenceFlow(Flow):
    def __init__(self,id,name,source,target):
        Flow.__init__(self,id,name,source,target)

class MessageFlow(Flow):
    def __init__(self,id,name,source,target,message):
        Flow.__init__(self,id,name,source,target)
        self.message = message


class Node:
    def __init__(self, id, name, state,lane):
        self.id = id
        self.name = name
        self.state = state
        self.lane = lane
    def notify(self):
        print(self)

    def __str__(self):
        return "\nAssigned to: "+ self.lane.name + " Running Node id: " + self.id + " Node name: " + str(self.name)

class Task(Node):
    def __init__(self, id, name, state,lane,incoming,outgoing,form):
        Node.__init__(self,id,name,state,lane)
        self.form = form
        #self.action = action
        self.incoming = incoming
        self.outgoing = outgoing

    def __str__(self):
        return "\nAssigned to: "+ self.lane.name + " Task id: " + self.id + " Task name: " \
               + self.name + "state: " + self.state+ " Incoming: "+self.incoming+" Outgoing: "+self.outgoing



class Gateway(Node):
    def __init__(self, id, name, state,lane,incoming,outgoing):
        Node.__init__(self,id,name,state,lane)
        self.incoming = incoming
        self.outgoing = outgoing

class EventBasedGateway(Gateway):
    def __init__(self, id, name, state, lane, incoming, outgoing):
        Gateway.__init__(self, id, name, state, lane, incoming, outgoing)

class ParallelGateway(Gateway):
    def __init__(self, id, name, state,lane,incoming,outgoing):
        Gateway.__init__(self,id,name,state,lane,incoming,outgoing)

class ExclusiveGateway(Gateway):
    def __init__(self, id, name, state,lane,incoming,outgoing):
        Gateway.__init__(self,id,name,state,lane,incoming,outgoing)

class InclusiveGateway(Gateway):
    def __init__(self, id, name, state,lane,incoming,outgoing):
        Gateway.__init__(self,id,name,state,lane,incoming,outgoing)


class Event(Node):
    def __init__(self, id, name = "", state = "waiting",lane = ""):
        Node.__init__(self,id,name,state,lane)

class NoHandlerEvent(Event):
    def __init__(self, id, name, state,lane):
        Event.__init__(self,id,name,state,lane)

class StartEvent(NoHandlerEvent):
    def __init__(self, id, name, state,lane,outgoing):
        NoHandlerEvent.__init__(self,id,name,state,lane)
        self.outgoing = outgoing

class EndEvent(NoHandlerEvent):
    def __init__(self, id, name, state,lane,incoming):
        self.incoming = incoming
        NoHandlerEvent.__init__(self,id,name,state,lane)

class HandlerEvent(Event):
    def __init__(self, id, name, state,lane):
        Event.__init__(self,id,name,state,lane)

class IntermediateCatchEvent(HandlerEvent):
    def __init__(self, id, name, state,lane,incoming,outgoing,type):
        Event.__init__(self,id,name,state,lane)
        self.type = type
        self.incoming = incoming
        self.outgoing = outgoing

class Lane:
    def __init__(self,name,id,flowNodeRef):
        self.name = name
        self.id = id
        self.flowNodeRef = flowNodeRef

    def __str__(self):
        str = ""
        for i in range(0,len(self.flowNodeRef)):
            str+=self.flowNodeRef[i]+"\n"
        return "Lane id: " + self.id + " Lane name: " + self.name + " Consist of: "+str

class Participant:
    def __init__(self,id,name,processRef):
        self.id = id
        self.name = name
        self.processRef = processRef

class Collaboration:
    def __init__(self,id,participants):
        self.id = id
        self.paticipants = participants

class Process:
    def __init__(self,id,elements):
        self.id = id
        self. elements = elements
