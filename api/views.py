from .models import *
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def registerView(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]

        try:
            object = Users.objects.create_user(username=name, email=email, password=password)
            object.first_name = name.upper()
            object.save()
        except:
            return render(request, "register.html", {
                "message": "Email already exists"
            })
        login(request, object)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def loginView(request):
    if request.method == "POST":
        user = None
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, username=email, password=password)
        except:
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {
                    "message": "Invalid email or password."
                })
    else:
        return render(request, "login.html")


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def indexView(request):
    if request.user.is_authenticated:
        return render(request, "index.html",
                      {"data": ToDoLists.objects.order_by("-priority").all().filter(user=request.user)})
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def newTask(request):
    if request.method == "POST":
        body = request.POST.get('body')
        user = request.user
        name = request.POST.get('name')
        priority = request.POST.get('priority')

        if len(list(name)) == 0 or len(list(body)) == 0:
            return HttpResponseRedirect(reverse("index"))
        else:
            try:
                ToDoLists(name=name, body=body, user=user, priority=priority).save()
                return render(request, "index.html",
                              {"data": ToDoLists.objects.order_by("-priority").all().filter(user=user)})
            except:
                return render(request, "index.html", {
                    "message": "Task Name already exists"
                })

@csrf_exempt
@login_required
def taskView(request, name):
    return render(request, "task.html",
                  {"data": ToDoLists.objects.order_by("-priority").all().filter(name=name, user=request.user)})


@csrf_exempt
@login_required
def deleteTask(request, name):
    ToDoLists.objects.all().filter(name=name, user=request.user).delete()
    return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def taskCompleted(request, name):
    object = ToDoLists.objects.get(name=name)
    object.completed = True
    object.save()

    return render(request, "task.html",
                  {"data": ToDoLists.objects.order_by("-priority").all().filter(name=name, user=request.user)})


@csrf_exempt
@login_required
def taskNotCompleted(request, name):
    object = ToDoLists.objects.get(name=name)
    object.completed = False
    object.save()
    return render(request, "task.html",
                  {"data": ToDoLists.objects.order_by("-priority").all().filter(name=name, user=request.user)})
