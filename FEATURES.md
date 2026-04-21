# Fitur Lengkap Aplikasi Histogram Specification

## Fitur Utama

### 1. Upload Gambar
- Upload gambar source (asli)
- Upload gambar target
- Preview gambar sebelum diproses
- Support format: JPG, PNG, JPEG
- Maksimal ukuran file: 16MB

### 2. Proses Histogram Specification
Implementasi lengkap algoritma histogram specification dengan 5 langkah:

#### Langkah 0: Konversi ke Grayscale
- Otomatis konversi gambar RGB ke grayscale
- Deteksi jika gambar sudah grayscale

#### Langkah 1: Menghitung Histogram
- Hitung frekuensi setiap intensitas piksel (0-255)
- Rumus: h(rₖ) = nₖ (jumlah piksel dengan intensitas rₖ)

#### Langkah 2: Normalisasi Histogram (PDF)
- Probability Density Function
- Rumus: p(rₖ) = nₖ / (M × N)

#### Langkah 3: Hitung CDF
- Cumulative Distribution Function
- Rumus: T(rₖ) = (L-1) × Σⱼ₌₀ᵏ p(rⱼ)

#### Langkah 4: Membuat Tabel Mapping (Inverse Mapping)
- Cari nilai zₖ yang paling cocok untuk setiap rₖ
- Algoritma: zₖ = argmin|CDF_target[z] - CDF_source[rₖ]|

#### Langkah 5: Aplikasi Transformasi
- Terapkan lookup table ke setiap piksel
- s(i,j) = lookup_table[r(i,j)]

### 3. Visualisasi Hasil

#### A. Gambar
- Gambar asli (grayscale)
- Gambar target (grayscale)
- Gambar hasil specification

#### B. Histogram
- Histogram citra asli (biru)
- Histogram citra target (hijau)
- Histogram hasil (merah)

#### C. CDF (Cumulative Distribution Function)
- CDF citra asli
- CDF citra target
- CDF hasil
- Perbandingan ketiga CDF dalam satu grafik

#### D. Tabel Data

**Tabel Mapping (20 nilai pertama):**
- rₖ: Intensitas asli
- CDF Source: Nilai CDF citra asli
- zₖ: Intensitas hasil mapping
- CDF Target: Nilai CDF citra target
- Error: Selisih absolut CDF

**Tabel Verifikasi (11 titik kunci):**
- Intensitas: 0, 25, 50, 75, 100, 128, 150, 175, 200, 225, 255
- CDF Asli, CDF Target, CDF Hasil
- Status: ✓ MATCH, ~ CLOSE, atau ✗ DIFF

#### E. Metrik Evaluasi
- MSE (Mean Squared Error) antara CDF hasil dan CDF target
- Semakin mendekati 0, semakin baik

#### F. Log Proses
- Log lengkap setiap langkah algoritma
- Penjelasan matematis
- Contoh perhitungan

## Desain UI

- Responsive design (mobile-friendly)
- Gradient background modern
- Card-based layout
- Smooth animations
- Loading indicator
- Error handling dengan pesan jelas

## Performa

- Proses cepat dengan NumPy
- Visualisasi real-time dengan Matplotlib
- Efficient image encoding (base64)
- Optimized chart generation

## Output

Semua hasil dapat dilihat langsung di browser:
1. Gambar hasil specification
2. 6 grafik (3 histogram + 3 CDF)
3. 1 grafik perbandingan CDF
4. 2 tabel data (mapping + verifikasi)
5. 1 nilai MSE
6. Log proses lengkap

## Teknologi

- **Backend**: Flask (Python)
- **Image Processing**: OpenCV
- **Numerical Computing**: NumPy
- **Visualization**: Matplotlib
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Kompatibilitas

- Desktop: Chrome, Firefox, Safari, Edge
- Mobile: iOS Safari, Chrome Mobile
- Tablet: iPad, Android Tablet

