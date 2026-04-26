// ─── STATE ───────────────────────────────────────────────────
let selectedGejala = new Set();
let allGejala = {};

// ─── INIT ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  loadGejala();
});

async function loadGejala() {
  // Gejala didefinisikan langsung di client (sinkron dengan sistempakar.py)
  allGejala = {
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
  };
  renderGejalaGrid();
}

// ─── RENDER GEJALA ───────────────────────────────────────────
function renderGejalaGrid() {
  const grid = document.getElementById('gejala-grid');
  grid.innerHTML = Object.entries(allGejala).map(([kode, teks]) => `
    <div class="gejala-item" id="gi-${kode}" onclick="toggleGejala('${kode}')">
      <div class="check-box" id="cb-${kode}"></div>
      <span class="gejala-kode">${kode}</span>
      <span>${teks}</span>
    </div>
  `).join('');
}

function toggleGejala(kode) {
  const item = document.getElementById('gi-' + kode);
  const box  = document.getElementById('cb-' + kode);
  if (selectedGejala.has(kode)) {
    selectedGejala.delete(kode);
    item.classList.remove('checked');
    box.textContent = '';
  } else {
    selectedGejala.add(kode);
    item.classList.add('checked');
    box.textContent = '✓';
  }
}

function resetGejala() {
  selectedGejala.clear();
  document.querySelectorAll('.gejala-item').forEach(el => el.classList.remove('checked'));
  document.querySelectorAll('.check-box').forEach(el => el.textContent = '');
  document.getElementById('hasil-panel').classList.add('hidden');
}

// ─── DIAGNOSA ────────────────────────────────────────────────
async function jalankanDiagnosa() {
  if (selectedGejala.size === 0) {
    alert('Pilih minimal 1 gejala terlebih dahulu!');
    return;
  }

  const btn = document.getElementById('btn-diagnosa');
  btn.classList.add('loading');
  btn.textContent = 'Mendiagnosa...';

  try {
    const res  = await fetch('/api/pakar', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ gejala: Array.from(selectedGejala) }),
    });
    const data = await res.json();
    renderHasil(data);
  } catch (err) {
    alert('Gagal menghubungi server: ' + err.message);
  } finally {
    btn.classList.remove('loading');
    btn.textContent = 'Diagnosa Sekarang';
  }
}

// ─── RENDER HASIL ────────────────────────────────────────────
function renderHasil(data) {
  const panel = document.getElementById('hasil-panel');
  const list  = document.getElementById('hasil-list');
  panel.classList.remove('hidden');

  if (!data.diagnosa || data.diagnosa.length === 0) {
    list.innerHTML = `
      <div class="no-result">
        <div class="no-result-icon">●</div>
        <div>Kombinasi gejala tidak cocok dengan basis pengetahuan.</div>
        <div style="margin-top:0.5rem;font-size:0.8rem;color:var(--dim)">Coba pilih lebih banyak gejala atau konsultasikan dengan teknisi.</div>
      </div>`;
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    return;
  }

  list.innerHTML = data.diagnosa.map((d, idx) => {
    const cfClass = d.cf_persen >= 70 ? 'cf-high' : d.cf_persen >= 40 ? 'cf-med' : 'cf-low';
    const cfIcon  = '●';

    const symptomTags = d.gejala_detail.map(g =>
      `<span class="sym-tag ${g.cocok ? 'matched' : ''}">${g.cocok ? '✓ ' : ''}${g.kode}: ${g.teks.substring(0, 38)}${g.teks.length > 38 ? '…' : ''}</span>`
    ).join('');

    const penyebabHTML = d.penyebab.map((p, i) =>
      `<div class="penyebab-item"><span class="penyebab-num">${i+1}</span><span>${p}</span></div>`
    ).join('');

    const solusiHTML = d.solusi.map((s, i) =>
      `<div class="solusi-item"><div class="solusi-num">${i+1}</div><div>${s}</div></div>`
    ).join('');

    return `
      <div class="diagnosa-card">
        <div class="dc-header">
          <div class="dc-rank">#${idx + 1}</div>
          <div>
            <div class="dc-name">${d.nama}</div>
            <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
              <span class="cf-badge ${cfClass}">${cfIcon} Diagnosa Teridentifikasi</span>
              <span style="font-size:0.75rem;color:var(--muted)">${d.gejala_cocok}/${d.gejala_total} gejala cocok</span>
            </div>
          </div>
        </div>
        <div class="dc-body">


          <!-- Gejala tags -->
          <div style="margin-bottom:1rem;">
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--dim);margin-bottom:0.5rem;">Gejala Terkait</div>
            <div class="symptom-tags">${symptomTags}</div>
          </div>

          <!-- Penyebab -->
          <div class="penyebab-list">
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:var(--dim);margin-bottom:0.5rem;">Kemungkinan Penyebab</div>
            ${penyebabHTML}
          </div>

          <!-- Solusi -->
          <div class="solusi-box">
            <div class="solusi-header">Rekomendasi Solusi</div>
            ${solusiHTML}
          </div>
        </div>
      </div>`;
  }).join('');

  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
