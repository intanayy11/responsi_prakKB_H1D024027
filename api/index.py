import os
import sys
from flask import Flask, render_template, request, jsonify

# Add api directory to sys.path for local module imports in Vercel
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sistemfuzzy import hitung_harga_fuzzy
from sistempakar import diagnosa_masalah

# Define absolute paths for templates and static files
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, '..', 'templates')
static_dir = os.path.join(base_dir, '..', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# ─── ROUTES ───────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fuzzy')
def fuzzy_page():
    return render_template('fuzzy.html')

@app.route('/pakar')
def pakar_page():
    return render_template('pakar.html')

@app.route('/basis')
def basis_page():
    return render_template('basis.html')

@app.route('/metodologi')
def metodologi_page():
    return render_template('metodologi.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/data-aturan')
def data_aturan_page():
    return render_template('data_aturan.html')

@app.route('/data-gejala')
def data_gejala_page():
    return render_template('data_gejala.html')

# ─── API FUZZY ────────────────────────────────────────────

@app.route('/api/fuzzy', methods=['POST'])
def api_fuzzy():
    data = request.get_json()
    kerumitan = float(data.get('kerumitan', 5))
    warna     = float(data.get('warna', 4))
    material  = float(data.get('material', 1.0))
    teknik    = float(data.get('teknik', 1.0))
    qty       = int(data.get('qty', 20))

    result = hitung_harga_fuzzy(kerumitan, warna, material, teknik, qty)
    return jsonify(result)

# ─── API PAKAR ────────────────────────────────────────────

@app.route('/api/pakar', methods=['POST'])
def api_pakar():
    data    = request.get_json()
    gejala  = data.get('gejala', [])

    result = diagnosa_masalah(gejala)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
