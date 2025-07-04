# 🐕 Conveting - 반려견 건강 관리 플랫폼

**AI 기반 반려견 질병 예측 및 종합 건강 관리 서비스**

## 📋 프로젝트 소개

Conveting은 AI 기술을 활용한 반려견 건강 관리 플랫폼입니다. 딥러닝 모델을 통해 반려견의 눈과 피부 질환을 예측하고, 반려견 정보 관리, 커뮤니티 기능, 동물병원 검색 등 반려견 양육에 필요한 다양한 서비스를 제공합니다.

## ✨ 주요 기능

### 🤖 AI 질병 예측

-   **눈 질환 예측**: 10가지 안구 질환 예측 모델
-   **피부 질환 예측**: 6가지 피부 질환 예측 모델
-   **고정밀 예측**: TensorFlow/Keras 기반 CNN 모델 사용
-   **질환 정보 제공**: 증상, 가정 요법, 수의학적 치료 정보

### 🐕 반려견 관리

-   **프로필 관리**: 반려견 정보 등록 및 수정
-   **견종별 관리**: 20여 종의 견종 정보 지원
-   **건강 기록**: 예측 이력 및 건강 상태 추적
-   **이미지 관리**: 반려견 사진 업로드 및 관리

### 💬 커뮤니티

-   **게시판**: 반려견 관련 정보 공유 및 소통
-   **댓글 시스템**: 계층형 댓글 및 대댓글 기능
-   **좋아요 기능**: 게시글 및 댓글 좋아요
-   **견종별 필터링**: 견종별 게시글 분류 및 검색

### 🏥 동물병원 찾기

-   **위치 기반 검색**: 주변 동물병원 검색
-   **병원 정보**: 연락처, 주소, 운영 정보 제공
-   **지도 연동**: Google Maps API 활용

### 🔐 사용자 인증

-   **소셜 로그인**: 카카오, 구글 계정 연동
-   **일반 로그인**: 이메일 기반 회원가입/로그인
-   **프로필 관리**: 사용자 정보 및 프로필 이미지 관리

## 🛠️ 사용 기술

### Backend

-   **Django**: 4.2.20
-   **Python**: 3.x
-   **MySQL**: 데이터베이스
-   **Django REST Framework**: API 개발
-   **Django Allauth**: 소셜 로그인

### AI/ML

-   **TensorFlow**: 2.19.0
-   **Keras**: 3.9.2
-   **NumPy**: 수치 계산
-   **Pillow**: 이미지 처리

### Frontend

-   **HTML5** (Django Template)
-   **CSS3** (직접 작성, Google Fonts, CSS Reset)
-   **Vanilla JavaScript (ES6+)**
-   **외부 리소스**: Google Fonts, SVG/PNG 이미지

### 외부 API

-   **Google Maps API**: 지도 및 위치 서비스
-   **Kakao Login API**: 카카오 소셜 로그인
-   **Google OAuth**: 구글 소셜 로그인

### 개발 도구

-   **Git**: 버전 관리
-   **MySQL**: 데이터베이스 관리
-   **Gunicorn**: WSGI 서버
-   **WhiteNoise**: 정적 파일 서빙

## 🗂️ 프로젝트 구조

```
conveting/
├── accounts/              # 사용자 인증 및 계정 관리
│   ├── models.py         # 사용자 모델
│   ├── views.py          # 인증 관련 뷰
│   ├── forms.py          # 사용자 폼
│   └── adapters.py       # 소셜 로그인 어댑터
├── dogs/                 # 반려견 정보 관리
│   ├── models.py         # 반려견 모델
│   └── views.py          # 반려견 관리 뷰
├── prediction/           # AI 질병 예측
│   ├── models.py         # 예측 결과 모델
│   ├── views.py          # 예측 뷰
│   └── utils.py          # AI 모델 유틸리티
├── post/                 # 커뮤니티 게시판
│   ├── models.py         # 게시글/댓글 모델
│   └── views.py          # 게시판 뷰
├── hospitals/            # 동물병원 정보
│   ├── models.py         # 병원 모델
│   └── views.py          # 병원 검색 뷰
├── ai_weights/           # 학습된 AI 모델
│   ├── eye/              # 안구 질환 예측 모델
│   └── skin/             # 피부 질환 예측 모델
├── templates/            # HTML 템플릿
├── static/               # 정적 파일 (CSS, JS, 이미지)
├── media/                # 업로드된 미디어 파일
└── config/               # Django 설정
    ├── settings.py       # 프로젝트 설정
    └── urls.py           # URL 라우팅
```

## 🎮 구현 화면

### 1. 메인 페이지

-   서비스 소개 및 주요 기능 안내
-   네비게이션 바를 통한 쉬운 접근

### 2. AI 질병 예측 페이지

-   직관적인 이미지 업로드 인터페이스
-   반려견 선택 및 예측 부위 선택
-   실시간 예측 결과 및 질환 정보 제공

### 3. 반려견 관리 페이지

-   반려견 프로필 등록 및 수정
-   견종별 특성 정보 제공
-   건강 기록 및 예측 이력 조회

### 4. 커뮤니티 게시판

-   반응형 게시글 목록
-   이미지 첨부 및 댓글 기능
-   좋아요 및 검색 기능

### 5. 동물병원 찾기

-   지도 기반 병원 위치 표시
-   병원 상세 정보 및 연락처
-   거리순 정렬 기능

### 6. 마이페이지

-   사용자 정보 관리
-   예측 이력 및 반려견 정보 조회
-   프로필 이미지 변경

## 📱 프로젝트 실행 방법

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone <repository-url>
cd conveting

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 설정

```bash
# MySQL 데이터베이스 생성
mysql -u root -p
CREATE DATABASE conveting CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'conveting'@'localhost' IDENTIFIED BY 'Conveting1!';
GRANT ALL PRIVILEGES ON conveting.* TO 'conveting'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 환경 변수 설정

```bash
# .env 파일 생성 (프로젝트 루트)
touch .env

# .env 파일 내용
GOOGLE_API_KEY=your_google_api_key
SECRET_KEY=your_secret_key
```

### 4. 데이터베이스 마이그레이션

```bash
# 마이그레이션 생성 및 적용
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

### 5. 정적 파일 수집

```bash
# 정적 파일 수집
python manage.py collectstatic
```

### 6. 서버 실행

```bash
# 개발 서버 실행
python manage.py runserver

# 서버 접속
http://localhost:8000
```

## 🔧 추가 설정

### 소셜 로그인 설정

1. **Google OAuth 설정**

    - Google Cloud Console에서 OAuth 2.0 클라이언트 생성
    - 승인된 리디렉션 URI 추가

2. **Kakao Login 설정**
    - Kakao Developers에서 애플리케이션 등록
    - 플랫폼 설정 및 Redirect URI 등록

### AI 모델 설정

-   `ai_weights/` 폴더에 학습된 모델 파일 배치
-   모델 파일 경로 확인 및 설정

## 🚀 배포 방법

### 프로덕션 환경 설정

```bash
# 프로덕션 패키지 설치
pip install gunicorn whitenoise

# 정적 파일 서빙 설정
# settings.py에 WhiteNoise 미들웨어 추가

# Gunicorn으로 서버 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 👥 기여하기

1. 이 저장소를 Fork 합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push 합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성합니다

## 📞 문의하기

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**Conveting** - 반려견과 함께하는 건강한 삶을 위한 AI 파트너 🐾
