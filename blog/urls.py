from django.conf import settings  # !!!
from django.conf.urls import url, include
from django.conf.urls.static import static  # !!!
from django.contrib import admin

from home.views import home_view, iletisim, hakkimda

urlpatterns=[
                url(r'^$', home_view, name='home'),
                url(r'^post/', include('post.urls')),
                url(r'^accounts/', include('accounts.urls')),
                url(r'^rest/', include('rest.urls')),
                # üyelik sistemi için account içinde oluşturudugumuz url dosyasını kaydettik.
                # yani projenin url dosyasında belirttik.
                url(r'^admin/', admin.site.urls),
                url(r'^iletisim/', iletisim, name='iletisim'),
                url(r'^hakkimda/', hakkimda, name='hakkimda'),

            ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# yani media url ve media root değişkenlerini kullanarak upload edilecek dosyaların url tanımlamasını yaptık.
