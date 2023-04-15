from django.db import models
from event.models import Event
from django.contrib.auth.models import User
from django.forms import ModelForm


class Room(models.Model):
    event = models.ForeignKey(Event,related_name='event',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)


class CreateRoom(ModelForm):
    class Meta:
        model=Room
        fields=['event','name','slug']


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)