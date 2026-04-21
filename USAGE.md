# Panduan Penggunaan Aplikasi Histogram Specification

## Menjalankan Aplikasi

### 1. Persiapan
```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py
```

### 2. Akses Aplikasi
Buka browser dan akses: **http://localhost:5000**

## Cara Menggunakan

### Langkah 1: Upload Gambar Source
1. Klik tombol "Pilih Gambar" di kotak "Gambar Asli (Source)"
2. Pilih gambar yang ingin diproses
3. Preview gambar akan muncul

### Langkah 2: Upload Gambar Target
1. Klik tombol "Pilih Gambar" di kotak "Gambar Target"
2. Pilih gambar target (referensi histogram)
3. Preview gambar akan muncul

### Langkah 3: Proses
1. Klik tombol "Proses Histogram Specification"
2. Tunggu proses selesai (loading indicator akan muncul)
3. Hasil akan ditampilkan secara otomatis

## Memahami Hasil

### 1. Gambar Hasil
Tiga gambar ditampilkan:
- **Gambar Asli**: Gambar source dalam grayscale
- **Gambar Target**: Gambar target dalam grayscale
- **Hasil Specification**: Gambar hasil dengan histogram yang disesuaikan

### 2. Histogram
Tiga grafik histogram menunjukkan distribusi intensitas piksel:
- **Histogram Citra Asli** (Biru): Distribusi intensitas gambar asli
- **Histogram Citra Target** (Hijau): Distribusi intensitas gambar target
- **Histogram Hasil** (Merah): Distribusi intensitas gambar hasil

### 3. CDF (Cumulative Distribution Function)
Tiga grafik CDF menunjukkan fungsi distribusi kumulatif:
- **CDF Citra Asli**: Akumulasi probabilitas gambar asli
- **CDF Citra Target**: Akumulasi probabilitas gambar target
- **CDF Hasil**: Akumulasi probabilitas gambar hasil

### 4. Perbandingan CDF
Grafik overlay yang menampilkan ketiga CDF dalam satu plot untuk perbandingan visual.

### 5. Tabel Mapping
Menampilkan 20 nilai pertama dari lookup table:
- **rₖ**: Intensitas piksel asli (0-19)
- **CDF Source**: Nilai CDF pada intensitas rₖ
- **zₖ**: Intensitas hasil mapping
- **CDF Target**: Nilai CDF target pada intensitas zₖ
- **Error**: Selisih absolut antara CDF source dan target

### 6. Tabel Verifikasi
Menampilkan 11 titik kunci (0, 25, 50, 75, 100, 128, 150, 175, 200, 225, 255):
- **Intensitas**: Nilai intensitas yang diuji
- **CDF Asli**: Nilai CDF gambar asli
- **CDF Target**: Nilai CDF gambar target
- **CDF Hasil**: Nilai CDF gambar hasil
- **Status**: 
  - ✓ MATCH: Perbedaan < 0.05 (sangat baik)
  - ~ CLOSE: Perbedaan 0.05-0.1 (baik)
  - ✗ DIFF: Perbedaan > 0.1 (perlu perbaikan)

### 7. MSE (Mean Squared Error)
Nilai MSE antara CDF hasil dan CDF target:
- **Semakin mendekati 0**: Semakin baik hasil specification
- **< 0.001**: Excellent
- **0.001 - 0.01**: Good
- **> 0.01**: Fair

### 8. Log Proses
Detail lengkap proses algoritma:
- Langkah 0: Konversi ke grayscale
- Langkah 1: Menghitung histogram
- Langkah 2: Normalisasi (PDF)
- Langkah 3: Hitung CDF
- Langkah 4: Membuat tabel mapping
- Langkah 5: Aplikasi transformasi
- Verifikasi hasil

## Tips Penggunaan

### Memilih Gambar Source
- Gunakan gambar dengan kontras rendah untuk hasil terbaik
- Format: JPG, PNG, JPEG
- Ukuran maksimal: 16MB

### Memilih Gambar Target
- Pilih gambar dengan distribusi histogram yang diinginkan
- Gambar target menentukan karakteristik histogram hasil
- Contoh: Gambar dengan kontras tinggi untuk meningkatkan kontras

### Interpretasi Hasil
1. **Histogram**: Perhatikan perubahan distribusi intensitas
2. **CDF**: CDF hasil harus mendekati CDF target
3. **MSE**: Nilai kecil menunjukkan specification berhasil
4. **Status Verifikasi**: Mayoritas harus MATCH atau CLOSE

## Troubleshooting

### Error: "Kedua gambar harus diupload"
- Pastikan kedua gambar (source dan target) sudah dipilih

### Error: "Tidak ada file yang dipilih"
- Klik tombol "Pilih Gambar" dan pilih file

### Proses Lambat
- Gambar besar membutuhkan waktu lebih lama
- Resize gambar jika terlalu besar (>2000x2000 piksel)

### Hasil Tidak Sesuai
- Coba gambar target yang berbeda
- Pastikan gambar target memiliki karakteristik yang diinginkan

## Referensi Algoritma

Algoritma berdasarkan:
- Gonzalez & Woods - Digital Image Processing
- Histogram Specification (Histogram Matching)
- Inverse CDF Mapping Technique
