"""
Sistem Pakar — Forward Chaining + Certainty Factor
Diagnosa Masalah pada Proses Printing Jersey

Basis Pengetahuan: 10 jenis masalah, 29 gejala
Metode CF: CF_gabungan = CF_pakar * CF_pengguna (disederhanakan = 1.0)
"""

# ─── BASIS PENGETAHUAN ────────────────────────────────────

GEJALA = {
    'G01': 'Warna hasil print berbeda dari layar monitor',
    'G02': 'Warna terlihat lebih merah / kuning dari desain',
    'G03': 'Warna berubah setelah dicuci',
    'G04': 'Gambar terlihat buram atau tidak tajam',
    'G05': 'Tepi gambar kabur / tidak presisi',
    'G06': 'Ada bintik-bintik putih di area solid',
    'G07': 'Detail halus hilang atau tidak tercetak',
    'G08': 'Tinta menyebar keluar dari area desain (bleeding)',
    'G09': 'Tepi desain terlihat berdarah / melebihi batas',
    'G10': 'Gradasi warna tidak halus',
    'G11': 'Warna terlihat pucat / tidak pekat',
    'G12': 'Hasil printing memudar setelah dicuci 1-2 kali',
    'G13': 'Warna putih terlihat kusam / kekuningan',
    'G14': 'Bahan menjadi berkerut / bergelombang setelah press',
    'G15': 'Jersey mengecil setelah proses heat press',
    'G16': 'Permukaan bahan tidak rata / ada bekas lipatan',
    'G17': 'Ada bayangan gambar ganda (ghost image)',
    'G18': 'Terdapat bekas garis dari proses press sebelumnya',
    'G19': 'Ada garis putih horizontal pada hasil print',
    'G20': 'Printer mengeluarkan suara tapi tidak mencetak',
    'G21': 'Nozzle check menunjukkan nozzle hilang / terputus',
    'G22': 'Ada garis-garis horizontal teratur pada hasil print (banding)',
    'G23': 'Kualitas banding lebih parah di bagian tertentu',
    'G24': 'Desain tercetak miring / tidak lurus',
    'G25': 'Ukuran hasil print tidak sesuai dengan file',
    'G26': 'Posisi desain geser dari yang direncanakan',
    'G27': 'Warna / tinta terkelupas setelah dicuci',
    'G28': 'Tinta mudah tergores / tidak menempel kuat',
    'G29': 'Print hanya menempel di permukaan, tidak meresap ke serat kain',
}

