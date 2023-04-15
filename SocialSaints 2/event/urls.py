from django.urls import path

from . import views

urlpatterns = [
    path('add_category/',views.addcategory,name='add_category'),
    path('add_area/',views.addarea,name='addarea'),
    path('addevent/',views.addevent,name='addevent'),
    path('updateevent/<int:id>',views.update_event,name='updateevent'),
    path('viewmyevents/',views.viewmyevent,name='viewmyevent'),
    path('event_details/<int:id>/<slug:slug>', views.event_detail, name='event_details'),
    path('deleteimage/<int:id>',views.deleteimage,name='deleteimage'),
    path('deletevideo/<int:id>',views.deletevideo,name='deletevideo'),
    path('deletemyevent/<int:id>',views.deletemyevent,name='deletemyevent'),
    path('addcomment/<int:id>',views.addcomment,name='addcomment'),
    path('r_volunteers/<int:id>',views.r_volunteer,name='r_volunteers'),
    path('volunteer/<int:id>',views.volunteer_list,name='volunteer'),
    path('my_volunteer/<int:id>',views.my_volunteer,name='my_volunteer'),
    path('e_comments/<int:id>',views.e_comments,name='e_comments'),
    path('e_comments_reply/<int:id>',views.e_comment_reply,name='e_comment_reply'),
    path('volunteered',views.volunteered,name='volunteered'),
    path('room/<int:id>/<slug:slug>',views.rooms,name='room'),
    path('faq/<int:id>',views.faq,name='faq'),
    path('e_faq/<int:id>',views.e_faq,name='e_faq'),
    path('e_faq_reply/<int:id>',views.e_faq_reply,name='e_faq_reply'),
    path('view_volunteer_profile/<int:id>',views.view_volunteer_profile,name='view_volunteer_profile')

]