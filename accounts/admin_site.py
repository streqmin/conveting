from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()


class JWTAdminSite(AdminSite):
    site_header = "JWT Admin"
    site_title = "Admin Portal"
    index_title = "Welcome to the Admin Panel"

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.is_staff

    def login(self, request, extra_context=None):
        return redirect("admin_jwt_login")


jwt_admin_site = JWTAdminSite(name="jwt_admin")
jwt_admin_site.register(User)
