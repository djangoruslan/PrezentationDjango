from captcha.fields import CaptchaField

from django import forms

from .models import Comment


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'post': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'post': forms.HiddenInput}