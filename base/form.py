from django.forms import ModelForm

from .models import *
# Create your forms here.

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'