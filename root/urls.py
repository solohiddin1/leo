from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from apps.shared.utils.swagger import (
    ProtectedSpectacularAPIView,
    ProtectedSpectacularRedocView,
    ProtectedSpectacularSwaggerView,
)
from root import settings

urlpatterns: list[URLPattern | URLResolver] = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/user/", include("apps.user.urls")),
    path("api/v1/product/", include("apps.product.urls")),
    path("api/v1/shared/", include("apps.shared.urls")),
    path("api/v1/transaction/", include("apps.transaction.urls")),
    path("api/v1/order/", include("apps.order.urls")),
]

if settings.DEBUG:
    from django.conf import settings as django_settings
    from django.conf.urls.static import static

    urlpatterns += [
        path("api/v1/schema/", ProtectedSpectacularAPIView.as_view(), name="schema"),
        path(
            "api/v1/swagger/",
            ProtectedSpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/v1/redoc/",
            ProtectedSpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]

    urlpatterns += static(
        django_settings.MEDIA_URL, document_root=django_settings.MEDIA_ROOT
    )
