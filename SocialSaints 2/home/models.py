from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.forms import TextInput, Textarea
from django.forms import ModelForm

from event.models import Event
from user.models import UserProfile


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    mission = models.CharField(blank=True, max_length=500)
    vission = models.CharField(blank=True, max_length=500)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class FAQ(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = RichTextUploadingField()
    note = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class ReplyForm(ModelForm):
    class Meta:
        model = FAQ
        fields = ['answer']


class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    head = models.CharField(default="Feedback",max_length=50)
    desc = models.TextField()
    type = models.CharField(max_length=7, default="Website")
    ftime = models.DateTimeField(auto_now_add=True)
    eid = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
    uid = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True)
