
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Sanza library"
admin.site.site_title = "Sanza ebook"
admin.site.index_title = "Welcome to Sanza library"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)