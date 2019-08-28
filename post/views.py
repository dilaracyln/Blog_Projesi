from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.utils.text import slugify  # !!!

from .forms import PostForm, CommentForm, ContactForm  # !!!
from .models import Post


def post_index(request):
    post_list=Post.objects.all()
    # post liste ile tüm nesneleri çektik.
    query=request.GET.get('q')
    if query:
        # arama çubuğuna değer girilmiş mi diye bir if kontrolu koyduk.
        # eğer değer geliyorsa onu alt kısımdan filtreledik.
        # şayet altta query yerine dilara yazmış olsaydık bize title alanında dilara yazan her postu getirirdi.
        post_list=post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
        # bu filtreleme sayesinde arama çubuğuna yazılan başlık metin yazar adı ve soyadı yazıldığında bize alakalı postları
        # listeler. En sona yazılan distinct fonk.u listelenen aynı postların 1 kez görünmesini sağlar.

    paginator=Paginator(post_list, 5)
    # çekilen nesneleri ve kaç nesne çekileceğini parametre olarak vermiş. yani her sayafada 5 tane post nesnesi gelecek.
    page=request.GET.get('sayfa')
    # page ile kullanıcının kaçıncı sayfayı istediği bilgisi çekilir.
    # index.html de page kısmını sayfa yapmıştık. burada da uygulayarak arama motorunda sayfa yazdırırız.

    try:
        posts=paginator.page(page)
        # parantez içindeki page kısmına sayfa bilgisi girilerek sadece ilgili nesneler getirilir. yani bizim kodumuzda 5 değer getirilir.
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts=paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts=paginator.page(paginator.num_pages)

    return render(request, "post/index.html", {'posts': posts})


# yorumlar postların detay kısmında oluşturulacağı için biz de detail kısmına yazdık.
def post_detail(request, slug):
    post=get_object_or_404(Post, slug=slug)

    form=CommentForm(request.POST or None)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        # yorumların hangi posta ait oldugunu belirtir yukarıdaki yapı.
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())
    # kullanıcılar yorum yaptıktan sonra tekrar aynı sayafaya yönlendirebilmek için yukarıdaki yapıyı yazdık.

    context={
        'post': post,
        'form': form,
    }
    return render(request, "post/detail.html", context)


def post_create(request):
    if not request.user.is_authenticated:
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()
    # bu if ile başlayan 2 satırlık kodu delete ve update kısmına da kopyaladık. bu kod sayesinde kullanıcı olmayan kişi arama motorunda post/create yapsa bile karşısına form çıkmayacak. error verecek sayfa.

    form=PostForm(request.POST or None, request.FILES or None)
    # upload edilen resim request.files dan gelir. sol taraf yazı için sağ taraf resim için çalışır. resim upload edilmemişse de kodun çalışması için or none ifadesi de koyduk.
    if form.is_valid():
        post=form.save(commit=False)
        # o an hangi kullanıcı post yazıyorsa o kullanıcıyı yazar olarak atadık.kullanıcı zorunlu bi alan olduğu için nesneyi kaydetmeden önce kullanıcıyı belirlememiz gerekiyor. bunun için commit=false parametresini kullanıyoruz. save metodu formdan aldıgı bilgilerle beraber bize o nesneyi geri döndürür ama o nesneyi veritabanına eklemez.
        post.slug=slugify(post.title.replace('ı', 'i'))
        # bu sayede slug alanında türkçe karakterin de benimsenmesini sağlarız.
        post.user=request.user
        # request nesnesinin de yardımıyla istek yapan kullanıcıyı getiriyoruz ve onu yazar olaraka kullanıyoruz.
        post.save()
        messages.success(request, "Başarılı bir şekilde oluşturdunuz.", extra_tags='mesaj-basarili')
        return HttpResponseRedirect(post.get_absolute_url())

    context={
        'form': form
    }

    return render(request, "post/form.html", context)


def post_update(request, slug):
    if not request.user.is_authenticated():
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()

    post=get_object_or_404(Post, slug=slug)
    form=PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Başarılı bir şekilde güncellediniz.")
        return HttpResponseRedirect(post.get_absolute_url())

    context={
        'form': form
    }

    return render(request, "post/form.html", context)


def post_delete(request, slug):
    if not request.user.is_authenticated:
        # Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
        return Http404()

    post=get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect("post:index")

