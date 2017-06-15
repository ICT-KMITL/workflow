from workflows.BPMNgraph import *
import datetime

class XMLParser:
    def __init__(self,root):
        self.root = root
        self.lanes = {}
        self.flows = {}
        self.nodes = {}
        self.processes = []
        self.participants = []
        self.elems = []

    def createCollaboration(self):
        for child in self.root[0]:
            if "participant" in child.tag:
                participant = Participant(child.get('id'), child.get('name'), child.get('processRef'))
                self.participants.append(participant)
        collaboration = Collaboration(self.root[0].get('id'), self.participants)

    def createLaneset(self):
        for child in self.root[1]:
            if 'laneSet' in child.tag:
                for lane in child:
                    lane1 = Lane(lane.get('name'), lane.get('id'), [])

                    for nodeRef in lane:
                        lane1.flowNodeRef.append(nodeRef.text)
                    self.lanes[lane1.id] = lane1

    def createProcess(self):
        for i in range(len(self.root)):
            #print(self.root)
            if "process" in self.root[i].tag:
                #elems = []
                for child in self.root[i]:
                    if 'startEvent' in child.tag:
                        self.createStartEvent(child)
                    if 'endEvent' in child.tag:
                        self.createEndEvent(child)
                    elif 'intermediateCatchEvent' in child.tag:
                        self.createIntermediateCatchEvent(child)
                    elif 'eventBasedGateway' in child.tag:
                        self.createEventBasedGateway(child)
                    elif 'intermediateCatchEvent' in child.tag:
                        self.createIntermediateCatchEvent(child)
                    elif 'task' in child.tag:
                        self.createTask(child)
                    elif 'exclusiveGateway' in child.tag:
                        self.createExclusiveGateway(child)
                    elif 'inclusiveGateway' in child.tag:
                        self.createInclusiveGateway(child)
                    elif 'parallelGateway' in child.tag:
                        self.createParallelGateway(child)
                    elif 'sequenceFlow' in child.tag:
                        self.createSequenceFlow(child)
                process = Process(self.root[i].get('id'), self.elems)
                self.processes.append(process)


    def createStartEvent(self,child):
        if len(child.attrib) > 1:

            for lane in self.lanes:
                #print(lane)
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    index = self.lanes[lane].flowNodeRef.index(child.get('id'))
                    for outgo in child:
                        if "outgoing" in outgo.tag:
                            outgoing = outgo.text
                    flowObj = StartEvent(child.get('id'), child.get('name'), "waiting", self.lanes[lane], outgoing)
                    #print(flowObj)
        else:
            for lane in self.lanes:
                #print(lane)
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    index = self.lanes[lane].flowNodeRef.index(child.get('id'))
                    for outgo in child:
                        if "outgoing" in outgo.tag:
                            outgoing = outgo.text
                    #print(index, self.lanes[lane].name)
                    #print(child.get('id'))
                    flowObj = StartEvent(child.get('id'), "", "waiting", self.lanes[lane], outgoing)
                    #print(flowObj)

        self.nodes[child.get('id')] = flowObj
        return (self.nodes)
        self.elems.append(flowObj)

    def createEndEvent(self,child):

        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lanes[lane].flowNodeRef.index(child.get('id'))
                    for incom in child:
                        if "incoming" in incom.tag:
                            incoming = incom.text
                    flowObj = EndEvent(child.get('id'), child.get('name'), "waiting", self.lanes[lane], incoming)
                    #print(flowObj)
        else:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    for incom in child:
                        if "incoming" in incom.tag:
                            incoming = incom.text
                    flowObj = EndEvent(child.get('id'), "", "waiting", self.lanes[lane], incoming)
                    #print(flowObj)
        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)

    def createIntermediateCatchEvent(self,child):
        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lanes[lane].flowNodeRef.index(child.get('id'))
                    for incom in child:
                        if "incoming" in incom.tag:
                            incoming = incom.text
                        elif "outgoing" in incom.tag:
                            incoming = incom.text
                        elif "timerEventDefinition" in incom.tag:
                            type = "timerEventDefinition"
                        elif 'messageEventDefinition' in incom.tag:
                            type = "messageEventDefinition"

                    flowObj = IntermediateCatchEvent(child.get('id'), child.get('name'), "waiting", self.lanes[lane], incoming,outgoing,type)
                    #print(flowObj)

        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)



    def createTask(self,child):
        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    is_form = 0
                    task_form = ""
                    for doc in child:
                        if "documentation" in doc.tag:
                            is_form = 1

                            task_form = doc.text
                    print(is_form)

                    for incom in child:

                        if "incoming" in incom.tag:
                            incoming = incom.text
                    for outgo in child:
                        if "outgoing" in outgo.tag:
                            outgoing = outgo.text
                    flowObj = Task(child.get('id'), child.get('name'), "waiting", self.lanes[lane], incoming, outgoing,task_form)
                    #print(flowObj)

        else:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))

                    flowObj = Task(child.get('id'), child.get('name'), "waiting", self.lanes[lane])
                    #print(flowObj)
        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)
    def createExclusiveGateway(self,child):
        incoming = []
        outgoing = []
        for flow in child:
            if 'incoming' in flow.tag:
                incoming.append(flow.text)
            elif 'outgoing' in flow.tag:
                outgoing.append(flow.text)
        #print(incoming)
        #print(outgoing)

        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = ExclusiveGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                               incoming, outgoing)
                    #print(flowObj)

        else:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = ExclusiveGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                               incoming, outgoing)
                    #print(flowObj)

        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)

    def createInclusiveGateway(self,child):
        incoming = []
        outgoing = []
        for flow in child:
            if 'incoming' in flow.tag:
                incoming.append(flow.text)
            elif 'outgoing' in flow.tag:
                outgoing.append(flow.text)
        #print(incoming)
        #print(outgoing)

        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = InclusiveGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                               incoming, outgoing)
                    #print(flowObj)

        else:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = InclusiveGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                               incoming, outgoing)
                    #print(flowObj)

        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)

    def createEventBasedGateway(self,child):

        incoming = []
        outgoing = []
        for flow in child:
            if 'incoming' in flow.tag:
                incoming.append(flow.text)
            elif 'outgoing' in flow.tag:
                outgoing.append(flow.text)
        #print(incoming)
        #print(outgoing)

        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = EventBasedGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                               incoming, outgoing)
                    #print(flowObj)

        else:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = EventBasedGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                               incoming, outgoing)
                    #print(flowObj)

        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)

    def createParallelGateway(self,child):
        incoming = []
        outgoing = []
        for flow in child:
            if 'incoming' in flow.tag:
                incoming.append(flow.text)
            elif 'outgoing' in flow.tag:
                outgoing.append(flow.text)
        #print(incoming)
        #print(outgoing)

        if len(child.attrib) > 1:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = ParallelGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                              incoming, outgoing)
                    #print(flowObj)

        else:
            for lane in self.lanes:
                if child.get('id') in self.lanes[lane].flowNodeRef:
                    # index = lane.flowNodeRef.index(child.get('id'))
                    flowObj = ParallelGateway(child.get('id'), child.get('name'), "waiting", self.lanes[lane],
                                              incoming, outgoing)
                    #print(flowObj)

        self.nodes[child.get('id')] = flowObj
        self.elems.append(flowObj)

    def createSequenceFlow(self,child):
        if len(child.attrib) > 3:

            seqFlow = Flow(child.get('id'), child.get('name'), child.get('sourceRef'), child.get('targetRef'))
        else:
            seqFlow = Flow(child.get('id'), "", child.get('sourceRef'), child.get('targetRef'))
        #print(seqFlow)
        self.flows[child.get('id')] = seqFlow
        self.elems.append(seqFlow)

