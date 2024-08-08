from django.contrib import admin
from django.urls import path, include
from .views import Home

from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('app/', include('users.urls')),
    path('freelancer/', include('freelancer.urls')),
    path('recruiter/', include('recruiter.urls')),
    path('messages/', include("messagesApp.urls")),
    path('', Home.as_view(), name="homepage"),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    