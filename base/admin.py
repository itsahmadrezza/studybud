from django.contrib import admin

from .models import *
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "updated", "created")
    

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
