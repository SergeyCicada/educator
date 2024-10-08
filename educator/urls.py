from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from educator import settings
from main.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('employees/', include('main.urls')),
    path('', include('accounts.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path("api/", include("educator_api.urls")),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

