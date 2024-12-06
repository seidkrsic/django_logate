from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect 
from django.urls import reverse
# Create your views here.


tasks = ["foo", "bar", "baz"] 

class NewTaskForm(forms.Form): 
    task = forms.CharField(label="New task", min_length=5)  


def index(request): 
    return render(request, "tasks/index.html", {
        "tasks" : tasks,  
    })

def add(request): 
    if request.method == "POST": 
        task = request.POST["task"]
        form = NewTaskForm(request.POST) 
        if form.is_valid():
            task = form.cleaned_data["task"] 
            tasks.append(task) 
            return HttpResponseRedirect(reverse("tasks:index")) 
        else: 
            return render(request, "tasks/add.html", {
                "form" : form,
            })

    return render(request, "tasks/add.html", {
        "form" : NewTaskForm(),
    })