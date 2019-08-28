from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .form import LoginForm, RegisterForm


def login_view(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        # kullanıcı formu başarılı bir şekilde doldurmuşsa giriş işlemlerini doldurur bu kodla. formdan gelen kullanıcı adı ve şifreyi bir değişkene atadık.
        # cleaned data metodu, form.is_valid metodu true olarak döndüğü zaman kullanabileceğimiz bir metod.buunu kullanarak kullanıcıdan gelen bilgilerin doğruluğunu teyit ederek getirmiş oluruz.
        # bu kullanıcının sisteme giriş yapması için authenticated ve login metodlarını kullandık ama önce import ettik.
        # kullanıcıyı sisteme dahil etmeden önce girilen bilgilerin doğruluğundan emin olmak için authenticated ve login metodlarını kullandık.
        user=authenticate(username=username, password=password)
        # eğer böyle bir kullanıcı sistemde kayıtlıysa authenticate metodu geriye user nesnesi döbndürür. değilse hata verir.
        login(request, user)
        return redirect('home')
    # kullanıcıyı sisteme login metoduyla dahil ederiz. return ile giriş yapan kullanıcıyı anasayfaya yönlendiririz. yukarıdan redirect metodunu import ederiz.

    return render(request, 'accounts/form.html', {'form': form, 'title': 'Giriş Yap'})


def register_view(request):
    form=RegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password1')
        user.set_password(password)
        user.is_staff=user.is_superuser=True
        user.save()
        new_user=authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('home')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Üye Ol'})


def logout_view(request):
    logout(request)
    return redirect('home')
