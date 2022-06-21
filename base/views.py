from multiprocessing import AuthenticationError
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .form import *
# Create your views here.

"""
rooms = [
    {'id':1, 'name': 'lets learn python!'},
    {'id':2, 'name': 'Design whit me!'},
    {'id':3, 'name': 'frontend developers'},
]
"""

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'UserName or Password does not exists')

    return render(request, 'base/login_register.html', {
        "page": page
    })


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {
        "form": form
    })



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    return render(request, 'base/home.html', {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count
    })



def room(request, pk):
    rooms = Room.objects.get(id = pk)
    return render(request, 'base/room.html', {
    "room": rooms
})
    

@login_required(login_url= 'login')    
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'base/room_form.html', {
        "form": form
    })


@login_required(login_url= 'login')    
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not Allowed to make changes")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'base/room_form.html', {
        "form": form
    })


@login_required(login_url= 'login')    
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("You are not Allowed to make changes")

    if request.method == 'POST':
        room.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'base/delete.html', {
        "obj": room
    })








