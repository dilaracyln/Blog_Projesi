import os

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #

SECRET_KEY='l-qq%e!ll9@u7g(yegilxideh)v(u!v61crlfcvfx-#nn8zs4s'

DEBUG=True

ALLOWED_HOSTS=['*']

INSTALLED_APPS=[
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # kendi uygulamalarım
    'post',
    # 3.parti uygulamalar

    'crispy_forms',
    'django_cleanup',
    # terminale yazılan pip install django-cleanup ve buraya yazılan üstteki yazıyla artık resimli post silindiğinde içindeki media klasorüne kaydedilmiş resim de silinir.
    'ckeditor',
    'captcha',
    'cls',
    'rest',
]

MIDDLEWARE=[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF='blog.urls'

TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION='blog.wsgi.application'

DATABASES={
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'blogdeneme',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS=[
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE='tr'

TIME_ZONE='Europe/Istanbul'

USE_I18N=True

USE_L10N=True

USE_TZ=True

STATIC_URL='/static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, "static"),

]

STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles/')

MEDIA_URL='/media/'
# buradaki medya kullanıcıların upload ettiği fotograf dosyalarını temsil eder.
MEDIA_ROOT=os.path.join(BASE_DIR, 'media')
# upload edilen dosyaların projede media isimli bir doyada bulunmasını sağladık yoksa fotolar kök dizinde kalırdı.

CRISPY_TEMPLATE_PACK='bootstrap3'

CKEDITOR_JQUERY_URL=os.path.join(STATIC_URL, 'js/jquery.min.js')
CKEDITOR_CONFIGS={
    'default': {
        # 'toolbar': 'full', #toolbar: full etiketi form için oluşturulan yazı özelliklerinin hepsini eklemeni sağlar ama nbu karışıklık yaratır.
        # 'height': 300,
        'width': '100%',
        # width ile form dosyasına eklenen yazi biçimleri tablosunun genişliğini sayfaya tam otuttururuz.
    },
}
RECAPTCHA_PUBLIC_KEY='6Lfsm6gUAAAAAIYoH3amFpz9eUMfhIR_4FS-pMit'
RECAPTCHA_PRIVATE_KEY='6Lfsm6gUAAAAAB-Y48qUOfMbuK1vNruHU7u5xR6e'
NOCAPTCHA=True
# captcha formüllerini buraya eklemeden önce terminale pip install django-recaptcha yazarız.
# installed apps kısmında captcha yı ekledik.
# captcha sıtesinden alınan şifreleri ekliyoruz.
# nocaptcha kısmı bıze kutucuğun 'ben robot değilim' kısmına tek tıkla güvenlik sistemini aşmamızı sağlar.
