import os
import pandas as pd
import googlemaps
from django.core.management.base import BaseCommand
from django.conf import settings
from hospitals.models import AnimalHospital


class Command(BaseCommand):
    help = "Excel에서 동물병원 읽고, 구글 Geocode API로 주소·위경도 보완 후 저장"

    def handle(self, *args, **options):
        # df = pd.read_excel("../../data/동물병원 목록_20250422.xls")
        file_path = os.path.join(
            settings.BASE_DIR, "hospitals", "data", "동물병원 목록_20250422.xls"
        )
        # .xls 읽을 때는 engine='xlrd' 지정
        df = pd.read_excel(file_path, engine="xlrd")
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)

        for _, row in df.iterrows():
            query = f"{row['병원명']} {row['소재지']}"
            result = gmaps.geocode(query, language="ko")
            if result:
                place = result[0]
                addr = place["formatted_address"]
                loc = place["geometry"]["location"]
                lat, lng = loc["lat"], loc["lng"]
            else:
                addr, lat, lng = "", None, None

            obj, created = AnimalHospital.objects.update_or_create(
                name=row["병원명"],
                license_no=row["인허가번호"],
                defaults={
                    "phone": row["전화번호"],
                    "raw_address": row["소재지"],
                    "full_address": addr,
                    "latitude": lat,
                    "longitude": lng,
                },
            )
            status = "생성" if created else "갱신"
            self.stdout.write(f"{obj.name} → {status}")
