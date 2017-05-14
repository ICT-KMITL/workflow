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



from django.shortcuts import render
import social.apps.django_app.default.models as sm
from django.contrib.auth import authenticate, login, logout






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

        #request.session['workflowId'] = workflow.id
        return render(request, 'workflows/modeler.html', {'xml': xml})




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

def create(request):
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