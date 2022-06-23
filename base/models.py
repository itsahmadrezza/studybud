from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name



class Room(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=64)
    decription = models.TextField(null=True, blank=True) # use null for user can be blank this fild
    participants = models.ManyToManyField(
        User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True) # this ecouls when type your cometns this type time now
    created = models.DateTimeField(auto_now_add=True) # this means take snapshot when text writed 

    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return f"{self.name}"



class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]

