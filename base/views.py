from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
rooms = [
    {'id':1 , 'name': "This is first id"},
    {'id':2 , 'name': "This is second id"},
    {'id':3 , 'name': "This is third id"},
]
def home(request):
    context =   {'rooms' : rooms}
    return render(request , 'home.html' ,context )

def room(request):
    return render(request, 'room.html')


