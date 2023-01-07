from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Room , Topic , Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse
from django.db.models import Q #helps for dynamic search , we can have || or && in if statements
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate , login, logout
# rooms = [
#     {'id':1 , 'name': "This is first id"},
#     {'id':2 , 'name': "This is second id"},
#     {'id':3 , 'name': "This is third id"},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated :
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
            messages.error(request, "Username or password doesn't exist")
        user = authenticate(request , username = username , password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist")
        
    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
   
    logout(request)
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False) # we write commit = false , to freeze the user  and we need the user object 
            user.username = user.username.lower() # so we havent commit the save for this , to clean the data we input
            user.save()
            login(request, user)
            return redirect('home')
        else:  
            messages.error(request , 'An error occured durign registration')
    context = {'page':page , 'form' : form}
    return render(request, 'base/login_register.html' , context)
    
def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    room_count = rooms.count()
    topics = Topic.objects.all()
    
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context =   {'rooms' : rooms , 'topics' : topics  ,'room_count':room_count , 'room_messages':room_messages}
    return render(request , 'base/home.html' ,context)

def room(request, pk):
    room = Room.objects.get(id= pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room' , pk = room.id)
    context = {'room' : room , 'room_messages':room_messages , 'participants':participants}
    return render(request, 'base/room.html' , context)

def userProfile(request,pk):
    user= User.objects.get(id = pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    context = {'user' : user , 'rooms':rooms ,'topics' : topics, 'room_messages': room_messages}
    return render(request , "base/profile.html" , context)


@login_required(login_url ='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit = False)
            room.hosts = request.user
            room.save()
            return redirect('home')
    context = { 'form': form}
    return render(request , 'base/room_form.html', context)


@login_required(login_url ='login')
def updateRoom(request , pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    
    if request.user != room.hosts:
        return HttpResponse(" Who are you , not the owner")

    if request.method == "POST":
        form = RoomForm(request.POST , instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form' : form}
    return render(request , 'base/room_form.html' , context)

@login_required(login_url ='login')
def deleteRoom(request , pk):
    room = Room.objects.get(id=pk)
    if request.user != room.hosts:
        return HttpResponse(" Who are you , not the owner")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request , "base/delete.html", {'obj':room})


@login_required(login_url ='login')
def deleteMessage(request , pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse(" Who are you , not the owner")
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request , "base/delete.html", {'obj':message})

