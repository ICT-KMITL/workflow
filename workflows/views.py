from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from channels import Group
from .forms import *

from workflows.WorkflowEngine import *
import xml.etree.ElementTree as ET

from django.shortcuts import render
import social.apps.django_app.default.models as sm
from django.contrib.auth import authenticate, login, logout
import json
import ast

def chat_room1(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        return render(request, 'workflows/chat_room1.html', {'user': user.username})

def chat_room2(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        return render(request, 'workflows/chat_room2.html', {'user': user.username})

def chat_room3(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        return render(request, 'workflows/chat_room3.html', {'user': user.username})

def tasks(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        assignedTasks = PendingTask.objects.filter(assignToUser=user)
        return render(request, 'workflows/tasks.html', {'assignedTasks': assignedTasks})

def do_task(request,task_id):
    if request.method == "POST": #Executing tasks

        print(request.POST)
        user = request.user
        task = get_object_or_404(PendingTask,pk=task_id)
        xml = task.belongToWFId.xml

        root = ET.fromstring(xml)

        parser = XMLParser(root)
        parser.createCollaboration()
        parser.createLaneset()
        parser.createProcess()

        nodes = parser.nodes
        lanes = parser.lanes
        flows = parser.flows
        elems = parser.elems

        workflow_engine = WorkflowExecution(flows[task.currentFlow],nodes,flows)
        workflow_engine.run()


        if workflow_engine.task == 1:
            print("HLEFOEOFEF")



            flow_id = workflow_engine.run().id
            target_task = flows[flow_id].target
            assignedUser = nodes[target_task].lane.name
            assignedUsers = assignedUser.split(",")
            task_name = nodes[target_task].name

            form = workflow_engine.form
            pending_task = PendingTask(form=form, listener=User.objects.get(username=assignedUsers[0]),
                                       belongToWFId=task.belongToWFId, taskName=task_name, currentFlow=flow_id, state=1)
            pending_task.save()

            for i in range(0,len(assignedUsers)):

                us = User.objects.get(username=assignedUsers[i])

                pending_task.assignToUser.add(us)


            #newjson = {}

            '''
            for form_elem_key, form_elem_value in request.body.iteritems():
                if form_elem_key != 'csrfmiddlewaretoken' and form_elem_key != 'submit':
                    print("hello")
            '''
            global dict
            print(xml)
            input = dict(request.POST)
            for i in range(len(root)):
                print("OK-1")
                if "process" in root[i].tag:
                    print("OK-2")
                    # noinspection PyPackageRequirements
                    for child in root[i]:
                        print("OK-3")
                        print(child.get('id'))
                        print("TASK ID: "+flows[flow_id].source)
                        if child.get('id') == flows[flow_id].source:
                            print("OK-4")
                            for doc in child:
                                print("OK-5")
                                if "documentation" in doc.tag:
                                    print(doc.text)
                                    form = doc.text
                                    form = form.replace("\n", "").replace("\r", "")
                                    json_form = json.loads(form)
                                    print(json_form)
                                    print(len(json_form))
                                    for j in json_form:
                                        print(j)
                                        if 'name' in j:
                                            for key, value in input.items():
                                                if j["name"] == key:
                                                    j["value"] = value[0]


                                                    doc.text = json.dumps(json_form)


            #print("JSON_FORM",json_form)
            print(root)
            print(ET.tostring(root))

            '''

            dict_json = {}
            dict_json['action'] = "notification"
            taskId = pending_task.taskId
            lst = [task_name, nodes[target_task].lane.name, task.belongToWFId.executingDate.strftime("%B %d, %Y"), taskId]
            dict_json['data'] = lst
            data_noti = json.dumps(dict_json)
            Group("User-" + assignedUser.username).send({"text": data_noti})


            print(data_noti,assignedUser.username)
            '''

            executing_flow = task.belongToWFId
            executing_flow.currentFlow = flow_id
            executing_flow.xml = ET.tostring(root)
            executing_flow.save()


        elif workflow_engine.exclusive == 1:

            option_list = workflow_engine.run()
            '''
            decisions = []
            for option in option_list:
                decisions.append(option.id)
            '''

            option_list = request.session['options_list']
            decision = request.POST['decisions']

            print(decision)
            flow_id = option_list[decision]
            print(flow_id)
            target_task = flows[flow_id].target
            assignedUser = nodes[target_task].lane.name
            assignedUsers = assignedUser.split(",")
            task_name = nodes[target_task].name

            form = workflow_engine.form
            pending_task = PendingTask(form=form, listener=User.objects.get(username=assignedUsers[0]),
                                       belongToWFId=task.belongToWFId, taskName=task_name, currentFlow=flow_id, state=1)
            pending_task.save()

            for i in range(0, len(assignedUsers)):
                us = User.objects.get(username=assignedUsers[i])

                pending_task.assignToUser.add(us)

            executing_flow = task.belongToWFId
            executing_flow.currentFlow = flow_id
            executing_flow.save()

        elif workflow_engine.parallel == 1:
            incom_flow_id_list =  workflow_engine.run()

            #Joining parallel tasks
            if workflow_engine.join == 1:
                count = 0
                for i in range(0,len(incom_flow_id_list)):
                    if PendingTask.objects.filter(currentFlow = nodes[flows[incom_flow_id_list[i]].source].incoming).exists():
                        count+=1
                        print("OKOKOKOKOERGRTGTGJTROGJREPGWEGJREPG")

                if count == 1:


                    next_flow = workflow_engine.joinOutgoing
                    target_task = flows[next_flow].target
                    #assignedUser = User.objects.get(username=nodes[target_task].lane.name)
                    '''
                    task_name = nodes[target_task].name

                    pending_task = PendingTask(assignToUser=assignedUser, form="", listener=assignedUser,
                                               belongToWFId=task.belongToWFId, taskName=task_name, currentFlow=next_flow,
                                               state=1)
                    pending_task.save()

                    '''
                    assignedUser = nodes[target_task].lane.name
                    assignedUsers = assignedUser.split(",")
                    task_name = nodes[target_task].name

                    form = workflow_engine.form
                    pending_task = PendingTask(form=form, listener=User.objects.get(username=assignedUsers[0]),
                                               belongToWFId=task.belongToWFId, taskName=task_name, currentFlow=next_flow,
                                               state=1)
                    pending_task.save()

                    for i in range(0, len(assignedUsers)):
                        us = User.objects.get(username=assignedUsers[i])

                        pending_task.assignToUser.add(us)

                    executing_flow = task.belongToWFId
                    executing_flow.currentFlow = next_flow
                    executing_flow.save()
                else:
                    task.delete()
                    assignedTasks = PendingTask.objects.filter(assignToUser=user)
                    return render(request, 'workflows/tasks.html', {'assignedTasks': assignedTasks})

            #Splitting parallel tasks
            else:
                flow_id_list = workflow_engine.run()
                for i in range(0,len(flow_id_list)):
                    target_task = flows[flow_id_list[i]].target
                    '''
                    assignedUser = User.objects.get(username=nodes[target_task].lane.name)
                    task_name = nodes[target_task].name
                    pending_task = PendingTask(assignToUser=assignedUser, form="", listener=assignedUser,
                                           belongToWFId=task.belongToWFId, taskName=task_name, currentFlow=flow_id_list[i], state=1)
                    pending_task.save()
                    '''
                    assignedUser = nodes[target_task].lane.name
                    assignedUsers = assignedUser.split(",")
                    task_name = nodes[target_task].name

                    form = workflow_engine.form
                    pending_task = PendingTask(form=form, listener=User.objects.get(username=assignedUsers[0]),
                                               belongToWFId=task.belongToWFId, taskName=task_name, currentFlow=flow_id_list[i],
                                               state=1)
                    pending_task.save()

                    for i in range(0, len(assignedUsers)):
                        us = User.objects.get(username=assignedUsers[i])

                        pending_task.assignToUser.add(us)


        elif workflow_engine.endEvent == 1:
            print("EFERGGRTHH")

            executing_flow = task.belongToWFId
            executing_flow.delete()


        task.delete()
        assignedTasks = PendingTask.objects.filter(assignToUser=user)


        return render(request,'workflows/tasks.html',{'assignedTasks':assignedTasks})

    else: #Showing task for user

        if not request.user.is_authenticated():
            return render(request, 'workflows/login.html')
        else:

            task = get_object_or_404(PendingTask, pk=task_id)
            xml = task.belongToWFId.xml

            root = ET.fromstring(xml)

            parser = XMLParser(root)
            parser.createCollaboration()
            parser.createLaneset()
            parser.createProcess()

            nodes = parser.nodes
            lanes = parser.lanes
            flows = parser.flows
            elems = parser.elems

            workflow_engine = WorkflowExecution(flows[task.currentFlow], nodes, flows)
            runningFlow = workflow_engine.run()
            user = request.user

            if workflow_engine.exclusive == 1:
                option_list = runningFlow

                print("OPTION_LIST:",option_list)

                request.session['options_list'] = option_list

                options = option_list.keys()

                form = workflow_engine.form
                print("------------------------------------FORM----------------------------------", form)
                form = form.replace("\n", "").replace("\r", "")
                print("------------------------------------FORM----------------------------------", form)

                return render(request, 'workflows/do_task.html', {'task': task, 'user': user,'form':form,'options':options})

            elif workflow_engine.endEvent == 1:
                end_name = workflow_engine.run()
                form = workflow_engine.form
                form = form.replace("\n", "").replace("\r", "")

                return render(request, 'workflows/do_task.html', {'task': task, 'user': user,'end':end_name,'form':form})


            else:

                user = request.user
                pending_task = get_object_or_404(PendingTask, pk=task_id)

                form = workflow_engine.form
                form = form.replace("\n", "").replace("\r", "")
                print("------------------------------------FORM----------------------------------",form)






                request.session['taskId'] = pending_task.taskId
                return render(request, 'workflows/do_task.html', {'task': pending_task, 'user': user,'form':form})



def publish(request):
    checkedList = request.POST.getlist('publishChecked')
    user = request.user

    for i in range(0,len(checkedList)):

        workflow_id = int(checkedList[i])
        workflow = get_object_or_404(WorkflowTemplate, pk=workflow_id)
        xml = workflow.xml
        #xml_file = open("file", "w").write(xml)
        root = ET.fromstring(xml)

        print(root.tag)
        parser = XMLParser(root)
        parser.createCollaboration()
        parser.createLaneset()
        parser.createProcess()

        nodes = parser.nodes
        lanes = parser.lanes
        flows = parser.flows
        elems = parser.elems

        startEventList = []
        startFlows = []
        for node in nodes:
            if isinstance(nodes[node],StartEvent):
                startEventList.append(nodes[node])

                print("StartFlow " + nodes[node].outgoing)
                startFlows.append(flows[nodes[node].outgoing])

        executing_flow = ExecutingFlow(status=1, templateId=workflow, executor=user, currentFlow="", xml=xml)
        executing_flow.save()

        for i in range (0,len(startFlows)):
            target_task = nodes[startFlows[i].target]
            flow_id = startFlows[i].id
            assignedUser = target_task.lane.name
            assignedUsers = assignedUser.split(",")
            task_name = target_task.name

            pending_task = PendingTask(form="", listener=User.objects.get(username=assignedUsers[0]),
                                       belongToWFId=executing_flow, taskName=task_name, currentFlow=flow_id, state=1)
            pending_task.save()

            for i in range(0, len(assignedUsers)):
                us = User.objects.get(username=assignedUsers[i])

                pending_task.assignToUser.add(us)







    assignedTasks = PendingTask.objects.filter(assignToUser=user)


    return render(request,'workflows/tasks.html',{'assignedTasks':assignedTasks})


def editingWorkflow(request, workflow_id):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        workflow = get_object_or_404(WorkflowTemplate, pk=workflow_id)
        xml = workflow.xml
        print(xml)
        xml = xml.replace("\r", "").replace("\n", "").replace("\"", "\\\"")

        request.session['workflowId'] = workflow.id
        return render(request, 'workflows/modeler.html', {'editingWorkflow': workflow, 'xml': xml, 'user': user})



def openXML(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:

        xml = request.FILES['file'].read().decode("utf-8")
        print(type(xml), xml)
        xml = xml.replace("\r", "\\r").replace("\n", "\\n").replace("\"", "\\\"").replace("\ufeff", "");

        request.session['XMLlocal'] = xml
        return render(request, 'workflows/create_XML.html', {'xml': xml})

def create_XML(request):
    form = WorkflowTemplateForm(request.POST or None)

    if form.is_valid():
        workflow = form.save(commit=False)
        workflow.creator = request.user
        workflow.save()
        request.session['workflowId'] = workflow.id

        xml = request.session['XMLlocal']
        return render(request, 'workflows/modeler.html', {'xml': xml})


    else:
        context = {
            "form": form,
        }
        return render(request, 'workflows/create_XML.html', context)



def job(request):
   return render(request, "workflows/job.html")


def announce(request):
   return render(request, "workflows/announce.html")


def funding(request):
   return render(request, "workflows/funding.html")

def view_profile(request):
    return render(request, "workflows/view_profile.html")


def profileEdit(request):
    return render(request, 'workflows/profile-edit.html')

def task_noti(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        return render(request, 'workflows/task_noti.html', {'user': user.username})

def track(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        executingFlows = ExecutingFlow.objects.filter(executor=user)
        return render(request, 'workflows/track.html', {'executingFlows': executingFlows})

def track_modeler(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        return render(request, 'workflows/track_modeler.html', {'user': user})



def create(request):

    print(request.POST)

    form = WorkflowTemplateForm(request.POST or None)

    if form.is_valid():
        workflow = form.save(commit=False)
        workflow.creator = request.user
        workflow.save()
        request.session['workflowId'] = workflow.id
        return render(request, 'workflows/modeler.html')

    else:
        context = {
            "form": form,
        }
        return render(request, 'workflows/create.html', context)

def create_job(request):
    form = WorkflowTemplateForm(request.POST or None)

    if form.is_valid():
        workflow = form.save(commit=False)
        workflow.creator = request.user
        workflow.save()

        request.session['workflowId'] = workflow.id
        return render(request, 'workflows/job.html')

    else:
        context = {
            "form": form,
        }
        return render(request, 'workflows/create_job.html', context)

def create_funding(request):
    form = WorkflowTemplateForm(request.POST or None)

    if form.is_valid():
        workflow = form.save(commit=False)
        workflow.creator = request.user
        workflow.save()
        request.session['workflowId'] = workflow.id
        return render(request, 'workflows/funding.html')

    else:
        context = {
            "form": form,
        }
        return render(request, 'workflows/create_funding.html', context)



def create_news(request):
    form = WorkflowTemplateForm(request.POST or None)

    if form.is_valid():
        workflow = form.save(commit=False)
        workflow.creator = request.user
        workflow.save()
        request.session['workflowId'] = workflow.id
        return render(request, 'workflows/announce.html')

    else:
        context = {
            "form": form,
        }
        return render(request, 'workflows/create_news.html', context)



@csrf_exempt
def saveXML(request):
    workflowId = request.session['workflowId']
    if request.is_ajax():
        if request.method == 'POST':
            workflow = WorkflowTemplate.objects.get(id=workflowId)
            workflow.xml = request.POST.get('userXml')
            workflow.save()
            user = request.user
            workflows = WorkflowTemplate.objects.filter(creator=user)
            return render(request, 'workflows/index.html', {'workflows': workflows})

@csrf_exempt
def saveEditedXML(request, workflow_id):

    if request.is_ajax():
        if request.method == 'POST':
            workflow = WorkflowTemplate.objects.get(id=workflow_id)
            workflow.xml = request.POST.get('userXml')
            workflow.save()
            user = request.user
            workflows = WorkflowTemplate.objects.filter(creator=user)
            return render(request, 'workflows/index.html', {'workflows': workflows})


def modeler(request):

    return render(request, "workflows/modeler.html")


def index(request):
    if not request.user.is_authenticated():
        return register(request)
    else:
        user = request.user
        workflows = WorkflowTemplate.objects.filter(creator=user)
        return render(request, 'workflows/index.html', {'workflows': workflows})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'workflows/login.html', context)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user = request.user
                workflows = WorkflowTemplate.objects.filter(creator=user)
                return render(request, 'workflows/index.html', {'workflows': workflows})

            else:
                return render(request, 'workflows/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'workflows/login.html', {'error_message': 'Invalid login'})
    return render(request, 'workflows/login.html')






def login_user_google(request):
    uname = ""
    if request.method == 'POST' and 'submit' in request.POST:
        submit = request.POST['submit']
        if submit == "sign-out":
            logout(request)
    if '_auth_user_id' in request.session:
        uname = sm.UserSocialAuth.objects.get(
            user_id=int(request.session['_auth_user_id'])
        ).user
    return render(request, 'workflows/index.html', {'uname': uname})






def register(request):

    if not request.user.is_authenticated():
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'workflows/index.html')
        context = {
            "form": form,
        }
        return render(request, 'workflows/register.html', context)
    else:
        user = request.user
        workflows = WorkflowTemplate.objects.filter(creator=user)
        return render(request, 'workflows/index.html', {'workflows': workflows})





#User edit profile
def register_user(request):
    if not request.user.is_authenticated():
        return redirect('/register')
    else:
        form = StudentForm(request.POST or None, request.FILES or None)
        context = {
            "form": form,
        }
        if form.is_valid():
            student = form.save(commit=False)

            student.user = request.user
            student.profileLogo = request.FILES['profileLogo']

            student.save()
            return render(request, 'workflows/index.html', context)

        return render(request, 'workflows/profile-edit.html', context)


def profileDetail(request):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:

        user = request.user
        try:
            student = StudentModel.objects.get(user=user)
        except StudentModel.DoesNotExist:
            student = {}


        print(student)

        return render(request, 'workflows/view_profile.html', {'student': student})


def job(request):
    return render(request, "workflows/job.html")

def announce(request):
    return render(request, "workflows/announce.html")

def funding(request):
    return render(request, "workflows/funding.html")


def design_form(request):
    return render(request, "workflows/designform.html")





'''
def verify(request):
    # Google will direct with state and code in the URL
    # ?state=zNHRjuYO...&code=4/zK5F93g2we...

    # ensure we have a session state and the state value is the same as what google returned
    if 'google_state' not in request.session \
            or 'state' not in request.GET \
            or 'code' not in request.GET \
            or request.session['google_state'] != request.GET['state']:
        return False
    else:
        return True





def profileDetail(request, user):
    if not request.user.is_authenticated():
        return render(request, 'workflows/login.html')
    else:
        user = request.user
        album = get_object_or_404(StudentModel, pk=user)
        return render(request, 'workflows/view_Profile.html', {'user': user})



def profileDetail(request):
  if request.method == 'GET':
    form = StudentForm(request.GET)
    if form.is_valid():
        return render(request, 'workflows/view_Profile.html')
  else:
    form = StudentForm()



def post_create(request):
    form =  StudentModel(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print (form.cleaned_data.get("firstname"))
        instance.save()

        context = {
            "form":  form,
        }

        return render(request,"post_form.html",context)
'''