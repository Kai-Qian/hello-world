from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Posting(models.Model):
    text = models.CharField(max_length=160)
    dateAndTime = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return self.__unicode__()

    class Meta:  # ordering descending
        ordering = ['-dateAndTime']


class Profile(models.Model):
    # Required: link a Profile to User.
    user = models.OneToOneField(User)
    # The additional attributes we wish to include.
    bio = models.CharField(max_length=430, blank=True)
    age = models.CharField(max_length=4, blank=True)
    picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __unicode__(self):
        return self.user.username


class Followings(models.Model):
    followings = models.ManyToManyField(User, related_name="followings")# I follow others
    user = models.ForeignKey(User, unique=True, related_name="user")
    countForFollowings = models.IntegerField(default = 0)

    def __unicode__(self):
        return '{}: {}'.format(self.user, self.countForFollowings)

    def __str__(self):
        return self.__unicode__()
