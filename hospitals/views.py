# hospitals/views.py
import math
import googlemaps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import AnimalHospital

# 지구 위 두 점 사이 거리 계산 (km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    dφ = math.radians(lat2 - lat1)
    dλ = math.radians(lon2 - lon1)
    a = math.sin(dφ/2)**2 + math.cos(φ1)*math.cos(φ2)*math.sin(dλ/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def nearest_hospitals_api(request):
    """
    JSON API: ?lat=...&lng=...
    1) 거리 계산 → 2) 상위 10개 선별 → 3) 각각 사진 fetch
    """
    try:
        user_lat = float(request.GET["lat"])
        user_lng = float(request.GET["lng"])
    except (KeyError, ValueError):
        return JsonResponse({"error": "lat, lng 파라미터가 필요합니다."}, status=400)

    # 1) DB에서 위도/경도 있는 병원만
    qs = AnimalHospital.objects.exclude(latitude__isnull=True, longitude__isnull=True)

    # 2) 거리 계산
    dist_list = []
    for h in qs:
        d = haversine(user_lat, user_lng, h.latitude, h.longitude)
        dist_list.append((h, d))

    # 3) 거리순 정렬 후 상위 10개만
    top_n = sorted(dist_list, key=lambda x: x[1])[:10]

    # 4) Google Maps 클라이언트 초기화
    gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

    result = []
    for h, dist in top_n:
        photo_url = None
        try:
            # 이름＋주소로 텍스트 검색 → photos 필드
            place = gmaps.find_place(
                input=f"{h.name} {h.full_address or h.raw_address}",
                input_type="textquery",
                fields=["photos"]
            )
            candidates = place.get("candidates", [])
            if candidates and candidates[0].get("photos"):
                ref = candidates[0]["photos"][0]["photo_reference"]
                photo_url = (
                    f"https://maps.googleapis.com/maps/api/place/photo"
                    f"?maxwidth=400&photoreference={ref}"
                    f"&key={settings.GOOGLE_API_KEY}"
                )
        except Exception:
            print("실패")
            photo_url = None

        print(photo_url)
        result.append({
            "name":     h.name,
            "address":  h.full_address or h.raw_address,
            "phone":    h.phone or "정보 없음",
            "distance": round(dist, 2),
            "photo":    photo_url,  # null 이면 클라이언트에서 기본 이미지로 처리
        })

    return JsonResponse(result, safe=False)

class NearestHospitalsView(LoginRequiredMixin, TemplateView):
    template_name = "hospitals/nearest.html"

    def get(self, request, *args, **kwargs):
        # lat/lng 파라미터가 있으면 API 함수 호출
        if request.GET.get("lat") and request.GET.get("lng"):
            return nearest_hospitals_api(request)
        # 없으면 템플릿 렌더
        return super().get(request, *args, **kwargs)
