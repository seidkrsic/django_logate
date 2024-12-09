from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect 
from django.urls import reverse
# Create your views here.



class NewTaskForm(forms.Form): 
    task = forms.CharField(label="New task", min_length=5)  


def index(request): 
    if "tasks" not in request.session: 
        request.session["tasks"] = [] 

    return render(request, "tasks/index.html", {
        "tasks" : request.session["tasks"],  
    })

def add(request): 
    if request.method == "POST": 
        task = request.POST["task"]
        form = NewTaskForm(request.POST) 
        if form.is_valid():
            task = form.cleaned_data["task"] 
            print(request.session["tasks"])
            request.session["tasks"] += [task] 
            return HttpResponseRedirect(reverse("tasks:index")) 
        else: 
            return render(request, "tasks/add.html", {
                "form" : form,
            })

    return render(request, "tasks/add.html", {
        "form" : NewTaskForm(),
    })