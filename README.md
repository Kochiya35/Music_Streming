# Music Streaming (Backend-only, Django + DRF + JWT)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

### Smoke Test
```bash
# 1) 시스템 점검
python manage.py check

# 2) 토큰 발급
curl -X POST http://127.0.0.1:8000/api/auth/register/ -H "Content-Type: application/json"       -d '{"username":"admin1","email":"a@a.com","password":"StrongPass!234"}'

curl -X POST http://127.0.0.1:8000/api/auth/token/ -H "Content-Type: application/json"       -d '{"username":"admin1","password":"StrongPass!234"}'
```

## Endpoints
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET/PATCH /api/me/`
- `GET /api/tracks/` `GET /api/tracks/{id}/`
- `POST /api/tracks/` (admin)
- `POST /api/tracks/presigned_upload/` (admin)
