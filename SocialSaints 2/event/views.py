from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib import messages
from datetime import datetime
from home.forms import SearchForm, NewQuestionForm
from home.models import Setting, FAQ, ReplyForm
from event.forms import CategoryForm,AreaForm,EventForm,ReviewUpdate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from event.models import Event, Category, Images, Video, Comment, CommentImages, CommentForm,Volunteers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from room.models import Room, CreateRoom


def addcategory(request):
    category=CategoryForm()
    setting = Setting.objects.get(pk=1)
    if request.method=='POST':
        category=CategoryForm(request.POST)
        if category.is_valid():
            category=category.save(commit=False)
            category.slug=slugify(category.title)
            category.save()

            messages.success(request, 'Your Category is added successfully')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, category.errors)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'add_category.html', {'category': category,'setting': setting})


def addarea(request):
    area=AreaForm()
    setting = Setting.objects.get(pk=1)
    if request.method=='POST':
        area=AreaForm(request.POST)
        if area.is_valid():
            area=area.save(commit=False)
            area.slug=slugify(area.title)
            area.save()

            messages.success(request, 'Your Area is added successfully')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, area.errors)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, 'add_area.html', {'area':area,'setting': setting})


@login_required(login_url='/login')
def addevent(request):
    eventform=EventForm()
    setting = Setting.objects.get(pk=1)
    if request.method=='POST':
        eventform = EventForm(request.POST,request.FILES)
        if eventform.is_valid():
            event=eventform.save(commit=False)
            event.user = request.user.userprofile
            event.slug=slugify(event.title)
            event.save()

            room=Room()
            room.event_id=event.id
            room.name=event.title
            room.slug=slugify(room.name)
            room.save()

            image=request.FILES.getlist('image')
            for img in image:
                Images.objects.create(event=event,image=img)

            video = request.FILES.getlist('video')
            for img in video:
                Video.objects.create(event=event, video=img)

            messages.success(request, 'Your event is added successfully')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, EventForm.errors)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return render(request,'addevent.html',{'eventform':eventform,'setting':setting})


@login_required(login_url='/login')
@csrf_exempt
def update_event(request,id):
    event = Event.objects.get(id=id)
    room=Room.objects.filter(event_id=id)
    setting = Setting.objects.get(pk=1)
    #print(event.user == request.user.userprofile)
    if event.user == request.user.userprofile:
        images = Images.objects.filter(event_id=id)
        video = Video.objects.filter(event_id=id)
        update=EventForm(instance=event)

        if request.method=='POST':
            category = request.POST.get('category')
            area = request.POST.get('area')
            title = request.POST.get('title')
            description = request.POST.get('description')
            keywords = request.POST.get('keywords')
            members = request.POST.get('members')
            status = request.POST.get('status')
            detail = request.POST.get('detail')
            start_time=request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            update = EventForm(request.POST, request.FILES, instance=event)
            if update.is_valid():
                print("saving")
                update = update.save(commit=False)
                update.slug = slugify(update.title)
                update.save()

                for i in room:
                    i.name=title
                    i.slug=slugify(i.name)
                    i.save()

                image = request.FILES.getlist('image')
                for img in image:
                    Images.objects.create(event=event, image=img)

                video = request.FILES.getlist('video')
                for img in video:
                    Video.objects.create(event=event, video=img)

                messages.success(request, 'Your event is added successfully')
                return HttpResponseRedirect('/event/viewmyevents')
            else:
                messages.warning(request, EventForm.errors)
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        return render(request, 'updateevent.html', {'event':event,'update':update,'images':images,'video':video,'setting':setting})
    else:
        messages.warning(request, 'You are not the organiser')
        return HttpResponseRedirect('/')


@login_required(login_url='/login')
def deleteimage(request,id):
    a=0
    setting = Setting.objects.get(pk=1)
    try:
        a=1
        print(request.META['HTTP_REFERER'])
    except KeyError:
        a=0
    if a==0:
        return render(request, '404-error.html', {'setting':setting})
    else:
        Images.objects.filter(id=id).delete()
        messages.success(request, 'Image is Deleted')
        print(request.META['HTTP_REFERER'])
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def deletevideo(request,id):
    a = 0
    setting = Setting.objects.get(pk=1)
    try:
        a = 1
        print(request.META['HTTP_REFERER'])
    except KeyError:
        a = 0
    if a == 0:
        return render(request,'404-error.html',{'setting':setting})
    else:
        Video.objects.filter(id=id).delete()
        messages.success(request, 'Video is Deleted')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def deletemyevent(request,id):
    setting = Setting.objects.get(pk=1)
    a = 0
    try:
        a = 1
        print(request.META['HTTP_REFERER'])
    except KeyError:
        a = 0
    if a == 0:
        return render(request, '404-error.html', {'setting':setting})
    else:
        Event.objects.filter(id=id).delete()
        messages.success(request, 'Event is Deleted')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def viewmyevent(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    event = Event.objects.filter(user=current_user.userprofile)
    context = {
        'event':event,'setting':setting
    }
    return render(request, 'viewmyevents.html', context)


@login_required(login_url='/login')
def event_detail(request,id,slug):
    event=Event.objects.get(pk=id)
    images=Images.objects.filter(event_id=id)
    video = Video.objects.filter(event_id=id)
    setting = Setting.objects.get(pk=1)
    comments=Comment.objects.filter(event_id=id,status='True')
    f=FAQ.objects.filter(event_id=id,status='True')
    comimg = CommentImages.objects.filter(event_id=id)
    a=0
    s=event.start_time
    t=datetime.now()
    if event.user == request.user.userprofile:
        a=2
    elif event.favorites.filter(id=request.user.id).exists():
        a=1
    else:
        a=0
    context = {'event':event,
               'images': images, 'comments': comments,
                'comimg': comimg,'video':video,'setting':setting,'a':a,'f':f
               }
    return render(request, 'eventdetails.html', context)


def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST,request.FILES)
      if form.is_valid():
         data = Comment()  # create relation with model
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.event_id=id
         current_user= request.user
         data.user_id=current_user.id
         event = Event.objects.get(id=data.event_id)
         data.save()  # save data to table
         image = request.FILES.getlist('image')
         for img in image:
            CommentImages.objects.create(event=event,comment=data, image=img)
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)


