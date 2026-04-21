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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def histogram_specification_complete(source_img, target_img):
    """
    Implementasi lengkap Histogram Specification dengan penjabaran matematis
    """
    logs = []
    
    logs.append("=" * 90)
    logs.append(" " * 25 + "HISTOGRAM SPECIFICATION")
    logs.append(" " * 28 + "ALGORITMA LENGKAP")
    logs.append("=" * 90)

    # Konversi ke grayscale
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

    # LANGKAH 1: HITUNG HISTOGRAM
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 1: MENGHITUNG HISTOGRAM")
    logs.append("=" * 90)

    M, N = source_gray.shape
    M_t, N_t = target_gray.shape
    L = 256

    logs.append(f"\nDIMENSI CITRA:")
    logs.append(f"   Citra Asli: {M} × {N} = {M*N} piksel")
    logs.append(f"   Citra Target: {M_t} × {N_t} = {M_t*N_t} piksel")
    logs.append(f"   Level Intensitas (L): {L} (0 sampai 255)")

    # Hitung histogram
    source_hist = np.zeros(L, dtype=np.float32)
    target_hist = np.zeros(L, dtype=np.float32)

    for i in range(M):
        for j in range(N):
            source_hist[source_gray[i, j]] += 1

    for i in range(M_t):
        for j in range(N_t):
            target_hist[target_gray[i, j]] += 1

    # LANGKAH 2: NORMALISASI (PDF)
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 2: NORMALISASI HISTOGRAM (PDF)")
    logs.append("=" * 90)
    logs.append(f"\nRUMUS PDF: p(rₖ) = nₖ / (M × N)")

    source_pdf = source_hist / (M * N)
    target_pdf = target_hist / (M_t * N_t)

    # LANGKAH 3: HITUNG CDF
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 3: HITUNG CDF (CUMULATIVE DISTRIBUTION FUNCTION)")
    logs.append("=" * 90)
    logs.append(f"\nRUMUS CDF: T(rₖ) = (L-1) × Σⱼ₌₀ᵏ p(rⱼ)")

    source_cdf = np.cumsum(source_pdf)
    target_cdf = np.cumsum(target_pdf)

    # LANGKAH 4: MEMBUAT MAPPING TABLE
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 4: MEMBUAT TABEL MAPPING (INVERSE MAPPING)")
    logs.append("=" * 90)

    lookup_table = np.zeros(L, dtype=np.uint8)
    mapping_data = []

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
            mapping_data.append({
                'r': r,
                'cdf_s': float(cdf_s),
                'z': best_z,
                'cdf_t': float(target_cdf[best_z]),
                'error': float(min_diff)
            })

    # LANGKAH 5: APLIKASIKAN TRANSFORMASI
    logs.append("\n" + "=" * 90)
    logs.append("LANGKAH 5: APLIKASI TRANSFORMASI PADA CITRA")
    logs.append("=" * 90)

    result_img = cv2.LUT(source_gray, lookup_table)

    # VERIFIKASI HASIL
    logs.append("\n" + "=" * 90)
    logs.append("VERIFIKASI HASIL")
    logs.append("=" * 90)

    result_hist = cv2.calcHist([result_img], [0], None, [256], [0, 256]).flatten()
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

    mse_cdf = np.mean((result_cdf - target_cdf) ** 2)
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
        'mse_cdf': float(mse_cdf)
    }

def create_histogram_plot(hist_data, title, color):
    """Generate histogram plot"""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(256), hist_data, color=color, alpha=0.7, width=1)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlim([0, 255])
    ax.set_xlabel('Intensitas')
    ax.set_ylabel('Frekuensi')
    ax.grid(True, alpha=0.3)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f"data:image/png;base64,{img_base64}"

def create_cdf_plot(cdf_data, title, color, label):
    """Generate CDF plot"""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(256), cdf_data, color=color, linewidth=2.5, label=label)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlim([0, 255])
    ax.set_ylim([0, 1])
    ax.set_xlabel('Intensitas')
    ax.set_ylabel('CDF')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f"data:image/png;base64,{img_base64}"

def create_comparison_plot(source_cdf, target_cdf, result_cdf):
    """Generate CDF comparison plot"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(256), source_cdf, 'b-', label='Citra Asli', linewidth=2)
    ax.plot(range(256), target_cdf, 'g-', label='Citra Target', linewidth=2)
    ax.plot(range(256), result_cdf, 'r--', label='Hasil Specification', linewidth=2.5)
    ax.set_title('Perbandingan CDF Ketiga Citra', fontsize=14, fontweight='bold')
    ax.set_xlabel('Intensitas Piksel')
    ax.set_ylabel('CDF')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return f"data:image/png;base64,{img_base64}"

def img_to_base64(img):
    """Convert image to base64 string"""
    _, buffer = cv2.imencode('.png', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"

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
        # Baca gambar
        source_bytes = np.frombuffer(source_file.read(), np.uint8)
        target_bytes = np.frombuffer(target_file.read(), np.uint8)
        
        source_img = cv2.imdecode(source_bytes, cv2.IMREAD_COLOR)
        target_img = cv2.imdecode(target_bytes, cv2.IMREAD_COLOR)

        # Proses histogram specification
        result = histogram_specification_complete(source_img, target_img)

        # Convert images ke base64
        source_b64 = img_to_base64(result['source_gray'])
        target_b64 = img_to_base64(result['target_gray'])
        result_b64 = img_to_base64(result['result_img'])

        # Generate plots
        hist_source_plot = create_histogram_plot(result['source_hist'], 'Histogram Citra Asli', 'blue')
        hist_target_plot = create_histogram_plot(result['target_hist'], 'Histogram Citra Target', 'green')
        hist_result_plot = create_histogram_plot(result['result_hist'], 'Histogram Hasil', 'red')

        cdf_source_plot = create_cdf_plot(result['source_cdf'], 'CDF Citra Asli', 'blue', 'CDF Asli')
        cdf_target_plot = create_cdf_plot(result['target_cdf'], 'CDF Citra Target', 'green', 'CDF Target')
        cdf_result_plot = create_cdf_plot(result['result_cdf'], 'CDF Hasil', 'red', 'CDF Hasil')

        comparison_plot = create_comparison_plot(result['source_cdf'], result['target_cdf'], result['result_cdf'])

        return jsonify({
            'source': source_b64,
            'target': target_b64,
            'result': result_b64,
            'hist_source': hist_source_plot,
            'hist_target': hist_target_plot,
            'hist_result': hist_result_plot,
            'cdf_source': cdf_source_plot,
            'cdf_target': cdf_target_plot,
            'cdf_result': cdf_result_plot,
            'comparison': comparison_plot,
            'logs': result['logs'],
            'mapping_data': result['mapping_data'],
            'verification_data': result['verification_data'],
            'mse_cdf': result['mse_cdf']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
