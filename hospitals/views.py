# hospitals/views.py
import math
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import AnimalHospital


def nearest_hospitals_api(request):
    """
    JSON API: ?lat=...&lng=...
    """
    try:
        user_lat = float(request.GET["lat"])
        user_lng = float(request.GET["lng"])
    except (KeyError, ValueError):
        return JsonResponse({"error": "lat, lng 파라미터가 필요합니다."}, status=400)

    qs = AnimalHospital.objects.exclude(latitude__isnull=True)
    data = []
    for h in qs:
        dist = haversine(user_lat, user_lng, h.latitude, h.longitude)
        data.append(
            {
                "name": h.name,
                "address": h.full_address or h.raw_address,
                "phone": h.phone,
                "distance": round(dist, 2),
            }
        )

    sorted_list = sorted(data, key=lambda x: x["distance"])[:20]
    return JsonResponse(sorted_list, safe=False)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 지구 반경(km)
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    dφ = math.radians(lat2 - lat1)
    dλ = math.radians(lon2 - lon1)
    a = math.sin(dφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(dλ / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class NearestHospitalsView(LoginRequiredMixin, TemplateView):
    template_name = "hospitals/nearest.html"

    def get(self, request, *args, **kwargs):
        # lat/lng 파라미터가 있으면 API 함수 호출
        if request.GET.get("lat") and request.GET.get("lng"):
            return nearest_hospitals_api(request)
        # 없으면 템플릿 렌더
        return super().get(request, *args, **kwargs)
