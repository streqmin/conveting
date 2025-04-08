---
name: WBS 기반 작업 내용
about: WBS 기반 작업 내용 업로드
title: "[작업 코드] 구현 요소 - 25/04/07"
labels: ''
assignees: streqmin

---

### 🧩 작업명
<!-- 구현할 기능의 간단한 이름 (ex. "JWT 인증 적용") -->

### 🗂️ 작업 코드
<!-- 예: USR-AUTH-LOCAL-JWT -->

### 📝 설명
<!-- 해당 작업이 무엇을 구현하는지 명확하게 작성해주세요. 필요시 참고할 기능 코드나 상위 작업명을 같이 적어도 좋습니다. -->

### 🔧 작업 상세
- [ ] 핵심 구현 요소
- [ ] 관련 모델/뷰/직렬화/URL 등
- [ ] 예외 처리 / 유효성 검사 여부
- [ ] 인증/권한 관련 여부

### 🔗 관련 항목
- 관련 작업: USR-AUTH-LOCAL-ENDPOINT
- PR: (작성 시 링크 추가)

### 🧪 테스트 조건
- 로그인 API 호출 시 JWT 토큰이 Set-Cookie로 반환되는지 확인
- 인증 필요한 API 호출 시 JWT 검증 통과 여부 확인

### 🧠 비고
- 쿠키 설정 시 SameSite / Secure 옵션 적용 고려
- CSRF 처리 여부 확인 필요

### 📎 참고 문서
- https://django-rest-framework-simplejwt.readthedocs.io/
