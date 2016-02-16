"""InClassExercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^$', auth_views.login, {'template_name':'login.html'}, name='login2'),
    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^follow/(\w+)/$','socialnetwork.views.follow', name='follow'),
    url(r'^register', 'socialnetwork.views.register', name='register'),
    url(r'^home', 'socialnetwork.views.home',name='home'),
    url(r'^post', 'socialnetwork.views.post', name='post'),
    url(r'^profile', 'socialnetwork.views.profile',name='profile'),
    url(r'^editprofile', 'socialnetwork.views.editprofile',name='editprofile'),
    url(r'^otherProfile/(\w+)/$', 'socialnetwork.views.follow',name='follow'),
    url(r'^followerStream', 'socialnetwork.views.followerStream',name='followerStream'),
    url(r'^logout$', auth_views.logout_then_login,name='logout'),
]
