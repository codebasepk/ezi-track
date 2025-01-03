from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

admin.site.site_header = "EziTrack QMS"

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
