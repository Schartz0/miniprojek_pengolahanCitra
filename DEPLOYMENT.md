# Panduan Deployment

## Deployment ke Render.com (Gratis)

1. Push kode ke GitHub repository
2. Buat akun di [Render.com](https://render.com)
3. Klik "New +" → "Web Service"
4. Connect repository GitHub Anda
5. Konfigurasi:
   - Name: histogram-specification
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Klik "Create Web Service"

## Deployment ke Railway.app (Gratis)

1. Push kode ke GitHub repository
2. Buat akun di [Railway.app](https://railway.app)
3. Klik "New Project" → "Deploy from GitHub repo"
4. Pilih repository Anda
5. Railway akan otomatis detect Python dan deploy

## Deployment ke Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create nama-app-anda`
4. Push: `git push heroku main`

## Deployment ke PythonAnywhere

1. Upload semua file ke PythonAnywhere
2. Buat virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure WSGI file untuk Flask
5. Reload web app

## Deployment ke Google Cloud Run

1. Install Google Cloud SDK
2. Build container: `gcloud builds submit --tag gcr.io/PROJECT-ID/histogram-app`
3. Deploy: `gcloud run deploy --image gcr.io/PROJECT-ID/histogram-app --platform managed`

## Environment Variables (Jika diperlukan)

Untuk production, tambahkan:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## Testing Lokal

```bash
python app.py
```

Akses di: http://localhost:5000
