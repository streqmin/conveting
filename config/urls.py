from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import index, AdminJWTLoginView
from accounts.admin_site import jwt_admin_site
import dogs.admin_site
import prediction.admin_site
import post.admin_site


urlpatterns = [
    path("admin/login/", AdminJWTLoginView.as_view(), name="admin_jwt_login"),
    path("admin/", jwt_admin_site.urls),
    path("", index),
    path("accounts/", include("accounts.urls")),
    path("dogs/", include("dogs.urls")),
    path("prediction/", include("prediction.urls")),
    path("post/", include("post.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
