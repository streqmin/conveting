from accounts.admin_site import jwt_admin_site
from .models import AnimalHospital

jwt_admin_site.register(AnimalHospital)