DIAGNOSA = [
    {
        'id': 'P01',
        'nama': 'Warna Tidak Akurat / Color Shifting',
        'gejala': ['G01', 'G02', 'G03'],
        'cf_pakar': 0.92,
        'penyebab': [
            'Profil warna ICC tidak dikalibrasi dengan benar',
            'Tinta tidak sesuai dengan spesifikasi substrat',
            'Suhu mesin press tidak stabil atau terlalu tinggi/rendah',
        ],
        'solusi': [
            'Kalibrasi ulang monitor dan printer dengan ICC profile yang sesuai',
            'Gunakan color proof sebelum produksi massal',
            'Periksa dan atur suhu press sesuai spesifikasi bahan (160–210°C)',
            'Ganti tinta dengan kualitas sublimasi dye yang sesuai',
        ],
    },
    {
        'id': 'P02',
        'nama': 'Hasil Print Buram / Tidak Tajam',
        'gejala': ['G04', 'G05', 'G06', 'G07'],
        'cf_pakar': 0.88,
        'penyebab': [
            'Resolusi file desain terlalu rendah (di bawah 150 DPI)',
            'Kepala print (printhead) kotor atau tersumbat sebagian',
            'Kertas transfer basah atau lembab',
            'Posisi bahan bergeser saat proses press',
        ],
        'solusi': [
            'Gunakan resolusi minimal 150 DPI, idealnya 300 DPI untuk desain detail',
            'Bersihkan printhead secara berkala menggunakan cairan pembersih khusus',
            'Simpan kertas transfer di tempat kering, gunakan silica gel',
            'Pasang bahan dengan kuat dan rata di atas platen mesin press',
            'Gunakan kertas anti-geser (non-slip paper) sebagai alas',
        ],
    },
    {
        'id': 'P03',
        'nama': 'Ink Bleeding / Tinta Melebar',
        'gejala': ['G08', 'G09', 'G10'],
        'cf_pakar': 0.85,
        'penyebab': [
            'Suhu press terlalu rendah sehingga sublimasi tidak optimal',
            'Waktu press terlalu singkat',
            'Kandungan polyester dalam bahan kurang dari 60%',
        ],
        'solusi': [
            'Tingkatkan suhu press bertahap (optimal 195–205°C)',
            'Perpanjang waktu press: 35–50 detik untuk kain polyester standar',
            'Pastikan bahan minimal 80% polyester untuk hasil sublimasi terbaik',
            'Lakukan uji coba pada scrap bahan sebelum produksi',
        ],
    },
    {
        'id': 'P04',
        'nama': 'Warna Pucat / Fading',
        'gejala': ['G11', 'G12', 'G13'],
        'cf_pakar': 0.90,
        'penyebab': [
            'Tinta sublimasi kadaluarsa atau kualitas rendah',
            'Profil printing salah (kurang saturasi)',
            'Suhu press kurang optimal',
        ],
        'solusi': [
            'Periksa tanggal kadaluarsa tinta, simpan di suhu 15–25°C',
            'Atur saturasi warna +15–30% di software RIP atau Photoshop',
            'Pastikan suhu press mencapai minimal 190°C untuk saturasi penuh',
            'Gunakan kertas transfer dengan daya serap tinta yang baik',
        ],
    },
    {
        'id': 'P05',
        'nama': 'Bahan Mengkerut / Distorsi',
        'gejala': ['G14', 'G15', 'G16'],
        'cf_pakar': 0.87,
        'penyebab': [
            'Suhu press terlalu tinggi untuk jenis kain tertentu',
            'Tekanan mesin press tidak merata',
            'Bahan tidak diregangkan dengan benar sebelum press',
        ],
        'solusi': [
            'Kurangi suhu press 5–10°C dan uji coba ulang',
            'Kalibrasi tekanan press, pastikan merata di seluruh permukaan',
            'Regangkan bahan rata di atas platen sebelum press',
            'Gunakan silicone pad pelindung antara platen dan bahan',
        ],
    },
    {
        'id': 'P06',
        'nama': 'Bekas Garis / Ghost Image',
        'gejala': ['G17', 'G18'],
        'cf_pakar': 0.82,
        'penyebab': [
            'Bahan bergerak sebelum tinta benar-benar tersublimasi',
            'Kertas transfer tidak langsung dilepas setelah press',
        ],
        'solusi': [
            'Gunakan heat-resistant tape untuk mengunci posisi kertas',
            'Ikuti instruksi peel (cold/hot) sesuai jenis kertas transfer',
            'Tambahkan cooling fan di area keluaran press',
            'Kurangi kelembaban ruangan produksi (<60% RH)',
        ],
    },
    {
        'id': 'P07',
        'nama': 'Printhead Tersumbat / Nozzle Clog',
        'gejala': ['G19', 'G20', 'G21'],
        'cf_pakar': 0.95,
        'penyebab': [
            'Tinta mengering di dalam nozzle akibat printer lama tidak digunakan',
            'Partikel debu atau kontaminan dalam tinta',
            'Suhu ruangan terlalu panas menyebabkan tinta mengental',
        ],
        'solusi': [
            'Lakukan head cleaning otomatis dari menu printer (3–5 siklus)',
            'Rendam printhead menggunakan flush liquid selama 30 menit',
            'Jalankan nozzle check dan power cleaning jika clog parah',
            'Jaga kelembaban ruangan 40–60% RH, suhu 20–28°C',
            'Lakukan print maintenance setiap hari minimal 1 lembar',
        ],
    },
    {
        'id': 'P08',
        'nama': 'Garis Horizontal / Banding',
        'gejala': ['G22', 'G23'],
        'cf_pakar': 0.88,
        'penyebab': [
            'Sebagian nozzle printhead tersumbat parsial',
            'Belt atau encoder strip kotor',
            'Setting bidirectional printing tidak dikalibrasi',
        ],
        'solusi': [
            'Cek nozzle pattern, lakukan head alignment dari menu printer',
            'Bersihkan encoder strip dengan isopropyl alcohol',
            'Nonaktifkan bidirectional printing untuk kualitas lebih tinggi',
            'Ganti printhead jika sudah melewati batas print volume',
        ],
    },
    {
        'id': 'P09',
        'nama': 'Desain Miring / Misregister',
        'gejala': ['G24', 'G25', 'G26'],
        'cf_pakar': 0.80,
        'penyebab': [
            'Bahan tidak diletakkan lurus pada platen',
            'File desain memiliki rotasi yang salah',
            'Pengaturan margin tidak sesuai dengan ukuran bahan',
        ],
        'solusi': [
            'Gunakan garis panduan atau jig positioning untuk memastikan bahan lurus',
            'Periksa rotasi file di software, gunakan 0° untuk posisi normal',
            'Ukur ulang bahan dan sesuaikan margin di RIP software',
            'Buat template ukuran standar untuk setiap jenis jersey',
        ],
    },
    {
        'id': 'P10',
        'nama': 'Hasil Print Tidak Menempel / Peeling',
        'gejala': ['G27', 'G28', 'G29'],
        'cf_pakar': 0.91,
        'penyebab': [
            'Kandungan polyester dalam bahan terlalu rendah (<60%)',
            'Suhu atau waktu press tidak cukup untuk proses sublimasi',
            'Ada lapisan coating pada bahan yang menghalangi sublimasi',
        ],
        'solusi': [
            'Pastikan bahan minimal 80% polyester untuk sublimasi optimal',
            'Tingkatkan suhu ke 200°C dan waktu ke 50–60 detik',
            'Test kain dengan iron-on transfer kecil sebelum produksi massal',
            'Hindari bahan dengan anti-UV atau water-resistant coating',
        ],
    },
]

