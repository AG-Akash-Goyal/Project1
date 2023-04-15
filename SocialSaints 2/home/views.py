from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string

from SocialSaints import settings
from home.models import Setting, FAQ, ContactForm, ContactMessage, Feedback
from django.contrib import messages
from home.forms import NewQuestionForm, SearchForm, CatForm
from event.models import Category, Area, Event, CommentImages, Video
from user.models import UserProfile
from django.http import HttpResponseRedirect, JsonResponse
import json,traceback
# Create your views here.


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    area = Area.objects.all()
    event = Event.objects.all()
    video = Video.objects.all().order_by('?')[:4]
    images = CommentImages.objects.all().order_by('?')[:6]
    context = {'setting': setting, 'category': category,
               'area': area, 'event': event, 'video': video, 'images': images}
    return render(request, 'test.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request, 'aboutus.html', context)


def contactus(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table

            template = render_to_string('contactmail.html', {'subject': data.subject, 'message': data.message,
                                                             'name': data.name, })
            email = EmailMessage(
                'Contact Message',
                template,
                data.email,
                [settings.EMAIL_HOST_USER],
            )
            email.fail_silently = False
            email.send()
            messages.success(
                request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/home/contactus')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm
    context = {'setting': setting, 'form': form, 'category': category}

    return render(request, 'contactus.html', context)


def gallery(request):
    setting = Setting.objects.get(pk=1)
    video = Video.objects.all()
    images = CommentImages.objects.all()
    context = {'setting': setting, 'images': images, 'video': video}
    return render(request, 'gallery.html', context)


def search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            areaid = form.cleaned_data['areaid']
            if query == '' and catid != 0 and areaid == 0:
                event = Event.objects.filter(category_id=catid)
            elif query == '' and catid == 0 and areaid != 0:
                event = Event.objects.filter(area_id=areaid)
            elif catid == 0 and areaid == 0:
                # SELECT * FROM product WHERE title LIKE '%query%'
                event = Event.objects.filter(title__icontains=query)
            elif areaid == 0 and catid != 0:
                event = Event.objects.filter(
                    title__icontains=query, category_id=catid)
            elif catid == 0 and areaid != 0:
                event = Event.objects.filter(
                    title__icontains=query, area_id=areaid)
            else:
                event = Event.objects.filter(
                    title__icontains=query, category_id=catid, area_id=areaid)

            category = Category.objects.all()
            area = Area.objects.all()
            context = {'event': event, 'query': query, 'area': area,
                       'category': category, 'setting': setting}
            return render(request, 'search_products.html', context)

    messages.warning(request, 'You dint enter the query')
    return HttpResponseRedirect('/')


def search_auto(request):
    query_original = request.GET.get('term')
    queryset = Event.objects.filter(title__icontains=query_original)
    mylist = []
    mylist += [x.title for x in queryset]
    print(mylist)
    return JsonResponse(mylist, safe=False)


def cat(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    event = Event.objects.all()
    area = Area.objects.all()
    context = {'event': event, 'setting': setting,
               'category': category, 'area': area}
    return render(request, 'eventlist.html', context)


def cat_display(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # check post
        form = CatForm(request.POST)
        if form.is_valid():
            catid = form.cleaned_data['catid']
            areaid = form.cleaned_data['areaid']
            if catid == 0 and areaid == 0:
                event = Event.objects.all()  # SELECT * FROM product WHERE title LIKE '%query%'
            elif catid == 0 and areaid != 0:
                event = Event.objects.filter(area_id=areaid)
            elif catid != 0 and areaid == 0:
                event = Event.objects.filter(category_id=catid)
            else:
                event = Event.objects.filter(category_id=catid, area_id=areaid)

            category = Category.objects.all()
            area = Area.objects.all()
            context = {'event': event, 'area': area,
                       'category': category, 'setting': setting}
            return render(request, 'eventlist.html', context)

    return HttpResponseRedirect('/')


def feedback(request):
    if request.method == "GET":
        eid = int(request.GET.get("eid", -1))
        setting = Setting.objects.get(pk=1)
        type = "Event" if eid >= 0 else "Website"
        return render(request, "feedback.html", {
            'setting': setting,
            'type': type,
            'eid': eid
        })
    elif request.method == "POST":
        try:
            feedback = Feedback.objects.create()
            feedback.head = request.POST["head"]
            feedback.desc = request.POST["desc"]
            eid = int(request.POST["eid"])
            if eid >= 0:
                feedback.eid = Event.objects.get(pk=eid)
                feedback.type = "Event"
            else:
                feedback.eid = null
                feedback.type = "Website"
            feedback.uid = UserProfile.objects.get(user=request.user)
            feedback.save()
            messages.info(request,"Thanks for the feedback")
        except Exception as e:
            traceback.print_exc()
            messages.error(request,"Error Saving Feedback",e)
        return HttpResponseRedirect("/")
