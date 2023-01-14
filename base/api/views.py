from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api'
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ] 
    return Response(routes)
    #return JsonResponse(routes, safe=False)#safe allows the python dictionary to only be used in python , where as conversion to JSon is restricted thus we set "safe"  to False.
    
@api_view(['GET'])   
def getRooms(request):
    rooms = Room.objects.all()
    serializier = RoomSerializer(rooms , many=True) #many if multiple instances of the class are to be serialized, or many objects are to be serialized in simple words
    return Response(serializier.data)#we can send lists or dictionaries but not the room object directly , hence we need serializers
    
@api_view(['GET'])   
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializier = RoomSerializer(room , many=False) #many if multiple instances of the class are to be serialized, or many objects are to be serialized in simple words
    return Response(serializier.data)#we can send lists or dictionaries but not the room object directly , hence we need serializers