from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#UserCreationForm 클래스를 상속하고 email 속성을 추가.
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")