from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Room , Topic
# Create your views here.
from .forms import RoomForm

# rooms = [
#     {'id':1 , 'name': "This is first id"},
#     {'id':2 , 'name': "This is second id"},
#     {'id':3 , 'name': "This is third id"},
# ]


def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context =   {'rooms' : rooms , 'topics' : topics}
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


