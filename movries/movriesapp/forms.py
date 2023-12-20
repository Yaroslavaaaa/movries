from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import *


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    age = forms.IntegerField(label='Возраст', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'age', 'email', 'password1', 'password2')



class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))



class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'age', 'avatar')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('com_text',)
        widgets = {
            'com_text': forms.Textarea(attrs={'placeholder': 'Введите комментарий', 'class': 'input-comment'}),
        }


class AnsCommentForm(forms.ModelForm):

    class Meta:
        model = CommentsAns
        fields = ('ans_com_text',)
        widgets = {
            'ans_com_text': forms.Textarea(attrs={'placeholder': 'Введите комментарий', 'class': 'input-ans-comment'}),
        }

class EditProfileForm:
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    username = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    age = forms.IntegerField(label='Возраст', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    avatar = forms.FileField(label="Аватар", widget=forms.FileInput(attrs={'class': 'avatar-input'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'age', 'email', 'avatar')
        widgets = {
            'com_text': forms.TextInput(attrs={'placeholder': 'Введите комментарий', 'class': 'input-comment'}),
        }