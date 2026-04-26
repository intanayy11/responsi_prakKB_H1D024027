// ─── SLIDER SYNC ─────────────────────────────────────────────

function syncSlider(el, valId) {
  const isInt = el.step >= 1;
  document.getElementById(valId).textContent = isInt ? parseInt(el.value) : parseFloat(el.value).toFixed(1);
  const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
  el.style.background = `linear-gradient(to right, var(--accent) ${pct}%, var(--surface3) ${pct}%)`;
}

// Init sliders on load
['kerumitan', 'warna', 'qty'].forEach(id => {
  const el = document.getElementById(id);
  if (el) syncSlider(el, id + '-val');
});

// ─── SELECTION CARDS ──────────────────────────────────────────
document.querySelectorAll('.selection-grid').forEach(grid => {
  grid.querySelectorAll('.selection-card').forEach(card => {
    card.addEventListener('click', function () {
      grid.querySelectorAll('.selection-card').forEach(c => c.classList.remove('selected'));
      this.classList.add('selected');
    });
  });
});

// ─── RADIO GROUP ─────────────────────────────────────────────

document.querySelectorAll('.radio-group').forEach(group => {
  group.querySelectorAll('.radio-item').forEach(item => {
    item.addEventListener('click', function () {
      group.querySelectorAll('.radio-item').forEach(r => r.classList.remove('selected'));
      this.classList.add('selected');
    });
  });
});

// ─── STEP NAVIGATION ──────────────────────────────────────────
function nextStep(n) {
  // Hide all steps
  document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
  // Show target step
  const target = document.getElementById('step-' + n);
  if (target) {
    target.classList.add('active');
    document.getElementById('input-section').classList.remove('hidden');
    document.getElementById('result-panel').classList.add('hidden');
    document.querySelector('.page-header').style.display = 'block';
  }
  
  // Update progress dots
  document.querySelectorAll('.sp-dot').forEach((dot, i) => {
    if (i + 1 <= n) dot.classList.add('active');
    else dot.classList.remove('active');
  });
}

function resetFuzzy() {
  nextStep(1);
}

// ─── HITUNG FUZZY ────────────────────────────────────────────

async function hitungFuzzy() {
  const btn = document.getElementById('btn-hitung');
  btn.classList.add('loading');
  btn.textContent = 'Menghitung...';

  const payload = {
    kerumitan: parseFloat(document.getElementById('kerumitan').value),
    warna:     parseFloat(document.getElementById('warna').value),
    material:  parseFloat(document.querySelector('#material-group .selection-card.selected')?.dataset.val || '1.0'),
    teknik:    parseFloat(document.querySelector('#teknik-group .selection-card.selected')?.dataset.val || '1.0'),
    qty:       parseInt(document.getElementById('qty').value),
  };

  try {
    const res  = await fetch('/api/fuzzy', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();
    renderFuzzyResult(data);
  } catch (err) {
    alert('Gagal menghubungi server: ' + err.message);
  } finally {
    btn.classList.remove('loading');
    btn.textContent = 'Hitung Estimasi Harga';
  }
}

// ─── RENDER RESULT ────────────────────────────────────────────

function renderFuzzyResult(data) {
  // Hide inputs and original header
  document.getElementById('input-section').classList.add('hidden');
  document.querySelector('.page-header').style.display = 'none';
  
  const panel = document.getElementById('result-panel');
  panel.classList.remove('hidden');

  // Harga
  document.getElementById('res-harga').textContent = 'Rp ' + data.harga.toLocaleString('id-ID');
  document.getElementById('res-range').textContent =
    `Rp ${data.harga_min.toLocaleString('id-ID')} – Rp ${data.harga_max.toLocaleString('id-ID')} per pcs`;

  // Labels
  const kerEl = document.getElementById('res-ker-label');
  kerEl.textContent = data.kerumitan_label;
  kerEl.className = 'mg-val ' + levelClass(data.kerumitan_label, ['Rendah','Sedang','Tinggi']);

  const warEl = document.getElementById('res-war-label');
  warEl.textContent = data.warna_label;
  warEl.className = 'mg-val ' + levelClass(data.warna_label, ['Sedikit','Sedang','Banyak']);

  const katEl = document.getElementById('res-kategori');
  katEl.textContent = data.kategori;
  katEl.className = 'mg-val ' + levelClass(data.kategori, ['Murah','Sedang','Mahal','Sangat Mahal']);

  // Bars
  const mu = data.output_mu;
  const murah  = mu.murah  || 0;
  const sedang = mu.sedang || 0;
  const mahal  = Math.max(mu.mahal || 0, mu.sangat_mahal || 0);

  setBar('bar-murah',  'pct-murah',  murah);
  setBar('bar-sedang', 'pct-sedang', sedang);
  setBar('bar-mahal',  'pct-mahal',  mahal);

  // Insight
  document.getElementById('insight-box').innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; text-align: left;">
      <div>
        <div style="font-size: 0.7rem; font-weight: 800; color: var(--dim); text-transform: uppercase;">Material</div>
        <div style="font-weight: 700;">${data.material_label}</div>
      </div>
      <div>
        <div style="font-size: 0.7rem; font-weight: 800; color: var(--dim); text-transform: uppercase;">Teknik</div>
        <div style="font-weight: 700;">${data.teknik_label}</div>
      </div>
      <div>
        <div style="font-size: 0.7rem; font-weight: 800; color: var(--dim); text-transform: uppercase;">Kuantitas</div>
        <div style="font-weight: 700;">${payload_qty()} Pcs</div>
      </div>
      <div>
        <div style="font-size: 0.7rem; font-weight: 800; color: var(--dim); text-transform: uppercase;">Diskon</div>
        <div style="font-weight: 700;">${data.qty_diskon}</div>
      </div>
    </div>
    <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border); font-size: 0.85rem; color: var(--muted); text-align: left;">
      Estimasi harga diperoleh dari defuzzifikasi centroid Mamdani berdasarkan parameter desain yang Anda masukkan.
    </div>
  `;

  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function setBar(barId, pctId, mu) {
  const pct = Math.round(mu * 100);
  document.getElementById(pctId).textContent = pct + '%';
  document.getElementById(barId).style.width = pct + '%';
}

function payload_qty() {
  return parseInt(document.getElementById('qty')?.value || 20);
}

function levelClass(val, levels) {
  const idx = levels.indexOf(val);
  return ['low','med','high','high'][Math.min(idx, 3)] ?? 'med';
}

// Spin animation for loading
const style = document.createElement('style');
style.textContent = '@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}';
document.head.appendChild(style);
