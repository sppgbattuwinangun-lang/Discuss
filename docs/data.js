/* =========================================================
   SPPG Data Layer
   - CRUD mitra di localStorage
   - Pub-sub event "datachange" untuk realtime UI
   - Import / Export Excel (SheetJS)
   - Seed dari docs/seed.json
   ========================================================= */
(function () {
  'use strict';

  const STORAGE_KEY = 'sppg_mitra_data';
  const VERSION_KEY = 'sppg_mitra_version';
  const SEED_URL = 'seed.json';

  const listeners = new Set();
  let cache = null;

  function emit() {
    listeners.forEach((fn) => {
      try { fn(cache); } catch (e) { console.error(e); }
    });
  }

  function uid() {
    return 'm_' + Date.now().toString(36) + '_' +
           Math.random().toString(36).slice(2, 8);
  }

  function load() {
    if (cache) return cache;
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      cache = raw ? JSON.parse(raw) : null;
    } catch (e) {
      cache = null;
    }
    return cache;
  }

  function save(arr) {
    cache = arr;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
    localStorage.setItem(VERSION_KEY, String(Date.now()));
    emit();
  }

  async function fetchSeed() {
    try {
      const res = await fetch(SEED_URL, { cache: 'no-store' });
      if (!res.ok) throw new Error('Gagal memuat seed');
      return await res.json();
    } catch (e) {
      console.warn('Seed tidak tersedia, mulai dengan data kosong.', e);
      return [];
    }
  }

  function normalizeMitra(m, fallbackNo) {
    return {
      id: m.id || uid(),
      no: Number(m.no) || fallbackNo || 0,
      kodeValidasi: String(m.kodeValidasi || '').trim(),
      jenisTugas: String(m.jenisTugas || '').trim(),
      nomorSK: String(m.nomorSK || '').trim(),
      tanggalSK: String(m.tanggalSK || '').trim(),
      nama: String(m.nama || '').trim(),
      jenisKelamin: String(m.jenisKelamin || '').trim(),
      tanggalLahir: String(m.tanggalLahir || '').trim(),
      usia: String(m.usia || '').trim(),
      alamat: String(m.alamat || '').trim(),
      telepon: String(m.telepon || '').trim(),
      email: String(m.email || '').trim(),
      honor: Number(m.honor) || 0,
      noBPJS: String(m.noBPJS || '').trim(),
      status: String(m.status || 'Aktif').trim() || 'Aktif',
      desil: String(m.desil || '').trim(),
      createdAt: m.createdAt || new Date().toISOString(),
      updatedAt: m.updatedAt || new Date().toISOString(),
    };
  }

  async function init() {
    const existing = load();
    if (!existing) {
      const seed = await fetchSeed();
      const arr = seed.map((m, i) => normalizeMitra(m, i + 1));
      save(arr);
    }
    return load();
  }

  function list() {
    return [...(load() || [])];
  }

  function getById(id) {
    return (load() || []).find((m) => m.id === id);
  }

  function add(mitra) {
    const arr = list();
    const next = normalizeMitra(mitra, arr.length + 1);
    arr.push(next);
    save(arr);
    return next;
  }

  function update(id, patch) {
    const arr = list();
    const idx = arr.findIndex((m) => m.id === id);
    if (idx === -1) return null;
    arr[idx] = normalizeMitra({
      ...arr[idx],
      ...patch,
      id: arr[idx].id,
      createdAt: arr[idx].createdAt,
      updatedAt: new Date().toISOString(),
    }, arr[idx].no);
    save(arr);
    return arr[idx];
  }

  function remove(id) {
    const arr = list().filter((m) => m.id !== id);
    arr.forEach((m, i) => (m.no = i + 1));
    save(arr);
  }

  function replaceAll(arr) {
    const cleaned = arr.map((m, i) => normalizeMitra(m, i + 1));
    save(cleaned);
  }

  function appendAll(arr) {
    const current = list();
    arr.forEach((m) => current.push(normalizeMitra(m, current.length + 1)));
    save(current);
  }

  async function reset() {
    localStorage.removeItem(STORAGE_KEY);
    cache = null;
    return init();
  }

  function onChange(fn) {
    listeners.add(fn);
    return () => listeners.delete(fn);
  }

  // === Cross-tab sync ===
  window.addEventListener('storage', (e) => {
    if (e.key === STORAGE_KEY) {
      cache = null;
      load();
      emit();
    }
  });

  /* ---------- Excel I/O ---------- */
  function colMap() {
    return [
      ['no', ['no', 'no.', 'nomor', 'number']],
      ['kodeValidasi', ['kode validasi', 'kode', 'code']],
      ['jenisTugas', ['jenis tugas', 'tugas', 'jabatan']],
      ['nomorSK', ['nomor sk tugas', 'nomor sk', 'no. sk', 'no sk']],
      ['tanggalSK', ['tanggal sk tugas', 'tanggal sk', 'tgl sk']],
      ['nama', ['nama', 'nama lengkap', 'nama penerima', 'nama mitra']],
      ['jenisKelamin', ['jenis kelamin', 'gender', 'jk']],
      ['tanggalLahir', ['tanggal lahir', 'tgl lahir', 'birthdate']],
      ['usia', ['usia', 'age']],
      ['alamat', ['alamat', 'address']],
      ['telepon', ['telepon', 'telp', 'no. hp', 'no hp', 'phone', 'nomor telepon']],
      ['email', ['e-mail', 'email', 'surel']],
      ['honor', ['honor', 'gaji', 'salary']],
      ['noBPJS', ['no. bpjs ketenagakerjaan', 'no bpjs', 'bpjs']],
      ['status', ['status']],
      ['desil', ['desil', 'decile']],
    ];
  }

  function findHeaderRow(rows) {
    // Cari baris yg punya minimal 4 header dikenali
    const map = colMap();
    const knownLowers = new Set(map.flatMap(([, ks]) => ks));
    for (let i = 0; i < Math.min(rows.length, 6); i++) {
      const row = rows[i] || [];
      const matches = row.filter((cell) =>
        knownLowers.has(String(cell || '').trim().toLowerCase())
      ).length;
      if (matches >= 4) return i;
    }
    return 0;
  }

  function parseSheetToMitra(sheet) {
    if (!window.XLSX) throw new Error('SheetJS belum dimuat');
    const aoa = XLSX.utils.sheet_to_json(sheet, {
      header: 1,
      raw: false,
      defval: '',
    });
    const headerIdx = findHeaderRow(aoa);
    const headers = (aoa[headerIdx] || []).map((h) =>
      String(h || '').trim().toLowerCase()
    );
    const map = colMap();
    const colIndex = {};
    headers.forEach((h, i) => {
      for (const [key, candidates] of map) {
        if (candidates.includes(h)) {
          colIndex[key] = i;
          break;
        }
      }
    });

    const rows = aoa.slice(headerIdx + 1);
    const out = [];
    for (const row of rows) {
      if (!row || row.every((c) => String(c || '').trim() === '')) continue;
      // Skip footer baris (mengandung "DOKUMEN INTERNAL")
      const joined = row.map((c) => String(c || '')).join(' ').toLowerCase();
      if (joined.includes('dokumen internal')) continue;

      const m = {};
      for (const key of Object.keys(colIndex)) {
        m[key] = row[colIndex[key]];
      }
      // Skip baris kosong / header tanpa nama
      if (!String(m.nama || '').trim() && !String(m.kodeValidasi || '').trim()) continue;

      m.honor = Number(String(m.honor || 0).replace(/[^\d.-]/g, '')) || 0;
      out.push(m);
    }
    return out;
  }

  async function importFromFile(file, replace) {
    if (!window.XLSX) throw new Error('SheetJS belum dimuat');
    const buf = await file.arrayBuffer();
    const wb = XLSX.read(buf, { type: 'array' });
    const sheetName = wb.SheetNames[0];
    const sheet = wb.Sheets[sheetName];
    const parsed = parseSheetToMitra(sheet);
    if (!parsed.length) throw new Error('Tidak ada baris data terdeteksi');
    if (replace) replaceAll(parsed);
    else appendAll(parsed);
    return parsed.length;
  }

  function exportToExcel(filename) {
    if (!window.XLSX) throw new Error('SheetJS belum dimuat');
    const data = list();
    const headers = [
      'No.', 'Kode Validasi', 'Jenis Tugas', 'Nomor SK Tugas', 'Tanggal SK Tugas',
      'Nama', 'Jenis Kelamin', 'Tanggal Lahir', 'Usia', 'Alamat', 'Telepon',
      'e-Mail', 'Honor', 'No. BPJS Ketenagakerjaan', 'Status', 'Desil',
    ];
    const rows = data.map((m) => [
      m.no, m.kodeValidasi, m.jenisTugas, m.nomorSK, m.tanggalSK,
      m.nama, m.jenisKelamin, m.tanggalLahir, m.usia, m.alamat, m.telepon,
      m.email, m.honor, m.noBPJS, m.status, m.desil,
    ]);
    const aoa = [['Profil Mitra & SPPG'], headers, ...rows];
    const ws = XLSX.utils.aoa_to_sheet(aoa);

    // Merge title
    ws['!merges'] = [{ s: { r: 0, c: 0 }, e: { r: 0, c: headers.length - 1 } }];
    // Column widths
    ws['!cols'] = [
      { wch: 5 }, { wch: 14 }, { wch: 22 }, { wch: 26 }, { wch: 18 },
      { wch: 28 }, { wch: 14 }, { wch: 22 }, { wch: 10 }, { wch: 50 },
      { wch: 16 }, { wch: 28 }, { wch: 14 }, { wch: 22 }, { wch: 12 }, { wch: 10 },
    ];
    // Data validation: kolom Desil (index 15 → kolom P) baris 3..(2+rows.length)
    if (rows.length) {
      ws['!dataValidation'] = [{
        sqref: `P3:P${rows.length + 2}`,
        type: 'list',
        formula1: '"1,2,3,4,5,6-10"',
        allowBlank: true,
        showInputMessage: true,
        promptTitle: 'Pilih Desil',
        prompt: 'Pilih: 1, 2, 3, 4, 5, atau 6-10',
      }];
    }

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Profil Mitra SPPG');
    XLSX.writeFile(wb, filename || `Profil-Mitra-SPPG_${new Date().toISOString().slice(0,10)}.xlsx`);
  }

  function exportToJson(filename) {
    const data = JSON.stringify(list(), null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || `mitra-backup_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  /* ---------- Filter / Search ---------- */
  function filter({ q = '', status = '', tugas = '', desil = '' } = {}) {
    const q1 = q.trim().toLowerCase();
    return list().filter((m) => {
      if (status && m.status !== status) return false;
      if (tugas && m.jenisTugas !== tugas) return false;
      if (desil) {
        if (desil === '(kosong)') {
          if (m.desil) return false;
        } else if (m.desil !== desil) return false;
      }
      if (!q1) return true;
      const blob = [
        m.nama, m.kodeValidasi, m.jenisTugas, m.telepon, m.email,
        m.alamat, m.nomorSK, m.noBPJS,
      ].join(' ').toLowerCase();
      return blob.includes(q1);
    });
  }

  function uniqueValues(field) {
    return [...new Set(list().map((m) => m[field]).filter(Boolean))].sort();
  }

  // Expose
  window.SPPGData = {
    init, list, getById, add, update, remove,
    replaceAll, appendAll, reset, onChange,
    importFromFile, exportToExcel, exportToJson,
    filter, uniqueValues,
  };
})();
