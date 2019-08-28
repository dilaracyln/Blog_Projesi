from ckeditor.fields import RichTextField  # !!!
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    user=models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    # bu üstteki kod ile her postun yazarı ve bilgilerine ulaşabileceğiz.
    # böylece her post yazacağımız zaman üst kısımda bir buton çıkar ve user seçebiliriz.
    title=models.CharField(max_length=120, verbose_name='başlık')
    content=RichTextField(verbose_name='İçerik')
    # içerik kısmına yazı yazılan yerin üstüne bir sürü yazı özelliği ekler.
    publishing_date=models.DateTimeField(verbose_name='yayımlanma tarihi', auto_now_add=True)
    image=models.ImageField(null=True, blank=True)
    # bu kod sayesinde postlar için bir resim alanı oluşturduk. parantez içine yazılan ifadeler bu alanı doldurmanın
    # zorunlu olmadığını yani boş geçilebileceğini söyler. yani resmi isteğe bağlı oluşturabiliriz.
    slug=models.SlugField(unique=True, editable=False, max_length=130)

    # unique= true dedik çünkü artık adreslerimizde ip yerine slug kullanacağız. ve her adresimizin de slug'ı farklı
    # olacağı için veritabanını silip yeni bir veri tabanı olusturuyoruz. eski veritabanını silmek için dbsqlite'ı
    # ve post/migrations dosyalarındaki sayıyla başlayan dosyaları sileriz.
    # sonrasında terminalde makemigrations ve migrate yaparız. sonra createsuperuser ile admin oluştururuz.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('post:create', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post:update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post:delete', kwargs={'slug': self.slug})

    # index.html sayfasına yazdığımız sil güncelle vb. kodları fonksiyona çevirdik ve bu fonksiyonları kullanarak onları çağırdık.

    def get_unique_slug(self):
        slug=slugify(self.title.replace('ı', 'i'))
        unique_slug=slug
        counter=1
        while Post.objects.filter(slug=unique_slug).exists():
            # while döngüsünde kullanmak için counter adında bir değişken atadık.
            # filter kullanarak veritabında daha önce böyle bir slug alanı olup olmadığını tanımladık.
            # exists:var mı yok mu demek. eğer filter metodundan nesne dönüyorsa true olur ve while tekrar çalışır.
            unique_slug='{}-{}'.format(slug, counter)
            # her dönüşte counter 1 artar. ve counter değişkeni slug dizisinin sonuna eklenir.
            counter+=1
            return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            # eğer slug alanı boşsa slug alanını doldur komutu verdik.
            self.slug=self.get_unique_slug()
            # bu alan yukarıda en son elde edilen eşsiz unique slug değerini döndürür.
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering=['-publishing_date', 'id']
        # bu sınıf sayesinde sıralama(ordering) yaparken yayımlanma tarihini baz alarak anasayfada postlar sıralanır. yani en eklenen post en başta görünür.
        # tarihin başındaki tre ile en son oluşturulan en başa gelir.
        # id ifadesi ile tarihleri aynı olan nesnelerin id alanına bakılır ve küçükten büyüğe doğru sıralaanır.


# post gönderilerine ziyaretçilerin yorum yazabilmesi için kullanılan alan.
class Comment(models.Model):
    post=models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    # bir postun birden fazla yorumu olabilir ama bir yorum bir posta aittir. bu yüzden foreignkey kullandık.
    # diyelim ki bir post'a birden fazla yorum geldi. o post silinince tüm yorumların da silinmesi için
    # cascade i kullandık.
    name=models.CharField(max_length=200, verbose_name='Ad Soyad')
    content=models.TextField(verbose_name='Yorum')
    # yorumu yapacak kişinin adı soyadı ve yorum kısmının sorgulandığı yer.
    created_date=models.DateTimeField(auto_now_add=True)

    # auto now add nesnesine true vererek tarih bilgisini otomatik doldurmasını sağladık.

    # return "/post/{}".format(self.id)

    def __str__(self):
        return self.name


class Contact(models.Model):
    created_date=models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=200, null=True, blank=True, verbose_name='Ad Soyad')
    phone=models.CharField(max_length=200, null=True, blank=True, verbose_name='Telefon')
    email=models.CharField(max_length=200, null=True, blank=True, verbose_name='Eposta')
    messages=models.TextField(null=True, blank=True, verbose_name='Mesajınız')

    def __str__(self):
        return self.name


class About(models.Model):
    name=models.CharField(max_length=200, verbose_name='Ad Soyad')
    messages=models.TextField(verbose_name='Mesajınız')

    def __str__(self):
        return self.name
