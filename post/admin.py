from django.contrib import admin

# Register your models here.
# from.models import  Post
from post.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publishing_date', 'slug']
    #buraya yazdığımız slug alanı ile oluşturulan postların sağında slug diye bir alan oluşur
    #ve burası oluşturulan postun başlığı gösterir.
    list_display_links = ['publishing_date']
    list_filter = ['publishing_date']
    search_fields = ['title', 'content']
    list_editable = ['title']
    #slug alanını title alanına referans oalrak verdik. bu sayede post ekleme kısmında slug
    #alanını doldurmak artık zorunlu değil. çünkü başlık alanına yazılan karakter otomatik
    #olarak slug alanına da yazılır.
    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
