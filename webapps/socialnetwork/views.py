# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.urlresolvers import reverse
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
import json
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from socialnetwork.models import *
from socialnetwork.forms import *


@login_required
def home(request):
    context = {}
    postings = Posting.objects.order_by('-dateAndTime')
    context['postings'] = postings
    return render(request, 'home.html', context)


@login_required
@transaction.atomic
def profile(request):
    postings = Posting.objects.filter(user=request.user)
    user = User.objects.get(username=request.user)
    user_form = UserProfileForm(instance=user)# if you use instance, the content will be shown in the form
    try:
        up = Profile.objects.get(user=user)
    except:
        up = None
    profile_form = ExtraUserProfileForm(instance=up)

    return render(request, 'profile.html',
                  {'postings': postings, 'user_form': user_form, 'profile_form': profile_form, 'profile': up})


@login_required
@transaction.atomic
def post(request):
    context = {}
    errors = []
    postings = request.POST['post']
    p = postings.split()
    length = len(p)
    if length > 160:
        errors.append("There should only be 160 words.")
        context['errors'] = errors
        return render(request, 'profile.html', {'postings': postings})
    elif 0 < length <= 160:
        posting = Posting.objects.create(text=postings, user=request.user)
        posting.save()
        return redirect(reverse('home'))


@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':# when the register page is loaded, it will first send the GET request to load the page
        context['user_form'] = UserForm()
        return render(request, 'register.html', context)
    # user = User()
    user_form = UserForm(request.POST)  # , instance=user)#I try to use instance to create the object, but the authenticate failed, so i have to use old method.
    profile_form = ExtraUserProfileForm()# maybe it is better to use old method, ie create the object through cleaned_data,  for register
    context['user_form'] = user_form

    if not user_form.is_valid():
        return render(request, 'register.html', context)
    new_user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                        password=user_form.cleaned_data['password'],
                                        first_name=user_form.cleaned_data['first_name'],
                                        last_name=user_form.cleaned_data['last_name'],
                                        email=user_form.cleaned_data['email'])
    new_user.save()
    # user_form.save()  # only after form save, the user has object

    profile = profile_form.save(commit=False)
    profile.user = new_user# link the user
    profile.save()
    # Logs in the new user and redirects to his/her todo list
    user = authenticate(username=user_form.cleaned_data['username'],
                        password=user_form.cleaned_data['password'])
    # user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect(reverse('home'))

@login_required
@transaction.atomic
def editprofile(request):
    context = {}
    postings = Posting.objects.filter(user=request.user)
    context['postings'] = postings
    user = User.objects.get(username=request.user)
    user_form = UserProfileForm(request.POST, instance=user)
    try:
        up = Profile.objects.get(user=user)
    except:
        up = None
    profile_form = ExtraUserProfileForm(request.POST, instance=up)
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    if not user_form.is_valid() or not profile_form.is_valid():
        return render(request, 'profile.html', context)

    profile = profile_form.save(commit=False)
    profile.user = user
    if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']
    context['profile'] = profile
    user_form.save()
    profile.save()
    return render(request, 'profile.html', context)


# follow(request, username)'s content is mainly cite from "Learning Djngo Web Development", have some modifications
# https://books.google.com/books?id=Xs_2CQAAQBAJ&pg=PA146&lpg=PA146&dq=django+follow+unfollow&source=bl&ots=tKwWI68tcK&sig=h5Nc7ny6vT6MLJFPjZS2bN2C6n0&hl=zh-CN&sa=X&ved=0ahUKEwin5s-6j_jKAhWPsh4KHYzxBvI4ChDoAQgpMAI#v=onepage&q&f=false
@login_required
@transaction.atomic
def follow(request, username):
    if request.method == 'GET':
        params = {}
        user = User.objects.get(username=username)
        postings = Posting.objects.filter(user=user)
        post = postings[0]
        user_form = UserProfileForm(instance=user)
        try:
            up = Profile.objects.get(user=user)
        except:
            up = None
        profile_form = ExtraUserProfileForm(instance=up)
        params['onepost'] = post
        params['postings'] = postings
        params['user_form'] = user_form
        params['profile_form'] = profile_form
        params['profile'] = up
        userProfile = User.objects.get(username=request.user.username)# First get the request user, ie the logged in user
        try:
            userFollowing = Followings.objects.get(user=userProfile)# use the user to get the Followings object
            print userFollowing
            print username
            if userFollowing.followings.filter(username=username).exists():# use Followings object to get the followings field, then you can treate it as a field, use all or filter ans so on
                print 1
                params["following"] = True
            else:
                print 2
                params["following"] = False
        except:
            userFollower = []

        # params["profile"] = userProfile
        return render(request, 'otherProfile.html', params)

    if request.method == 'POST':
        follow = request.POST['follow']
        user = User.objects.get(username=request.user.username)
        userProfile = User.objects.get(username=username)
        userFollowing, status = Followings.objects.get_or_create(user=user)
        if follow == 'true':
            # follow user
            userFollowing.countForFollowings += 1
            userFollowing.followings.add(userProfile)# add and remove can deal with object i the field
        else:
            # unfollow user
            userFollowing.countForFollowings -= 1
            userFollowing.followings.remove(userProfile)
        userFollowing.save()
        return HttpResponse(json.dumps(""), content_type="application/json")

@login_required
@transaction.atomic
def followerStream(request):
    context = {}
    postings = []
    user = User.objects.get(username=request.user.username)  # myself
    following, status = Followings.objects.get_or_create(user=user)
    print following.followings.all()
    for usr in following.followings.all():
        posting = Posting.objects.filter(user=usr).order_by('-dateAndTime')
        for i in posting:
            postings.append(i)
    context['postings'] = postings
    return render(request, 'followings.html', context)
