"""SocialSaints URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from home import views
from event import views as eventviews
from user import views as UserViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('home/',include('home.urls')),
    path('event/',include('event.urls')),
    path('user/',include('user.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('login/',UserViews.login_form,name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reenter.html'),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name="password_reset_complete"),
    path('signup/', UserViews.signup_form, name='signup'),
    path('logout/', UserViews.logout_func, name='logout'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('categoryproduct/',views.cat_display,name='cat_display'),
    path('cat/',views.cat,name="cat"),
    path('rooms/', include('room.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
