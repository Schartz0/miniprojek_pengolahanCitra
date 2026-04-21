
# ============================================================
# HISTOGRAM SPECIFICATION - GOOGLE COLAB VERSION
# ============================================================


# Cell 1: Import Library
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
from PIL import Image
import io

print("✅ Library berhasil diimport")

# Cell 2: Definisi Fungsi Histogram Specification

def histogram_specification_complete(source_img, target_img):
    """
    Implementasi lengkap Histogram Specification dengan penjabaran matematis
    Berdasarkan konsep dari Gonzalez & Woods - Digital Image Processing
    """

    print("=" * 90)
    print(" " * 25 + "HISTOGRAM SPECIFICATION (SPECIFICATION)")
    print(" " * 28 + "ALGORITMA LENGKAP")
    print("=" * 90)

    # Konversi ke grayscale
    if len(source_img.shape) == 3:
        source_gray = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)
        print("\n[STEP 0] KONVERSI: Citra Asli (RGB) → Grayscale")
    else:
        source_gray = source_img.copy()
        print("\n[STEP 0] Citra Asli sudah Grayscale")

    if len(target_img.shape) == 3:
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        print("[STEP 0] KONVERSI: Citra Target (RGB) → Grayscale")
    else:
        target_gray = target_img.copy()
        print("[STEP 0] Citra Target sudah Grayscale")

    # ============================================================
    # LANGKAH 1: HITUNG HISTOGRAM
    # ============================================================
    print("\n" + "=" * 90)
    print("LANGKAH 1: MENGHITUNG HISTOGRAM (HISTOGRAM COMPUTATION)")
    print("=" * 90)

    M, N = source_gray.shape
    M_t, N_t = target_gray.shape
    L = 256  # Level intensitas (0-255)

    print(f"\n📊 DIMENSI CITRA:")
    print(f"   Citra Asli: {M} × {N} = {M*N} piksel")
    print(f"   Citra Target: {M_t} × {N_t} = {M_t*N_t} piksel")
    print(f"   Level Intensitas (L): {L} (0 sampai 255)")

    print(f"\n📐 RUMUS HISTOGRAM:")
    print(f"   h(rₖ) = nₖ  (jumlah piksel dengan intensitas rₖ)")

    # Hitung histogram
    source_hist = np.zeros(L, dtype=np.float32)
    target_hist = np.zeros(L, dtype=np.float32)

    for i in range(M):
        for j in range(N):
            source_hist[source_gray[i, j]] += 1

    for i in range(M_t):
        for j in range(N_t):
            target_hist[target_gray[i, j]] += 1

    print(f"\n🔢 PERHITUNGAN HISTOGRAM CITRA ASLI (10 nilai pertama):")
    print(f"{'rₖ':<8} {'Frekuensi (nₖ)':<20} {'Keterangan'}")
    print("-" * 50)
    for k in range(10):
        print(f"{k:<8} {int(source_hist[k]):<20} h({k}) = {int(source_hist[k])}")

    print(f"\n🔢 PERHITUNGAN HISTOGRAM CITRA TARGET (10 nilai pertama):")
    print(f"{'zₖ':<8} {'Frekuensi (nₖ)':<20} {'Keterangan'}")
    print("-" * 50)
    for k in range(10):
        print(f"{k:<8} {int(target_hist[k]):<20} h({k}) = {int(target_hist[k])}")

    # ============================================================
    # LANGKAH 2: NORMALISASI (PDF)
    # ============================================================
    print("\n" + "=" * 90)
    print("LANGKAH 2: NORMALISASI HISTOGRAM (PDF)")
    print("=" * 90)

    print(f"\n📐 RUMUS PDF (Probability Density Function):")
    print(f"   p(rₖ) = nₖ / (M × N)")

    source_pdf = source_hist / (M * N)
    target_pdf = target_hist / (M_t * N_t)

    print(f"\n🔢 PERHITUNGAN PDF CITRA ASLI:")
    print(f"{'rₖ':<8} {'nₖ':<12} {'M×N':<12} {'p(rₖ)':<15}")
    print("-" * 55)
    for k in range(10):
        print(f"{k:<8} {int(source_hist[k]):<12} {M*N:<12} {source_pdf[k]:<15.8f}")

    print(f"\n🔢 PERHITUNGAN PDF CITRA TARGET:")
    print(f"{'zₖ':<8} {'nₖ':<12} {'M×N':<12} {'p(zₖ)':<15}")
    print("-" * 55)
    for k in range(10):
        print(f"{k:<8} {int(target_hist[k]):<12} {M_t*N_t:<12} {target_pdf[k]:<15.8f}")

    # ============================================================
    # LANGKAH 3: HITUNG CDF
    # ============================================================
    print("\n" + "=" * 90)
    print("LANGKAH 3: HITUNG CDF (CUMULATIVE DISTRIBUTION FUNCTION)")
    print("=" * 90)

    print(f"\n📐 RUMUS CDF:")
    print(f"   T(rₖ) = (L-1) × Σⱼ₌₀ᵏ p(rⱼ)")
    print(f"   G(zₖ) = (L-1) × Σⱼ₌₀ᵏ p(zⱼ)")
    print(f"   Dengan L = 256, maka (L-1) = 255")

    source_cdf = np.cumsum(source_pdf)
    target_cdf = np.cumsum(target_pdf)

    source_eq = np.round(255 * source_cdf).astype(np.uint8)
    target_eq = np.round(255 * target_cdf).astype(np.uint8)

    print(f"\n🔢 PERHITUNGAN CDF & TRANSFORMASI CITRA ASLI:")
    print(f"{'rₖ':<6} {'p(rₖ)':<12} {'Σp(rⱼ)':<12} {'255×Σ':<12} {'sₖ=T(rₖ)'}")
    print("-" * 70)
    cumsum = 0
    for k in range(10):
        cumsum += source_pdf[k]
        print(f"{k:<6} {source_pdf[k]:<12.6f} {cumsum:<12.6f} {255*cumsum:<12.4f} {source_eq[k]}")

    print(f"\n🔢 PERHITUNGAN CDF & TRANSFORMASI CITRA TARGET:")
    print(f"{'zₖ':<6} {'p(zₖ)':<12} {'Σp(zⱼ)':<12} {'255×Σ':<12} {'vₖ=G(zₖ)'}")
    print("-" * 70)
    cumsum = 0
    for k in range(10):
        cumsum += target_pdf[k]
        print(f"{k:<6} {target_pdf[k]:<12.6f} {cumsum:<12.6f} {255*cumsum:<12.4f} {target_eq[k]}")

    # ============================================================
    # LANGKAH 4: MEMBUAT MAPPING TABLE (INVERSE MAPPING)
    # ============================================================
    print("\n" + "=" * 90)
    print("LANGKAH 4: MEMBUAT TABEL MAPPING (INVERSE MAPPING)")
    print("=" * 90)

    print(f"\n📐 KONSEP INVERSE MAPPING:")
    print(f"   Untuk setiap nilai rₖ di citra asli:")
    print(f"   1. Hitung sₖ = T(rₖ) = round(255 × CDF_source[rₖ])")
    print(f"   2. Cari zₖ sedemikian sehingga G(zₖ) ≈ sₖ")
    print(f"   3. Atau: cari zₖ dengan CDF_target[zₖ] ≈ CDF_source[rₖ]")
    print(f"   ")
    print(f"   Algoritma: zₖ = argmin|CDF_target[z] - CDF_source[rₖ]|")

    lookup_table = np.zeros(L, dtype=np.uint8)

    print(f"\n🔢 PERHITUNGAN INVERSE MAPPING (20 nilai pertama):")
    print(f"{'rₖ':<6} {'CDF_s[rₖ]':<12} {'zₖ yang cocok':<15} {'CDF_t[zₖ]':<12} {'Error':<12}")
    print("-" * 75)

    for r in range(L):
        cdf_s = source_cdf[r]
        min_diff = float('inf')
        best_z = 0

        for z in range(L):
            diff = abs(target_cdf[z] - cdf_s)
            if diff < min_diff:
                min_diff = diff
                best_z = z

        lookup_table[r] = best_z

        if r < 20:
            print(f"{r:<6} {cdf_s:<12.6f} {best_z:<15} {target_cdf[best_z]:<12.6f} {min_diff:.6f}")

    # ============================================================
    # LANGKAH 5: APLIKASIKAN TRANSFORMASI
    # ============================================================
    print("\n" + "=" * 90)
    print("LANGKAH 5: APLIKASI TRANSFORMASI PADA CITRA")
    print("=" * 90)

    print(f"\n📐 PROSES:")
    print(f"   Untuk setiap piksel (i,j) di citra asli dengan nilai r:")
    print(f"   s(i,j) = lookup_table[r(i,j)]")

    result_img = cv2.LUT(source_gray, lookup_table)

    print(f"\n🔢 CONTOH TRANSFORMASI PIKSEL:")
    print(f"{'Posisi (i,j)':<15} {'Nilai Asli (r)':<15} {'Nilai Baru (z)'}")
    print("-" * 50)

    samples = [
        (M//4, N//4),
        (M//2, N//2),
        (3*M//4, 3*N//4),
        (M//3, 2*N//3),
        (2*M//3, N//3)
    ]

    for i, j in samples:
        if i < M and j < N:
            r_val = source_gray[i, j]
            z_val = result_img[i, j]
            print(f"({i},{j}){'':<6} {r_val:<15} {z_val}")

    # ============================================================
    # VERIFIKASI HASIL
    # ============================================================
    print("\n" + "=" * 90)
    print("VERIFIKASI HASIL")
    print("=" * 90)

    result_hist = cv2.calcHist([result_img], [0], None, [256], [0, 256]).flatten()
    result_pdf = result_hist / result_img.size
    result_cdf = np.cumsum(result_pdf)

    print(f"\n📊 PERBANDINGAN CDF PADA TITIK-TITIK KUNCI:")
    print(f"{'Intensitas':<12} {'CDF Asli':<15} {'CDF Target':<15} {'CDF Hasil':<15} {'Status'}")
    print("-" * 75)

    test_points = [0, 25, 50, 75, 100, 128, 150, 175, 200, 225, 255]
    for val in test_points:
        diff = abs(result_cdf[val] - target_cdf[val])
        status = "✓ MATCH" if diff < 0.05 else "~ CLOSE" if diff < 0.1 else "✗ DIFF"
        print(f"{val:<12} {source_cdf[val]:<15.6f} {target_cdf[val]:<15.6f} {result_cdf[val]:<15.6f} {status}")

    mse_cdf = np.mean((result_cdf - target_cdf) ** 2)
    print(f"\n📈 MSE antara CDF Hasil dan CDF Target: {mse_cdf:.8f}")
    print(f"    (Semakin mendekati 0, semakin baik)")

    return source_gray, target_gray, result_img, lookup_table, source_cdf, target_cdf, result_cdf, source_hist, target_hist, result_hist


def visualize_results(source, target, result, s_hist, t_hist, r_hist, s_cdf, t_cdf, r_cdf):
    """
    Visualisasi lengkap hasil histogram specification
    """
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    fig.suptitle('HISTOGRAM SPECIFICATION - ANALISIS LENGKAP', fontsize=16, fontweight='bold', y=0.98)

    # Row 1: Images
    axes[0, 0].imshow(source, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title('CITRA ASLI (Source)', fontweight='bold', fontsize=12)
    axes[0, 0].axis('off')

    axes[0, 1].imshow(target, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title('CITRA TARGET (Target)', fontweight='bold', fontsize=12)
    axes[0, 1].axis('off')

    axes[0, 2].imshow(result, cmap='gray', vmin=0, vmax=255)
    axes[0, 2].set_title('HASIL SPECIFICATION', fontweight='bold', fontsize=12, color='red')
    axes[0, 2].axis('off')

    # Row 2: Histograms
    axes[1, 0].bar(range(256), s_hist, color='blue', alpha=0.7, width=1)
    axes[1, 0].set_title('Histogram Citra Asli', fontsize=11)
    axes[1, 0].set_xlim([0, 255])
    axes[1, 0].set_xlabel('Intensitas')
    axes[1, 0].set_ylabel('Frekuensi')
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].bar(range(256), t_hist, color='green', alpha=0.7, width=1)
    axes[1, 1].set_title('Histogram Citra Target', fontsize=11)
    axes[1, 1].set_xlim([0, 255])
    axes[1, 1].set_xlabel('Intensitas')
    axes[1, 1].set_ylabel('Frekuensi')
    axes[1, 1].grid(True, alpha=0.3)

    axes[1, 2].bar(range(256), r_hist, color='red', alpha=0.7, width=1)
    axes[1, 2].set_title('Histogram Hasil', fontsize=11)
    axes[1, 2].set_xlim([0, 255])
    axes[1, 2].set_xlabel('Intensitas')
    axes[1, 2].set_ylabel('Frekuensi')
    axes[1, 2].grid(True, alpha=0.3)

    # Row 3: CDFs
    axes[2, 0].plot(range(256), s_cdf, 'b-', linewidth=2.5, label='CDF Asli')
    axes[2, 0].set_title('CDF Citra Asli', fontsize=11)
    axes[2, 0].set_xlim([0, 255])
    axes[2, 0].set_ylim([0, 1])
    axes[2, 0].set_xlabel('Intensitas')
    axes[2, 0].set_ylabel('CDF')
    axes[2, 0].grid(True, alpha=0.3)
    axes[2, 0].legend()

    axes[2, 1].plot(range(256), t_cdf, 'g-', linewidth=2.5, label='CDF Target')
    axes[2, 1].set_title('CDF Citra Target', fontsize=11)
    axes[2, 1].set_xlim([0, 255])
    axes[2, 1].set_ylim([0, 1])
    axes[2, 1].set_xlabel('Intensitas')
    axes[2, 1].set_ylabel('CDF')
    axes[2, 1].grid(True, alpha=0.3)
    axes[2, 1].legend()

    axes[2, 2].plot(range(256), r_cdf, 'r-', linewidth=2.5, label='CDF Hasil')
    axes[2, 2].plot(range(256), t_cdf, 'g--', linewidth=2, alpha=0.7, label='CDF Target (ref)')
    axes[2, 2].set_title('CDF Hasil vs Target', fontsize=11)
    axes[2, 2].set_xlim([0, 255])
    axes[2, 2].set_ylim([0, 1])
    axes[2, 2].set_xlabel('Intensitas')
    axes[2, 2].set_ylabel('CDF')
    axes[2, 2].grid(True, alpha=0.3)
    axes[2, 2].legend()

    plt.tight_layout()
    plt.savefig('histogram_specification_complete.png', dpi=150, bbox_inches='tight')
    plt.show()

    # Plot tambahan: Perbandingan CDF
    fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
    fig2.suptitle('PERBANDINGAN CDF DAN PDF', fontsize=14, fontweight='bold')

    axes2[0].plot(range(256), s_cdf, 'b-', label='Citra Asli', linewidth=2)
    axes2[0].plot(range(256), t_cdf, 'g-', label='Citra Target', linewidth=2)
    axes2[0].plot(range(256), r_cdf, 'r--', label='Hasil Spec', linewidth=2.5)
    axes2[0].set_title('Perbandingan CDF Ketiga Citra')
    axes2[0].set_xlabel('Intensitas Piksel')
    axes2[0].set_ylabel('CDF')
    axes2[0].legend()
    axes2[0].grid(True, alpha=0.3)

    axes2[1].plot(range(256), s_hist/s_hist.sum(), 'b-', alpha=0.7, label='Asli', linewidth=1.5)
    axes2[1].plot(range(256), t_hist/t_hist.sum(), 'g-', alpha=0.7, label='Target', linewidth=1.5)
    axes2[1].plot(range(256), r_hist/r_hist.sum(), 'r-', alpha=0.7, label='Hasil', linewidth=1.5)
    axes2[1].set_title('Perbandingan PDF (Histogram Normalized)')
    axes2[1].set_xlabel('Intensitas Piksel')
    axes2[1].set_ylabel('Probabilitas')
    axes2[1].legend()
    axes2[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('cdf_pdf_comparison.png', dpi=150, bbox_inches='tight')
    plt.show()

print("✅ Fungsi berhasil didefinisikan")
print("\n" + "="*70)
print("CARA PENGGUNAAN:")
print("="*70)
print("1. Upload citra asli (source):")
print("   uploaded = files.upload()")
print("   source_img = cv2.imread(list(uploaded.keys())[0])")
print("\n2. Upload citra target:")
print("   uploaded = files.upload()")
print("   target_img = cv2.imread(list(uploaded.keys())[0])")
print("\n3. Jalankan histogram specification:")
print("   source_gray, target_gray, result, lookup, s_cdf, t_cdf, r_cdf, s_hist, t_hist, r_hist = histogram_specification_complete(source_img, target_img)")
print("\n4. Visualisasikan:")
print("   visualize_results(source_gray, target_gray, result, s_hist, t_hist, r_hist, s_cdf, t_cdf, r_cdf)")

# Cell 3: Upload dan Proses (Contoh Penggunaan)
print("\n" + "="*70)
print("UPLOAD CITRA ASLI (SOURCE):")
print("="*70)
uploaded_source = files.upload()
source_filename = list(uploaded_source.keys())[0]
source_img = cv2.imread(source_filename)

print("\n" + "="*70)
print("UPLOAD CITRA TARGET:")
print("="*70)
uploaded_target = files.upload()
target_filename = list(uploaded_target.keys())[0]
target_img = cv2.imread(target_filename)

print(f"\n✅ Citra Asli: {source_filename} - Shape: {source_img.shape}")
print(f"✅ Citra Target: {target_filename} - Shape: {target_img.shape}")

# Cell 4: Jalankan Histogram Specification
source_gray, target_gray, result_img, lookup_table, s_cdf, t_cdf, r_cdf, s_hist, t_hist, r_hist = histogram_specification_complete(source_img, target_img)

# Cell 5: Visualisasi
visualize_results(source_gray, target_gray, result_img, s_hist, t_hist, r_hist, s_cdf, t_cdf, r_cdf)

# Cell 6: Simpan Hasil (Opsional)
cv2.imwrite('hasil_specification.jpg', result_img)
print("\n💾 Hasil telah disimpan sebagai 'hasil_specification.jpg'")
files.download('hasil_specification.jpg')