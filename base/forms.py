from django.forms import ModelForm 
from .models import Room , User
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['hosts' , 'participants']
        
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [ 'avatar' , 'name' , 'username', 'email' ,'bio']