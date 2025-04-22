from accounts.admin_site import jwt_admin_site
from .models import Dog

jwt_admin_site.register(Dog)