@login_required(login_url='/login')
def r_volunteer(request, id):
    event=Event.objects.get(pk=id)
    post = get_object_or_404(Event, id=id)
    data=Volunteers()
    if post.favorites.filter(id=request.user.id).exists():
        post.favorites.remove(request.user)
        event.members+=1
        event.save()
        Volunteers.objects.filter(event_id=id,user_id=request.user.id).delete()
        messages.success(request, "You are unregistered as volunteer")
    else:
        post.favorites.add(request.user)
        event.members-=1
        event.save()
        data.event_id=event.id
        data.user=request.user
        data.save()
        print('members',event.members)
        messages.success(request, "You are registered as volunteer")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def faq(request,id):
    url = request.META.get('HTTP_REFERER')
    setting = Setting.objects.get(pk=1)
    event=Event.objects.get(pk=id)
    faq = FAQ.objects.filter(status="True",event_id=id)

    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                data=FAQ()
                data.event_id=id
                data.question=form.cleaned_data['question']
                data.save()
                messages.success(request, 'Your Question is sent')
        except Exception as e:
            print(e)
            raise

    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def rooms(request,id,slug):
    setting=Setting.objects.get(pk=1)
    event = Event.objects.get(pk=id)
    rooms = Room.objects.filter(event=id,slug=slug)

    return render(request, 'rooms.html', {'rooms': rooms, 'event': event,'setting':setting})


@login_required(login_url='/login')
def volunteer_list(request,id):
    setting=Setting.objects.get(pk=1)
    event = Event.objects.get(id=id)
    if event.user == request.user.userprofile:
        new = Volunteers.objects.filter(event_id=id)
        return render(request, 'volunteer_list.html', {'new': new,'setting':setting})
    else:
        messages.warning(request,'You are not the organiser')
        return HttpResponseRedirect('/')


@login_required(login_url='/login')
def my_volunteer(request,id):
    setting=Setting.objects.get(pk=1)
    new = Volunteers.objects.filter(user_id=id)
    return render(request, 'my_volunteer.html', {'new': new,'setting':setting})


@login_required(login_url='/login')
def volunteered(request):
    setting = Setting.objects.get(pk=1)
    current_user=request.user
    volunteer=Volunteers.objects.filter(user_id=current_user.id)
    context={'setting':setting,'volunteer':volunteer}
    return render(request,'volunteer.html',context)


@login_required(login_url='/login')
def e_comments(request,id):
    setting=Setting.objects.get(pk=1)
    event = Event.objects.get(id=id)
    if event.user == request.user.userprofile:
        comment= Comment.objects.filter(event_id=id)
        return render(request,'commentlist.html',{'comment':comment,'setting':setting,'event':event})
    else:
        messages.warning(request,"You are not the organiser to see the comments")
        return HttpResponseRedirect('/')


@login_required(login_url='/login')
def e_comment_reply(request,id):
    comment = Comment.objects.get(id=id)
    setting=Setting.objects.get(pk=1)
    if comment.event.user == request.user.userprofile:
        coming = CommentImages.objects.filter(comment=comment)
        update = ReviewUpdate(instance=comment)
        if request.method == 'POST':
            update = ReviewUpdate(request.POST, instance=comment)
            if update.is_valid():
                update.save(commit=False)
                comment.note = True
                update.save()
                messages.success(request, 'Review is updated Successfully')
                return HttpResponseRedirect('/event/viewmyevents')
        return render(request, 'detail_reviews.html', {'update': update, 'comment': comment, 'coming': coming,'setting':setting})
    else:
        messages.warning(request,'You are not the organiser to reply to the comment')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def e_faq(request,id):
    setting=Setting.objects.get(pk=1)
    event = Event.objects.get(id=id)
    if event.user == request.user.userprofile:
        f= FAQ.objects.filter(event_id=id)
        return render(request,'faq.html',{'f':f,'setting':setting,'event':event})
    else:
        messages.warning(request,"You are not the organiser to see the comments")
        return HttpResponseRedirect('/')


@login_required(login_url='/login')
def e_faq_reply(request,id):
    setting=Setting.objects.get(pk=1)
    f = FAQ.objects.get(id=id)
    if f.event.user == request.user.userprofile:
        f= FAQ.objects.get(id=id)
        reply= ReplyForm(instance=f)
        if request.method == 'POST':
            reply=ReplyForm(request.POST,instance=f)
            if reply.is_valid():
                reply.save(commit=False)
                f.note=True
                reply.save()

                messages.success(request, 'FAQ is updated Successfully')
                return HttpResponseRedirect('/event/viewmyevents')
        return render(request,'faq_reply.html',{'f':f,'setting':setting,'reply':reply})
    else:
        messages.warning(request,"You are not the organiser to see the comments")
        return HttpResponseRedirect('/')

@login_required(login_url='/login')
def view_volunteer_profile(request,id):
    setting=Setting.objects.get(pk=1)
    user=User.objects.get(id=id)
    volunteer=Volunteers.objects.filter(user_id=user.id).count()
    organised=Event.objects.filter(user=user.userprofile).count()

    context={'user':user,'volunteer':volunteer,'organised':organised,'setting':setting}
    return render(request,'view_volunteer_profile.html',context)
