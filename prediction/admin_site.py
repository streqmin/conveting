from accounts.admin_site import jwt_admin_site
from .models import DiseaseInfo

jwt_admin_site.register(DiseaseInfo)
