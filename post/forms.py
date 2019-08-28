from captcha.fields import ReCaptchaField
from django import forms

from .models import Post, Comment, Contact, About  # !!!


# settings içine kaydedilen captcha yı buraya tanımladık.


class PostForm(forms.ModelForm):
    captcha=ReCaptchaField()

    # form dosyası içine sadece işlem değil işlem uygulanmayacak uygulamalar da konur.

    class Meta:
        model=Post
        fields=[
            'title',
            'content',
            'image',
            # eklediğimiz image alanı sayesinde artık form oluşturmak istersek altında resim seçme
            # butonu olacak.
        ]


# comment modelini web sayfalarında kullanabilmek için form modelini oluşturduk aşağıda.
class CommentForm(forms.ModelForm):
    captcha=ReCaptchaField()

    class Meta:
        model=Comment
        fields=[
            'name',
            'content',
        ]


class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=[
            'name',
            'messages',
            'email',
            'phone'
        ]


class AboutForm(forms.ModelForm):
    class Meta:
        model=About
        fields=[
            'name',
            'messages',
        ]