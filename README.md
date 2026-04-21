# Histogram Specification Web App

Aplikasi web untuk melakukan histogram specification pada gambar menggunakan Flask dengan visualisasi lengkap.

## Fitur

- Upload gambar source dan target
- Proses histogram specification dengan algoritma lengkap
- Visualisasi hasil:
  - Gambar asli, target, dan hasil
  - Histogram untuk ketiga gambar
  - CDF (Cumulative Distribution Function) untuk ketiga gambar
  - Perbandingan CDF
  - Tabel mapping inverse (20 nilai pertama)
  - Tabel verifikasi hasil
  - MSE (Mean Squared Error) antara CDF hasil dan target
  - Log proses lengkap dengan penjelasan matematis

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Cara Menggunakan

1. Buka browser dan akses `http://localhost:5000`
2. Upload gambar asli (source)
3. Upload gambar target
4. Klik tombol "Proses Histogram Specification"
5. Lihat hasil pemrosesan lengkap dengan:
   - Gambar hasil
   - Grafik histogram dan CDF
   - Tabel data mapping
   - Tabel verifikasi
   - Log proses detail

## Teknologi

- Flask - Web framework
- OpenCV - Image processing
- NumPy - Numerical computing
- Matplotlib - Data visualization
- HTML/CSS/JavaScript - Frontend

## Hosting

Aplikasi ini dapat di-hosting di:
- Heroku
- Railway
- Render
- PythonAnywhere
- Google Cloud Run
- AWS Elastic Beanstalk

Pastikan untuk mengatur environment variables dan dependencies sesuai platform hosting yang dipilih.
