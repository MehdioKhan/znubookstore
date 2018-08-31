from django.contrib import admin
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'', include('store.urls')),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
