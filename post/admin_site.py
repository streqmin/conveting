from accounts.admin_site import jwt_admin_site
from .models import Post

jwt_admin_site.register(Post)
