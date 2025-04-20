from accounts.admin_site import jwt_admin_site
from .models import DiseaseInfo, Prediction

jwt_admin_site.register(DiseaseInfo)
jwt_admin_site.register(Prediction)