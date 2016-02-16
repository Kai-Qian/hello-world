from django import forms
from socialnetwork.models import *
from django.contrib.auth.models import User


# class RegistrationForm(forms.Form):
#     username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-username form-control', 'placeholder': 'Username'}))
#     firs_tname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-username form-control', 'placeholder': 'First name'}))
#     last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-username form-control', 'placeholder': 'Last name'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-username form-control', 'placeholder': 'Email address'}))
#     password1 = forms.CharField(max_length=200, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-password form-control', 'placeholder': 'Password'}))
#     password2 = forms.CharField(max_length=200, label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-password form-control', 'placeholder': 'Password'}))
#
#     def clean(self):
#         cleaned_data = super(RegistrationForm, self).clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords did not match")
#
#         return cleaned_data
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username__exact=username):
#             raise forms.ValidationError('Username is already taken')
#
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email__exact=email):
#             raise forms.ValidationError('Email address is already taken')
#
#         return email


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=20,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(max_length=200, label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-password form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=200, label="Confirm password", widget=forms.PasswordInput(
        attrs={'class': 'form-password form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError('Username is already taken')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError('Email address is already taken')

        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        }


class ExtraUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'age', 'picture')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': '4', 'class': 'form-control', 'placeholder': 'Bio'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
        }

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 430:
            raise forms.ValidationError('Bio is too long')

        return bio

    def clean_age(self):
        age = self.cleaned_data.get('age')
        try:
            int(age)
        except ValueError:
            raise forms.ValidationError('Age must be a number')

        return age
