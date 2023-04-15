from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.urls import reverse
# Create your models here.
from user.models import UserProfile
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg, Count
from django.forms import ModelForm


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Area(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    status=models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Event(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # many to one relation with Category
    area = models.ForeignKey(Area, on_delete=models.CASCADE)  # many to one relation with Area
    title = models.CharField(max_length=150)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(upload_to='images/', null=False)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    favorites = models.ManyToManyField(User, related_name='favourites', default=None, blank=True)
    members = models.IntegerField(default=0, blank=True)
    location=models.CharField(max_length=500,null=True)
    is_volunteer = models.ManyToManyField(User, related_name='is_volunteer', default=None, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="150"/>'.format(self.image.url))
        else:
            return ""

    def avaregereview(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews["avarage"] is not None:
            avg = float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def five(self):
        reviews = Comment.objects.filter(event=self, status='True', rate=5).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def five1(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(count=Count('id'))
        reviews1 = Comment.objects.filter(event=self, status='True', rate=5).aggregate(count1=Count('id'))
        cnt = 0
        try:
            cnt = int(reviews1["count1"]) / int(reviews["count"]) * 100
            return cnt
        except ZeroDivisionError:
            return 0

    def four(self):
        reviews = Comment.objects.filter(event=self, status='True', rate=4).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def four1(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(count=Count('id'))
        reviews1 = Comment.objects.filter(event=self, status='True', rate=4).aggregate(count1=Count('id'))
        cnt = 0
        try:
            cnt = int(reviews1["count1"]) / int(reviews["count"]) * 100
            return cnt
        except ZeroDivisionError:
            return 0

    def three(self):
        reviews = Comment.objects.filter(event=self, status='True', rate=3).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def three1(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(count=Count('id'))
        reviews1 = Comment.objects.filter(event=self, status='True', rate=3).aggregate(count1=Count('id'))
        cnt = 0
        try:
            cnt = int(reviews1["count1"]) / int(reviews["count"]) * 100
            return cnt
        except ZeroDivisionError:
            return 0

    def two(self):
        reviews = Comment.objects.filter(event=self, status='True', rate=2).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def two1(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(count=Count('id'))
        reviews1 = Comment.objects.filter(event=self, status='True', rate=2).aggregate(count1=Count('id'))
        cnt = 0
        try:
            cnt = int(reviews1["count1"]) / int(reviews["count"]) * 100
            return cnt
        except ZeroDivisionError:
            return 0

    def one(self):
        reviews = Comment.objects.filter(event=self, status='True', rate=1).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def one1(self):
        reviews = Comment.objects.filter(event=self, status='True').aggregate(count=Count('id'))
        reviews1 = Comment.objects.filter(event=self, status='True', rate=1).aggregate(count1=Count('id'))
        cnt = 0
        try:
            cnt = int(reviews1["count1"]) / int(reviews["count"]) * 100
            return cnt
        except ZeroDivisionError:
            return 0


class Images(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class Video(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    video = models.FileField(upload_to='images/%y', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    note = models.BooleanField(default=False)
    adminnote = models.CharField(blank=True, max_length=100)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='True')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentImages(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images/')


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class Volunteers(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)



class VolunteersForm(ModelForm):
    class Meta:
        model = Volunteers
        fields = ['user','event']
