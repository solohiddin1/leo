from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from root import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('apps.user.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.conf import settings as django_settings

    urlpatterns += [
        path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/v2/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)