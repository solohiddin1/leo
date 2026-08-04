from root import settings
from django.contrib import admin
from django.urls import path, include, URLPattern, URLResolver

from apps.shared.utils.swagger import ProtectedSpectacularSwaggerView, ProtectedSpectacularRedocView, ProtectedSpectacularAPIView

urlpatterns: list[URLPattern | URLResolver] = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/user/', include('apps.user.urls')),
    path('api/v1/product/', include('apps.product.urls')),
    path('api/v1/shared/', include('apps.shared.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.conf import settings as django_settings

    urlpatterns += [
        path('api/v1/schema/', ProtectedSpectacularAPIView.as_view(), name='schema'),
        path('api/v1/swagger/', ProtectedSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/v1/redoc/', ProtectedSpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

    urlpatterns += static(django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT)