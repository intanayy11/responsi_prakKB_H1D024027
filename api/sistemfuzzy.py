"""
Sistem Fuzzy Mamdani
Estimasi Harga Printing Jersey Berdasarkan Tingkat Kerumitan Desain dan Jumlah Warna

Variabel Input:
  1. Kerumitan Desain (0 - 10)
  2. Jumlah Warna     (1 - 12)
  3. Jenis Material   (multiplier)
  4. Teknik Printing  (multiplier)
  5. Jumlah Order/qty (diskon bertingkat)

Variabel Output:
  Harga per pcs (Rp)
  Kategori: murah | sedang | mahal | sangat_mahal
"""

# ─── FUNGSI KEANGGOTAAN ───────────────────────────────────

def trimf(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership function."""
    if x <= a or x >= c:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    if x > b:
        return (c - x) / (c - b)
    return 1.0

def trapmf(x: float, a: float, b: float, c: float, d: float) -> float:
    """Trapezoidal membership function."""
    if x <= a or x >= d:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    if x <= c:
        return 1.0
    return (d - x) / (d - c)

# ─── FUZZIFIKASI ──────────────────────────────────────────

def fuzzifikasi_kerumitan(x: float) -> dict:
    """
    Himpunan Fuzzy Kerumitan Desain:
      - rendah : trapmf [0, 0, 2, 5]
      - sedang : trimf  [2, 5, 8]
      - tinggi : trapmf [6, 8, 10, 10]
    """
    return {
        'rendah': trapmf(x, 0, 0, 2, 5),
        'sedang': trimf(x, 2, 5, 8),
        'tinggi': trapmf(x, 6, 8, 10, 10),
    }

def fuzzifikasi_warna(x: float) -> dict:
    """
    Himpunan Fuzzy Jumlah Warna:
      - sedikit : trapmf [1, 1, 3, 6]
      - sedang  : trapmf [3, 5, 7, 9]
      - banyak  : trapmf [7, 9, 12, 12]
    """
    return {
        'sedikit': trapmf(x, 1, 1, 3, 6),
        'sedang' : trapmf(x, 3, 5, 7, 9),
        'banyak' : trapmf(x, 7, 9, 12, 12),
    }

# ─── INFERENSI MAMDANI ────────────────────────────────────
# Aturan (Rules):
#  R1: kerumitan=Rendah  AND warna=Sedikit → Murah
#  R2: kerumitan=Rendah  AND warna=Sedang  → Murah
#  R3: kerumitan=Rendah  AND warna=Banyak  → Sedang
#  R4: kerumitan=Sedang  AND warna=Sedikit → Sedang
#  R5: kerumitan=Sedang  AND warna=Sedang  → Sedang
#  R6: kerumitan=Sedang  AND warna=Banyak  → Mahal
#  R7: kerumitan=Tinggi  AND warna=Sedikit → Sedang
#  R8: kerumitan=Tinggi  AND warna=Sedang  → Mahal
#  R9: kerumitan=Tinggi  AND warna=Banyak  → Sangat Mahal

def inferensi(mk: dict, mw: dict) -> dict:
    """Evaluasi semua rule, kembalikan derajat keanggotaan output."""
    rules = [
        # (min_operand, output_category)
        (min(mk['rendah'], mw['sedikit']), 'murah'),
        (min(mk['rendah'], mw['sedang']),  'murah'),
        (min(mk['rendah'], mw['banyak']),  'sedang'),
        (min(mk['sedang'], mw['sedikit']), 'sedang'),
        (min(mk['sedang'], mw['sedang']),  'sedang'),
        (min(mk['sedang'], mw['banyak']),  'mahal'),
        (min(mk['tinggi'], mw['sedikit']), 'sedang'),
        (min(mk['tinggi'], mw['sedang']),  'mahal'),
        (min(mk['tinggi'], mw['banyak']),  'sangat_mahal'),
    ]

    fired = []
    output_mu = {'murah': 0.0, 'sedang': 0.0, 'mahal': 0.0, 'sangat_mahal': 0.0}

    LABEL_MAP = {
        'murah':        'Kerumitan Rendah ∧ Warna Sedikit → Murah',
        'sedang':       'Kerumitan Sedang ∧ Warna Sedang → Sedang',
        'mahal':        'Kerumitan Tinggi ∧ Warna Sedang → Mahal',
        'sangat_mahal': 'Kerumitan Tinggi ∧ Warna Banyak → Sangat Mahal',
    }

    rule_labels = [
        'IF Kerumitan=Rendah AND Warna=Sedikit THEN Murah',
        'IF Kerumitan=Rendah AND Warna=Sedang  THEN Murah',
        'IF Kerumitan=Rendah AND Warna=Banyak  THEN Sedang',
        'IF Kerumitan=Sedang AND Warna=Sedikit THEN Sedang',
        'IF Kerumitan=Sedang AND Warna=Sedang  THEN Sedang',
        'IF Kerumitan=Sedang AND Warna=Banyak  THEN Mahal',
        'IF Kerumitan=Tinggi AND Warna=Sedikit THEN Sedang',
        'IF Kerumitan=Tinggi AND Warna=Sedang  THEN Mahal',
        'IF Kerumitan=Tinggi AND Warna=Banyak  THEN Sangat Mahal',
    ]

    for i, (alpha, out_cat) in enumerate(rules):
        if alpha > 0:
            output_mu[out_cat] = max(output_mu[out_cat], alpha)
            fired.append({
                'label':  rule_labels[i],
                'alpha':  round(alpha, 4),
                'output': out_cat,
            })

    return output_mu, fired

# ─── DEFUZZIFIKASI (Weighted Average / Centroid) ──────────

# Titik pusat (centroid) tiap himpunan output (Rp)
OUTPUT_CENTERS = {
    'murah':        30_000,
    'sedang':       75_000,
    'mahal':        135_000,
    'sangat_mahal': 210_000,
}

def defuzzifikasi(output_mu: dict) -> float:
    """Metode centroid / weighted average."""
    num = sum(mu * OUTPUT_CENTERS[cat] for cat, mu in output_mu.items())
    den = sum(output_mu.values())
    if den == 0:
        return 50_000.0
    return num / den

# ─── MAIN FUNCTION ────────────────────────────────────────

MATERIAL_LABELS = {
    1.0:  'Polyester Biasa',
    1.25: 'Polyester Premium',
    1.5:  'Dry-Fit / Mikro',
    1.8:  'Grade Ori / Import',
}

TEKNIK_LABELS = {
    1.0:  'Sublimasi',
    1.3:  'DTF (Direct to Film)',
    1.15: 'Screen Printing',
    1.5:  'Bordir Digital',
}

def hitung_harga_fuzzy(kerumitan: float, warna: float,
                       material: float, teknik: float, qty: int) -> dict:
    """
    Proses lengkap fuzzy Mamdani.
    Return dict berisi harga, detail keanggotaan, rule yang fired, dll.
    """
    # 1. Fuzzifikasi
    mk = fuzzifikasi_kerumitan(kerumitan)
    mw = fuzzifikasi_warna(warna)

    # 2. Inferensi
    output_mu, fired_rules = inferensi(mk, mw)

    # 3. Defuzzifikasi
    base_price = defuzzifikasi(output_mu)

    # 4. Terapkan multiplier material & teknik
    base_price *= material * teknik

    # 5. Diskon kuantitas
    if qty >= 100:
        qty_factor, qty_disc_label = 0.80, '20% (≥100 pcs)'
    elif qty >= 50:
        qty_factor, qty_disc_label = 0.85, '15% (≥50 pcs)'
    elif qty >= 30:
        qty_factor, qty_disc_label = 0.90, '10% (≥30 pcs)'
    elif qty >= 10:
        qty_factor, qty_disc_label = 0.95, '5% (≥10 pcs)'
    else:
        qty_factor, qty_disc_label = 1.0,  'Tidak ada (< 10 pcs)'

    base_price *= qty_factor

    # 6. Pembulatan ke 500
    base_price = round(base_price / 500) * 500
    min_price  = round(base_price * 0.90 / 500) * 500
    max_price  = round(base_price * 1.10 / 500) * 500

    # 7. Tentukan kategori dominan
    dominant = max(output_mu, key=output_mu.get)
    kategori_map = {
        'murah': 'Murah', 'sedang': 'Sedang',
        'mahal': 'Mahal', 'sangat_mahal': 'Sangat Mahal'
    }

    # 8. Label keanggotaan input
    def dominant_label(d):
        return max(d, key=d.get)

    kerumitan_label = {'rendah': 'Rendah', 'sedang': 'Sedang', 'tinggi': 'Tinggi'}[dominant_label(mk)]
    warna_label     = {'sedikit': 'Sedikit', 'sedang': 'Sedang', 'banyak': 'Banyak'}[dominant_label(mw)]

    return {
        'harga':          int(base_price),
        'harga_min':      int(min_price),
        'harga_max':      int(max_price),
        'kategori':       kategori_map[dominant],
        'kerumitan_label': kerumitan_label,
        'warna_label':    warna_label,
        'material_label': MATERIAL_LABELS.get(material, '-'),
        'teknik_label':   TEKNIK_LABELS.get(teknik, '-'),
        'qty_diskon':     qty_disc_label,
        'membership_kerumitan': {k: round(v, 4) for k, v in mk.items()},
        'membership_warna':     {k: round(v, 4) for k, v in mw.items()},
        'output_mu':            {k: round(v, 4) for k, v in output_mu.items()},
        'fired_rules':    fired_rules,
    }
