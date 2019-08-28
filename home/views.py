from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, Http404
from django.urls import reverse

from post.forms import ContactForm, AboutForm


def home_view(request):
    if request.user.is_authenticated:
        context={
            'isim': 'Barış'
        }
    else:
        context={
            'isim': 'Misafir Kullanıcı'
        }
    return render(request, 'home.html', context)


def iletisim(request):
    if not request.user.is_authenticated:
        return Http404()

    form=ContactForm(request.POST or None)

    if form.is_valid():
        contact=form.save(commit=False)
        contact.save()
        messages.success(request, "Başarılı bir şekilde oluşturdunuz.", extra_tags='mesaj-basarili')
        return HttpResponseRedirect(reverse('iletisim'))

    return render(request, 'post/contact.html')

def hakkimda(request):
    if not request.user.is_authenticated:
        return Http404()

    form=AboutForm(request.POST or None)

    if form.is_valid():
        about=form.save(commit=False)
        about.save()
        return HttpResponseRedirect(reverse('hakkimda'))

    return render(request, 'post/about.html')


