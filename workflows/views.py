
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse

from .forms import UserForm

def index(request):
    return HttpResponse("<h1>This is workflow!</h1>")

class UserFormView(View):
    form_class = UserForm
    template_name = "workflows/registration_form.html"

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name, {'form':form})

    #process from data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('workflow:index')

        return render(request, self.template_name, {'form': form})
