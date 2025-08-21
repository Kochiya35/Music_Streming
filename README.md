# 🎵 Music Streaming Backend (Django + DRF)

## 📌 개요
이 프로젝트는 **음악 스트리밍 웹 서비스 백엔드**입니다.  
사용자 요구사항 정의서 + ERD + FlowChart에 따라 구현되었으며,  
**회원가입/로그인 → 음악 업로드 → 스트리밍 → 즐겨찾기/재생기록/플레이리스트** 흐름을 지원합니다.

---

## ✅ 요구사항 정의서 매핑

| 요구사항 | 구현 여부 | 엔드포인트/기능 |
|----------|-----------|----------------|
| 회원가입/로그인 | ✅ | `POST /api/auth/register/`, `POST /api/auth/token/`, `POST /api/auth/token/refresh/` |
| 마이페이지(내 정보 수정) | ✅ | `GET/PATCH /api/me/` |
| 음악 업로드 (관리자) | ✅ | `POST /api/tracks/presigned_upload/` (S3 업로드 URL 발급)<br>`POST /api/tracks/` (메타데이터 등록) |
| 음악 목록 조회 | ✅ | `GET /api/tracks/` (검색, 필터링, 정렬) |
| 곡 상세/스트리밍 | ✅ | `GET /api/tracks/{id}/`<br>`POST /api/tracks/{id}/stream/` (presigned GET URL 발급 + 재생 기록 저장) |
| 즐겨찾기 | ✅ | `POST /api/tracks/{id}/toggle_favorite/`<br>`GET /api/favorites/` |
| 재생 기록 | ✅ | `GET /api/history/` |
| 플레이리스트 | ✅ | `POST /api/playlists/` (생성)<br>`GET /api/playlists/` (목록)<br>`POST /api/playlists/{id}/add/` (곡 추가)<br>`POST /api/playlists/{id}/remove/` (곡 삭제)<br>`GET /api/playlists/{id}/` (조회) |
| 관리자 페이지 | ✅ | `/admin/` (User, Track, Favorite, PlayHistory, Playlist 관리 가능) |

---

## 🗄️ ERD 매핑

| 테이블 | 설명 | 모델 |
|--------|------|------|
| User | 회원 정보 (닉네임, 이메일, 비밀번호, 아바타 등) | `core.models.User` |
| Track | 곡 메타데이터 (제목, 아티스트, 장르, 썸네일, S3 key 등) | `core.models.Track` |
| Favorite | 즐겨찾기 (user-track 관계) | `core.models.Favorite` |
| PlayHistory | 재생기록 (user-track, 재생 시간 기록) | `core.models.PlayHistory` |
| Playlist | 사용자별 재생목록 | `core.models.Playlist` |
| PlaylistTrack | Playlist와 Track의 연결 (순서, 추가 시간) | `core.models.PlaylistTrack` |

---

## 🔄 FlowChart 매핑

사용자 흐름은 다음과 같이 매핑됩니다:

1. 회원가입 → 로그인 (JWT 발급)  
2. 곡 목록 조회 (`GET /api/tracks/`)  
3. 곡 선택 → 스트리밍 (`POST /api/tracks/{id}/stream/`)  
   - presigned GET URL 발급  
   - 동시에 **재생 기록 자동 저장**  
4. 곡 즐겨찾기 on/off (`toggle_favorite`)  
5. 나만의 플레이리스트 생성 및 관리  
   - 곡 추가/삭제  
   - 공개 여부(is_public)로 공유 가능  

---

## 🚀 실행 방법

```bash
# 가상환경 & 설치
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 환경변수
cp .env.example .env

# DB 초기화
python manage.py makemigrations
python manage.py migrate

# 관리자 계정 생성
python manage.py createsuperuser

# 서버 실행
python manage.py runserver 8001
