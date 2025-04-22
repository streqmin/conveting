from accounts.admin_site import jwt_admin_site
from .models import Post, PostLike, Comment, CommentLike

jwt_admin_site.register(Post)
jwt_admin_site.register(PostLike)
jwt_admin_site.register(Comment)
jwt_admin_site.register(CommentLike)
