from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # OpenID Connect URLs
    path("oidc/", include("mozilla_django_oidc.urls")),
    # API endpoints
    path("api/customers/", include("customers.urls")),
    path("api/orders/", include("orders.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
