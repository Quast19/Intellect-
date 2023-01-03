from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room , Topic

from django.contrib import messages
# Create your views here.

from django.db.models import Q #helps for dynamic search , we can have || or && in if statements
from .forms import RoomForm


from django.contrib.auth import authenticate , login, logout
# rooms = [
#     {'id':1 , 'name': "This is first id"},
#     {'id':2 , 'name': "This is second id"},
#     {'id':3 , 'name': "This is third id"},
# ]

def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        try:
           user = User.objects.get(username = username)
        except:
            messages.error(request, "No such user")
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, "username or password doesn't exist")
    
    context = {}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    context =   {'rooms' : rooms , 'topics' : topics  ,'room_count':room_count}
    return render(request , 'base/home.html' ,context)

def room(request, pk):
    room = Room.objects.get(id= pk)
    context = {'room' : room}
    return render(request, 'base/room.html' , context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = { 'form': form}
    return render(request , 'base/room_form.html', context)

def updateRoom(request , pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    
    if request.method == "POST":
        form = RoomForm(request.POST , instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request , 'base/room_form.html' , context)


def deleteRoom(request , pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request , "base/delete.html", {'obj':room})


