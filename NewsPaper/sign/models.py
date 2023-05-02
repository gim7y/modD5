from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# форма, с помощью которой мы будем создавать нового
#  пользователя:
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )
# Для облегчения создания нового пользователя в модуле
# аутентификации есть базовая форма (с валидацией и проверкой).
# По умолчанию она имеет только поле username и два поля пароля
# — сам пароль и его подтверждение.
# Здесь расширили форму, добавив другие значимые поля:
# * электронная почта + имя + фамилия нового пользователя.
# Эти поля есть в самой встроенной модели User, поэтому мы можем
# получить эти поля «бесплатно».

#  В идеале этот код (скрипт относящиеся к формам) нужно хранить в отд.
#  файле forms.py, но сейчас это не принципиально.

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
