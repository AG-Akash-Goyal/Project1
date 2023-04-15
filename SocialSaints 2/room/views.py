from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from home.models import Setting
from .models import Room, Message,Event


@login_required(login_url='/login')
def room(request, slug):
    setting=Setting.objects.get(pk=1)
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'room.html', {'room': room, 'msg': messages,'setting':setting})
