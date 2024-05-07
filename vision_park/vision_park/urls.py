from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_control
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve

from . import views
from . import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.main, name='main'),
    path('auth/', include('accounts.urls')),
    path('parking_area/', include('parking_area.urls')),
    path('recognize/', include('recognize.urls')),
    # path("cars/", include("cars.urls")),
    # path("photos/", include("photos.urls")),
    # path("finance/", include("finance.urls")),
    # path("communications/", include("communications.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)