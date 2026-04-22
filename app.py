from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB max

# Batas panjang sisi terpanjang gambar untuk display (bukan untuk komputasi)
DISPLAY_MAX_SIZE = 800

def resize_for_display(img):
    """Resize gambar hanya untuk keperluan display, bukan komputasi."""
    h, w = img.shape[:2]
    if max(h, w) <= DISPLAY_MAX_SIZE:
        return img
    scale = DISPLAY_MAX_SIZE / max(h, w)
    new_w = int(w * scale)
    new_h = int(h * scale)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def img_to_base64(img, quality=85):
    """Encode gambar ke JPEG base64 untuk transfer yang lebih ringan."""
    display_img = resize_for_display(img)
    _, buffer = cv2.imencode('.jpg', display_img, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')

def plot_to_base64(fig):
    """Simpan figure matplotlib ke base64 PNG dengan DPI rendah."""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=72, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return "data:image/png;base64," + data

def create_histogram_plot(hist_data, title, color):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(range(256), hist_data, color=color, alpha=0.7, width=1)
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlim([0, 255])
    ax.set_xlabel('Intensitas', fontsize=8)
    ax.set_ylabel('Frekuensi', fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return plot_to_base64(fig)

def create_cdf_plot(cdf_data, title, color, label):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(range(256), cdf_data, color=color, linewidth=2, label=label)
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_xlim([0, 255])
    ax.set_ylim([0, 1])
    ax.set_xlabel('Intensitas', fontsize=8)
    ax.set_ylabel('CDF', fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    return plot_to_base64(fig)

def create_comparison_plot(source_cdf, target_cdf, result_cdf):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(range(256), source_cdf, 'b-', label='Citra Asli', linewidth=1.5)
    ax.plot(range(256), target_cdf, 'g-', label='Citra Target', linewidth=1.5)
    ax.plot(range(256), result_cdf, 'r--', label='Hasil Specification', linewidth=2)
    ax.set_title('Perbandingan CDF Ketiga Citra', fontsize=11, fontweight='bold')
    ax.set_xlabel('Intensitas Piksel', fontsize=8)
    ax.set_ylabel('CDF', fontsize=8)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return plot_to_base64(fig)

def histogram_specification_complete(source_img, target_img):
    logs = []
    logs.append("=" * 90)
    logs.append(" " * 25 + "HISTOGRAM SPECIFICATION")
    logs.append(" " * 28 + "ALGORITMA LENGKAP")
    logs.append("=" * 90)

    # Step 0: Konversi ke grayscale
    if len(source_img.shape) == 3:
        source_gray = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)
        logs.append("\n[STEP 0] KONVERSI: Citra Asli (RGB) → Grayscale")
    else:
        source_gray = source_img.copy()
        logs.append("\n[STEP 0] Citra Asli sudah Grayscale")

    if len(target_img.shape) == 3:
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        logs.append("[STEP 0] KONVERSI: Citra Target (RGB) → Grayscale")
    else:
        target_gray = target_img.copy()
        logs.append("[STEP 0] Citra Target sudah Grayscale")

    # Step 1: Hitung histogram — gunakan np.bincount, jauh lebih cepat dari double loop
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 1: MENGHITUNG HISTOGRAM")
    logs.append("=" * 90)

    M, N = source_gray.shape
    M_t, N_t = target_gray.shape
    L = 256

    logs.append(f"\nDIMENSI CITRA:")
    logs.append(f"   Citra Asli: {M} x {N} = {M*N} piksel")
    logs.append(f"   Citra Target: {M_t} x {N_t} = {M_t*N_t} piksel")
    logs.append(f"   Level Intensitas (L): {L} (0 sampai 255)")

    # np.bincount jauh lebih cepat dari double loop untuk gambar besar
    source_hist = np.bincount(source_gray.ravel(), minlength=L).astype(np.float32)
    target_hist = np.bincount(target_gray.ravel(), minlength=L).astype(np.float32)

    # Step 2: Normalisasi (PDF)
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 2: NORMALISASI HISTOGRAM (PDF)")
    logs.append("=" * 90)
    logs.append(f"\nRUMUS PDF: p(rk) = nk / (M x N)")

    source_pdf = source_hist / (M * N)
    target_pdf = target_hist / (M_t * N_t)

    # Step 3: Hitung CDF
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 3: HITUNG CDF (CUMULATIVE DISTRIBUTION FUNCTION)")
    logs.append("=" * 90)
    logs.append(f"\nRUMUS CDF: T(rk) = (L-1) x jumlah p(rj) dari j=0 sampai k")

    source_cdf = np.cumsum(source_pdf)
    target_cdf = np.cumsum(target_pdf)

    # Step 4: Inverse mapping — gunakan np.searchsorted, O(256 log 256) vs O(256x256)
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 4: MEMBUAT TABEL MAPPING (INVERSE MAPPING)")
    logs.append("=" * 90)

    # searchsorted mencari posisi insert yang menjaga urutan sorted,
    # efeknya sama dengan argmin |target_cdf[z] - source_cdf[r]| tapi jauh lebih cepat
    lookup_table = np.searchsorted(target_cdf, source_cdf).clip(0, 255).astype(np.uint8)

    mapping_data = []
    for r in range(20):
        z = int(lookup_table[r])
        mapping_data.append({
            'r': r,
            'cdf_s': float(source_cdf[r]),
            'z': z,
            'cdf_t': float(target_cdf[z]),
            'error': float(abs(target_cdf[z] - source_cdf[r]))
        })

    # Step 5: Aplikasi transformasi
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 5: APLIKASI TRANSFORMASI PADA CITRA")
    logs.append("=" * 90)

    result_img = cv2.LUT(source_gray, lookup_table)

    # Verifikasi
    logs.append("\n" + "=" * 90)
    logs.append("VERIFIKASI HASIL")
    logs.append("=" * 90)

    result_hist = np.bincount(result_img.ravel(), minlength=L).astype(np.float32)
    result_pdf = result_hist / result_img.size
    result_cdf = np.cumsum(result_pdf)

    verification_data = []
    test_points = [0, 25, 50, 75, 100, 128, 150, 175, 200, 225, 255]
    for val in test_points:
        diff = abs(result_cdf[val] - target_cdf[val])
        status = "MATCH" if diff < 0.05 else "CLOSE" if diff < 0.1 else "DIFF"
        verification_data.append({
            'intensity': val,
            'cdf_source': float(source_cdf[val]),
            'cdf_target': float(target_cdf[val]),
            'cdf_result': float(result_cdf[val]),
            'status': status
        })

    mse_cdf = float(np.mean((result_cdf - target_cdf) ** 2))
    logs.append(f"\nMSE antara CDF Hasil dan CDF Target: {mse_cdf:.8f}")

    return {
        'source_gray': source_gray,
        'target_gray': target_gray,
        'result_img': result_img,
        'source_hist': source_hist,
        'target_hist': target_hist,
        'result_hist': result_hist,
        'source_cdf': source_cdf,
        'target_cdf': target_cdf,
        'result_cdf': result_cdf,
        'logs': logs,
        'mapping_data': mapping_data,
        'verification_data': verification_data,
        'mse_cdf': mse_cdf
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'source' not in request.files or 'target' not in request.files:
        return jsonify({'error': 'Kedua gambar harus diupload'}), 400

    source_file = request.files['source']
    target_file = request.files['target']

    if source_file.filename == '' or target_file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400

    try:
        source_bytes = np.frombuffer(source_file.read(), np.uint8)
        target_bytes = np.frombuffer(target_file.read(), np.uint8)

        source_img = cv2.imdecode(source_bytes, cv2.IMREAD_COLOR)
        target_img = cv2.imdecode(target_bytes, cv2.IMREAD_COLOR)

        if source_img is None or target_img is None:
            return jsonify({'error': 'Gagal membaca gambar. Pastikan format file valid.'}), 400

        result = histogram_specification_complete(source_img, target_img)

        return jsonify({
            'source':       img_to_base64(result['source_gray']),
            'target':       img_to_base64(result['target_gray']),
            'result':       img_to_base64(result['result_img']),
            'hist_source':  create_histogram_plot(result['source_hist'], 'Histogram Citra Asli', 'blue'),
            'hist_target':  create_histogram_plot(result['target_hist'], 'Histogram Citra Target', 'green'),
            'hist_result':  create_histogram_plot(result['result_hist'], 'Histogram Hasil', 'red'),
            'cdf_source':   create_cdf_plot(result['source_cdf'], 'CDF Citra Asli', 'blue', 'CDF Asli'),
            'cdf_target':   create_cdf_plot(result['target_cdf'], 'CDF Citra Target', 'green', 'CDF Target'),
            'cdf_result':   create_cdf_plot(result['result_cdf'], 'CDF Hasil', 'red', 'CDF Hasil'),
            'comparison':   create_comparison_plot(result['source_cdf'], result['target_cdf'], result['result_cdf']),
            'logs':             result['logs'],
            'mapping_data':     result['mapping_data'],
            'verification_data': result['verification_data'],
            'mse_cdf':          result['mse_cdf']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