global tread_no
tread_no=0
global threads
threads = []
global checklist
global condition_no
checklist = 0

class WorkflowExecution:
    def __init__(self,currentFlow,nodes,flows):
        self.currentFlow = currentFlow
        self.currentObj = self.currentFlow.source
        self.nextObj = self.currentFlow.target
        self.nodes = nodes
        self.flows = flows

        self.exclusive = 0
        self.inclusive = 0
        self.parallel = 0
        self.endEvent = 0
        self.task = 0
        self.join = 0
        self.joinOutgoing =0
        self.form = ""
        self.eventbased = 0
        self.timer = 0


    def run(self):
        currentObj = self.currentFlow.source
        self.nodes[currentObj].state = "Running"
        nextObj = self.currentFlow.target

        if isinstance(self.nodes[nextObj], Task):
            nextFlow1 = self.nodes[nextObj].outgoing
            nextFlow = self.flows[nextFlow1]
            nextFlow_target = nextFlow.target

            if isinstance(self.nodes[nextFlow_target], ExclusiveGateway):
                if isinstance(self.nodes[currentObj], Task):

                    #print("currentObject:",self.nodes[currentObj].name)
                    self.form = self.nodes[currentObj].form
                    print ("Workflow_engine:",self.nodes[currentObj].form)
                return self.getExclusiveGatewayDecisions(nextFlow_target)


            elif isinstance(self.nodes[nextFlow_target], InclusiveGateway):
                return self.getInclusiveGatewayDecisions(nextFlow_target)

            elif isinstance(self.nodes[nextFlow_target],ParallelGateway):
                return self.getParallelGatewayDecisions(nextFlow_target)

            elif isinstance(self.nodes[nextFlow_target],EventBasedGateway):
                return self.getEventBasedGatewayDecisions(nextFlow_target)

            else:
                self.task = 1
                self.form = self.nodes[nextObj].form
                if isinstance(self.nodes[currentObj], Task):
                    self.form += self.nodes[currentObj].form

                #print("Form"+self.nodes[nextObj].form)
                return self.flows[self.nodes[nextObj].outgoing]

        elif isinstance(self.nodes[nextObj],EndEvent):

            self.form = self.nodes[currentObj].form
            self.getEndEvent(self.nodes[nextObj])

        elif isinstance(self.nodes[nextObj],IntermediateCatchEvent):
            self.getIntermediateCatchEvent(self.nodes[nextObj])

        elif isinstance(self.nodes[nextObj],ParallelGateway):
            self.getParallelGatewayDecisions(nextObj)

        elif isinstance(self.nodes[nextObj],ExclusiveGateway):
            return (self.getExclusiveGatewayDecisions(nextObj))

    def getEventBasedGatewayDecisions(self,target):
        self.eventbased = 1
        event_list = []
        for i in range(0, len(self.nodes[target].outgoing)):
            eventFlow_id = self.flows[self.nodes[target].outgoing[i]].id
            event_list.append(eventFlow_id)
        return event_list
    def getIntermediateCatchEvent(self,target):
        if  target.type =='timerEventDefinition':

            time = target.name.split(' ')
            if time[1] == "Minutes":
                sec = int(time[0])*60
                d = datetime.timedelta(seconds=sec)
                self.timer = d
            elif time[1] == "Seconds":
                d = datetime.timedelta(seconds=int(time[0]))
                self.timer = d
            elif time[1] == "Hours":
                sec = int(time[0]) * 3600
                d = datetime.timedelta(seconds=sec)
                self.timer = d
            return target
        elif target.type == 'messageEventDefinition':
            return target


    def getExclusiveGatewayDecisions(self,target):
        print("-------------------EXCLUSIVEEEE GATWWAYYYYYY--------------------")
        self.exclusive = 1
        option_list = {}
        for i in range(0, len(self.nodes[target].outgoing)):
            decision_name = self.flows[self.nodes[target].outgoing[i]].name
            decision_name = decision_name.replace("\n", "").replace("\r", "")
            decision_flow = self.flows[self.nodes[target].outgoing[i]].id
            print(decision_name)
            option_list[decision_name] = decision_flow
        print(option_list)
        return option_list

    def getInclusiveGatewayDecisions(self):
        self.inclusive = 1
        return 1

    def getParallelGatewayDecisions(self,target):
        self.parallel = 1
        parallel_list = []
        if len(self.nodes[target].incoming) > 1:
            self.join = 1
            self.joinOutgoing = self.nodes[target].outgoing[0]
            for i in range(0, len(self.nodes[target].incoming)):
                #decision_name = (i, self.flows[self.nodes[target].outgoing[i]].name)
                decision_flow = self.flows[self.nodes[target].incoming[i]].id
                parallel_list.append(decision_flow)
            return parallel_list
        else:
            for i in range(0, len(self.nodes[target].outgoing)):
                #decision_name = (i, self.flows[self.nodes[target].outgoing[i]].name)
                decision_flow = self.flows[self.nodes[target].outgoing[i]].id
                parallel_list.append(decision_flow)
            return parallel_list


    def getEndEvent(self,endObj):
        self.endEvent = 1

        return endObj.name


