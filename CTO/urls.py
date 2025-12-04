from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/v1/niveau1/", include("niveau1.urls")),
    path("api/v1/niveau2/", include("niveau2.urls")),
    path("api/v1/niveau3/", include("niveau3.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)