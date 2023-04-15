from django.contrib import admin
from .models import Category, Area, Event, Comment, Volunteers, CommentImages

# Register your models here.

admin.site.register(Category)
admin.site.register(Area)
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Volunteers)
admin.site.register(CommentImages)