# ─── FORWARD CHAINING + CF ────────────────────────────────

def diagnosa_masalah(gejala_input: list) -> dict:
    """
    Forward Chaining: mulai dari fakta (gejala) → cari diagnosa yang cocok.
    CF_combined = CF_pakar × (jumlah_gejala_cocok / total_gejala_diagnosa)
    """
    gejala_set = set(gejala_input)
    hasil = []

    for diag in DIAGNOSA:
        gejala_cocok = [g for g in diag['gejala'] if g in gejala_set]
        if not gejala_cocok:
            continue

        # Hitung Certainty Factor
        cf_score = diag['cf_pakar'] * (len(gejala_cocok) / len(diag['gejala']))

        # Level keyakinan
        if cf_score >= 0.70:
            level = 'Tinggi'
        elif cf_score >= 0.40:
            level = 'Sedang'
        else:
            level = 'Rendah'

        # Gejala yang relevan (matched & tidak)
        gejala_detail = []
        for g in diag['gejala']:
            gejala_detail.append({
                'kode':  g,
                'teks':  GEJALA[g],
                'cocok': g in gejala_set,
            })

        hasil.append({
            'id':             diag['id'],
            'nama':           diag['nama'],
            'cf_score':       round(cf_score, 4),
            'cf_persen':      round(cf_score * 100, 1),
            'level':          level,
            'gejala_cocok':   len(gejala_cocok),
            'gejala_total':   len(diag['gejala']),
            'gejala_detail':  gejala_detail,
            'penyebab':       diag['penyebab'],
            'solusi':         diag['solusi'],
        })

    # Urutkan berdasarkan CF tertinggi
    hasil.sort(key=lambda x: x['cf_score'], reverse=True)

    return {
        'diagnosa':        hasil[:3],   # Top 3
        'total_match':     len(hasil),
        'gejala_input':    gejala_input,
        'semua_gejala':    GEJALA,
    }


def get_all_gejala() -> dict:
    """Kembalikan semua daftar gejala."""
    return GEJALA
