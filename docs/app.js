/* =========================================================
   SPPG Web App — UI controller
   ========================================================= */
(function () {
  'use strict';

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const PAGE_TITLES = {
    dashboard: { title: 'Dashboard', subtitle: 'Ringkasan data Profil Mitra & SPPG' },
    mitra:     { title: 'Profil Mitra', subtitle: 'Daftar lengkap data mitra' },
    tambah:    { title: 'Tambah / Edit Data', subtitle: 'Lengkapi form untuk menyimpan data' },
    impor:     { title: 'Impor / Ekspor', subtitle: 'Unggah Excel atau unduh data Anda' },
    pengaturan:{ title: 'Pengaturan', subtitle: 'Konfigurasi aplikasi & keamanan' },
  };

  const PAGE_SIZE = 10;
  let currentPage = 1;
  let currentEditId = null;
  let charts = {};

  /* ---------- Init ---------- */
  document.addEventListener('DOMContentLoaded', async () => {
    setupLogin();
    setupTogglePassword();
    if (window.SPPGAuth.isAuthenticated()) {
      await enterApp();
    } else {
      showLogin();
    }
    startClock();
  });

  function showLogin() {
    const lv = $('#login-view');
    const av = $('#app-view');
    lv.hidden = false;
    lv.style.display = '';
    av.hidden = true;
    av.style.display = 'none';
  }

  async function enterApp() {
    const lv = $('#login-view');
    const av = $('#app-view');
    lv.hidden = true;
    lv.style.display = 'none';
    av.hidden = false;
    av.style.display = '';
    const session = window.SPPGAuth.getSession();
    if (session) {
      $('#user-name').textContent = session.username;
      $('#user-avatar').textContent = (session.username || 'A')[0].toUpperCase();
    }
    await window.SPPGData.init();
    setupNav();
    setupTable();
    setupForm();
    setupImpor();
    setupSettings();
    setupLogout();
    setupModal();
    window.SPPGData.onChange(() => renderAll());
    renderAll();
  }

  /* ---------- Login ---------- */
  function setupLogin() {
    const form = $('#login-form');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const u = $('#login-username').value;
      const p = $('#login-password').value;
      const remember = $('#remember-me').checked;
      const errBox = $('#login-error');
      errBox.hidden = true;
      const res = await window.SPPGAuth.login(u, p, remember);
      if (res.ok) {
        await enterApp();
      } else {
        errBox.textContent = res.error;
        errBox.hidden = false;
      }
    });
  }
  function setupTogglePassword() {
    const btn = $('#toggle-password');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const inp = $('#login-password');
      inp.type = inp.type === 'password' ? 'text' : 'password';
    });
  }
  function setupLogout() {
    $('#btn-logout').addEventListener('click', () => {
      confirmAction(
        'Keluar Aplikasi',
        'Apakah Anda yakin ingin keluar?',
        () => {
          window.SPPGAuth.logout();
          location.reload();
        },
        { okLabel: 'Keluar', okClass: 'btn-danger' }
      );
    });
  }

  /* ---------- Navigation ---------- */
  function setupNav() {
    $$('.nav-item').forEach((btn) => {
      btn.addEventListener('click', () => navigate(btn.dataset.page));
    });
    $$('[data-page]').forEach((el) => {
      if (el.classList.contains('btn-link')) {
        el.addEventListener('click', () => navigate(el.dataset.page));
      }
    });
    $('#btn-add-mitra').addEventListener('click', () => {
      currentEditId = null;
      $('#mitra-form').reset();
      $('#f-id').value = '';
      $('#form-title').textContent = 'Tambah Data Mitra';
      navigate('tambah');
    });
    $('#btn-cancel-form').addEventListener('click', () => {
      $('#mitra-form').reset();
      currentEditId = null;
      navigate('mitra');
    });
  }
  function navigate(name) {
    $$('.nav-item').forEach((b) => b.classList.toggle('active', b.dataset.page === name));
    $$('.page').forEach((p) => (p.hidden = p.dataset.page !== name));
    const meta = PAGE_TITLES[name] || { title: name, subtitle: '' };
    $('#page-title').textContent = meta.title;
    $('#page-subtitle').textContent = meta.subtitle;
    if (name === 'dashboard') renderDashboard();
    if (name === 'mitra') { currentPage = 1; renderTable(); }
    if (name === 'tambah') populateTugasDatalist();
  }

  /* ---------- Render dispatcher ---------- */
  function renderAll() {
    renderDashboard();
    renderTable();
    populateTugasFilter();
    populateTugasDatalist();
  }

  /* ---------- Dashboard ---------- */
  function renderDashboard() {
    const data = window.SPPGData.list();
    $('#stat-total').textContent = data.length;
    $('#stat-aktif').textContent = data.filter((m) => m.status === 'Aktif').length;
    const totalHonor = data.reduce((s, m) => s + (Number(m.honor) || 0), 0);
    $('#stat-honor').textContent = formatRupiah(totalHonor);
    $('#stat-bpjs').textContent = data.filter((m) => (m.noBPJS || '').replace(/[^\d]/g, '').length >= 5).length;

    renderRecent(data);
    renderCharts(data);
  }
  function renderRecent(data) {
    const recent = [...data]
      .sort((a, b) => new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0))
      .slice(0, 5);
    const list = $('#recent-list');
    if (!recent.length) {
      list.innerHTML = '<div class="muted" style="padding:1rem">Belum ada data.</div>';
      return;
    }
    list.innerHTML = recent.map((m) => `
      <div class="recent-item">
        <div class="recent-avatar" style="background:${avatarColor(m.nama)}">${initials(m.nama)}</div>
        <div>
          <div class="recent-name">${escapeHtml(m.nama)}</div>
          <div class="recent-meta">${escapeHtml(m.jenisTugas || '-')} • ${escapeHtml(m.kodeValidasi || '-')}</div>
        </div>
        <span class="recent-tag ${m.status === 'Aktif' ? 'badge badge-success' : 'badge badge-danger'}">${escapeHtml(m.status)}</span>
        <span class="recent-tag ${desilClass(m.desil)}">${m.desil ? 'Desil ' + escapeHtml(m.desil) : 'Belum diisi'}</span>
      </div>
    `).join('');
  }
  function renderCharts(data) {
    const desilCounts = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6-10': 0, '(belum)': 0 };
    data.forEach((m) => {
      const k = m.desil && desilCounts.hasOwnProperty(m.desil) ? m.desil : '(belum)';
      desilCounts[k]++;
    });
    drawDoughnut('chart-desil', Object.keys(desilCounts), Object.values(desilCounts), [
      '#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981', '#0ea5e9', '#94a3b8',
    ]);

    const tugasMap = {};
    data.forEach((m) => {
      const k = m.jenisTugas || '(Tidak diisi)';
      tugasMap[k] = (tugasMap[k] || 0) + 1;
    });
    const tugasEntries = Object.entries(tugasMap).sort((a, b) => b[1] - a[1]);
    drawBar('chart-tugas',
      tugasEntries.map(e => e[0]),
      tugasEntries.map(e => e[1]),
      '#6366f1');

    const lk = data.filter((m) => m.jenisKelamin === 'Laki-laki').length;
    const pr = data.filter((m) => m.jenisKelamin === 'Perempuan').length;
    const aktif = data.filter((m) => m.status === 'Aktif').length;
    const nonAktif = data.filter((m) => m.status === 'Non-Aktif').length;
    drawGroupedBar('chart-jk',
      ['Laki-laki', 'Perempuan', 'Aktif', 'Non-Aktif'],
      [lk, pr, aktif, nonAktif],
      ['#3b82f6', '#ec4899', '#10b981', '#ef4444']);
  }
  function drawDoughnut(id, labels, dataArr, colors) {
    const ctx = $(`#${id}`);
    if (!ctx) return;
    if (charts[id]) charts[id].destroy();
    charts[id] = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: dataArr,
          backgroundColor: colors,
          borderWidth: 2,
          borderColor: '#fff',
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 11 }, padding: 12, boxWidth: 14 } },
        },
        cutout: '62%',
      },
    });
  }
  function drawBar(id, labels, dataArr, color) {
    const ctx = $(`#${id}`);
    if (!ctx) return;
    if (charts[id]) charts[id].destroy();
    charts[id] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Jumlah',
          data: dataArr,
          backgroundColor: color,
          borderRadius: 6,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { font: { size: 10 } }, grid: { display: false } },
          y: { beginAtZero: true, ticks: { precision: 0, font: { size: 10 } } },
        },
      },
    });
  }
  function drawGroupedBar(id, labels, data, colors) {
    const ctx = $(`#${id}`);
    if (!ctx) return;
    if (charts[id]) charts[id].destroy();
    charts[id] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Jumlah',
          data,
          backgroundColor: colors,
          borderRadius: 6,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false } },
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  /* ---------- Table ---------- */
  function setupTable() {
    $('#search-input').addEventListener('input', () => { currentPage = 1; renderTable(); });
    $('#filter-status').addEventListener('change', () => { currentPage = 1; renderTable(); });
    $('#filter-tugas').addEventListener('change', () => { currentPage = 1; renderTable(); });
    $('#filter-desil').addEventListener('change', () => { currentPage = 1; renderTable(); });
  }
  function populateTugasFilter() {
    const sel = $('#filter-tugas');
    if (!sel) return;
    const cur = sel.value;
    const opts = window.SPPGData.uniqueValues('jenisTugas');
    sel.innerHTML = '<option value="">Semua Jenis Tugas</option>' +
      opts.map((t) => `<option value="${escapeAttr(t)}">${escapeHtml(t)}</option>`).join('');
    sel.value = cur;
  }
  function populateTugasDatalist() {
    const dl = $('#dl-tugas');
    if (!dl) return;
    const opts = window.SPPGData.uniqueValues('jenisTugas');
    dl.innerHTML = opts.map((t) => `<option value="${escapeAttr(t)}">`).join('');
  }
  function getTableFilters() {
    return {
      q: $('#search-input').value,
      status: $('#filter-status').value,
      tugas: $('#filter-tugas').value,
      desil: $('#filter-desil').value,
    };
  }
  function renderTable() {
    const tbody = $('#mitra-tbody');
    if (!tbody) return;
    const all = window.SPPGData.filter(getTableFilters());
    const total = window.SPPGData.list().length;
    const totalPages = Math.max(1, Math.ceil(all.length / PAGE_SIZE));
    if (currentPage > totalPages) currentPage = totalPages;
    const start = (currentPage - 1) * PAGE_SIZE;
    const slice = all.slice(start, start + PAGE_SIZE);

    if (!slice.length) {
      tbody.innerHTML = `
        <tr><td colspan="11" style="text-align:center;padding:3rem;color:var(--text-muted)">
          ${all.length === 0 ? '🔍 Tidak ada data yang cocok dengan filter.' : 'Memuat...'}
        </td></tr>`;
    } else {
      tbody.innerHTML = slice.map((m, i) => `
        <tr>
          <td>${start + i + 1}</td>
          <td><code>${escapeHtml(m.kodeValidasi || '-')}</code></td>
          <td>
            <div class="cell-name">
              <div class="cell-avatar" style="background:${avatarColor(m.nama)}">${initials(m.nama)}</div>
              <div>
                <strong>${escapeHtml(m.nama || '(Tanpa Nama)')}</strong>
                <small>${escapeHtml(m.email || m.telepon || '')}</small>
              </div>
            </div>
          </td>
          <td>${escapeHtml(m.jenisTugas || '-')}</td>
          <td>${jkBadge(m.jenisKelamin)}</td>
          <td>${escapeHtml(m.usia || '-')}</td>
          <td>${escapeHtml(m.telepon || '-')}</td>
          <td>${formatRupiah(m.honor)}</td>
          <td>${desilBadge(m.desil)}</td>
          <td>${statusBadge(m.status)}</td>
          <td>
            <div class="cell-actions">
              <button class="icon-btn edit" title="Edit" data-edit="${m.id}">✏️</button>
              <button class="icon-btn delete" title="Hapus" data-del="${m.id}">🗑️</button>
            </div>
          </td>
        </tr>
      `).join('');
    }

    $('#table-info').textContent = `Menampilkan ${slice.length} dari ${all.length} mitra (total: ${total})`;
    renderPager(totalPages);

    tbody.querySelectorAll('[data-edit]').forEach((b) =>
      b.addEventListener('click', () => editMitra(b.dataset.edit))
    );
    tbody.querySelectorAll('[data-del]').forEach((b) =>
      b.addEventListener('click', () => deleteMitra(b.dataset.del))
    );
  }
  function renderPager(totalPages) {
    const pager = $('#pager');
    if (totalPages <= 1) { pager.innerHTML = ''; return; }
    let html = `<button data-p="${currentPage - 1}" ${currentPage === 1 ? 'disabled' : ''}>‹</button>`;
    const max = Math.min(totalPages, 5);
    let startP = Math.max(1, currentPage - 2);
    let endP = Math.min(totalPages, startP + max - 1);
    startP = Math.max(1, endP - max + 1);
    for (let i = startP; i <= endP; i++) {
      html += `<button data-p="${i}" class="${i === currentPage ? 'active' : ''}">${i}</button>`;
    }
    html += `<button data-p="${currentPage + 1}" ${currentPage === totalPages ? 'disabled' : ''}>›</button>`;
    pager.innerHTML = html;
    pager.querySelectorAll('button[data-p]').forEach((b) =>
      b.addEventListener('click', () => {
        const p = +b.dataset.p;
        if (p >= 1 && p <= totalPages) { currentPage = p; renderTable(); }
      })
    );
  }

  /* ---------- Form ---------- */
  function setupForm() {
    $('#mitra-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const payload = {
        kodeValidasi: $('#f-kode').value.trim(),
        nama: $('#f-nama').value.trim(),
        jenisTugas: $('#f-tugas').value.trim(),
        nomorSK: $('#f-nosk').value.trim(),
        tanggalSK: $('#f-tglsk').value.trim(),
        jenisKelamin: $('#f-jk').value,
        tanggalLahir: $('#f-tgllahir').value.trim(),
        usia: $('#f-usia').value.trim(),
        alamat: $('#f-alamat').value.trim(),
        telepon: $('#f-telp').value.trim(),
        email: $('#f-email').value.trim(),
        honor: Number($('#f-honor').value) || 0,
        noBPJS: $('#f-bpjs').value.trim(),
        status: $('#f-status').value,
        desil: $('#f-desil').value,
      };
      if (currentEditId) {
        window.SPPGData.update(currentEditId, payload);
        toast('success', 'Berhasil diperbarui', `${payload.nama} sudah diperbarui.`);
      } else {
        window.SPPGData.add(payload);
        toast('success', 'Berhasil disimpan', `${payload.nama} ditambahkan.`);
      }
      currentEditId = null;
      $('#mitra-form').reset();
      navigate('mitra');
    });
  }
  function editMitra(id) {
    const m = window.SPPGData.getById(id);
    if (!m) return;
    currentEditId = id;
    $('#form-title').textContent = `Edit: ${m.nama}`;
    $('#f-id').value = m.id;
    $('#f-kode').value = m.kodeValidasi;
    $('#f-nama').value = m.nama;
    $('#f-tugas').value = m.jenisTugas;
    $('#f-nosk').value = m.nomorSK;
    $('#f-tglsk').value = m.tanggalSK;
    $('#f-jk').value = m.jenisKelamin;
    $('#f-tgllahir').value = m.tanggalLahir;
    $('#f-usia').value = m.usia;
    $('#f-alamat').value = m.alamat;
    $('#f-telp').value = m.telepon;
    $('#f-email').value = m.email;
    $('#f-honor').value = m.honor;
    $('#f-bpjs').value = m.noBPJS;
    $('#f-status').value = m.status;
    $('#f-desil').value = m.desil;
    navigate('tambah');
  }
  function deleteMitra(id) {
    const m = window.SPPGData.getById(id);
    if (!m) return;
    confirmAction(
      'Hapus Data Mitra',
      `Hapus permanen data ${m.nama}? Tindakan ini tidak dapat dibatalkan.`,
      () => {
        window.SPPGData.remove(id);
        toast('danger', 'Data dihapus', `${m.nama} telah dihapus.`);
      },
      { okLabel: 'Hapus', okClass: 'btn-danger' }
    );
  }

  /* ---------- Impor / Ekspor ---------- */
  function setupImpor() {
    const fi = $('#file-import');
    $('#btn-import').addEventListener('click', () => fi.click());
    fi.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      try {
        const replace = $('#import-replace').checked;
        const n = await window.SPPGData.importFromFile(file, replace);
        toast('success', 'Impor berhasil', `${n} baris dimuat.`);
        navigate('mitra');
      } catch (err) {
        toast('danger', 'Impor gagal', err.message || String(err));
      } finally {
        fi.value = '';
      }
    });
    $('#btn-export').addEventListener('click', () => {
      try {
        window.SPPGData.exportToExcel();
        toast('success', 'Berhasil', 'File Excel siap diunduh.');
      } catch (err) {
        toast('danger', 'Ekspor gagal', err.message);
      }
    });
    $('#btn-export-json').addEventListener('click', () => {
      window.SPPGData.exportToJson();
      toast('success', 'JSON tersimpan', 'Backup berhasil diunduh.');
    });
    $('#btn-reset').addEventListener('click', () => {
      confirmAction(
        'Reset Data',
        'Yakin ingin mengembalikan ke 52 data awal? Semua perubahan akan hilang.',
        async () => {
          await window.SPPGData.reset();
          toast('warning', 'Data direset', 'Kembali ke data seed.');
        },
        { okLabel: 'Reset', okClass: 'btn-danger' }
      );
    });
  }

  /* ---------- Settings ---------- */
  function setupSettings() {
    $('#form-password').addEventListener('submit', async (e) => {
      e.preventDefault();
      const oldP = $('#old-password').value;
      const newP = $('#new-password').value;
      const conf = $('#confirm-password').value;
      const msg = $('#pw-msg');
      msg.hidden = true;
      msg.classList.remove('alert-danger', 'alert-success');
      if (newP !== conf) {
        msg.textContent = 'Konfirmasi password baru tidak cocok.';
        msg.classList.add('alert-danger');
        msg.hidden = false;
        return;
      }
      const res = await window.SPPGAuth.changePassword(oldP, newP);
      if (res.ok) {
        msg.textContent = 'Password berhasil diubah.';
        msg.classList.add('alert-success');
        msg.hidden = false;
        $('#form-password').reset();
        toast('success', 'Password diubah', 'Gunakan password baru saat login berikutnya.');
      } else {
        msg.textContent = res.error;
        msg.classList.add('alert-danger');
        msg.hidden = false;
      }
    });
  }

  /* ---------- Modal & Toast ---------- */
  function setupModal() {
    $('#modal-cancel').addEventListener('click', closeModal);
    $('#modal-confirm').addEventListener('click', (e) => {
      if (e.target === e.currentTarget) closeModal();
    });
  }
  let modalCallback = null;
  function confirmAction(title, msg, cb, opts = {}) {
    $('#modal-title').textContent = title;
    $('#modal-message').textContent = msg;
    const okBtn = $('#modal-ok');
    okBtn.textContent = opts.okLabel || 'Ya, Lanjutkan';
    okBtn.className = opts.okClass || 'btn-danger';
    modalCallback = cb;
    const m = $('#modal-confirm');
    m.hidden = false;
    m.style.display = '';
    okBtn.onclick = () => {
      closeModal();
      if (modalCallback) modalCallback();
    };
  }
  function closeModal() {
    const m = $('#modal-confirm');
    m.hidden = true;
    m.style.display = 'none';
    modalCallback = null;
  }

  function toast(type, title, message) {
    const stack = $('#toast-stack');
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    const icon = { success: '✅', danger: '❌', warning: '⚠️', info: 'ℹ️' }[type] || 'ℹ️';
    el.innerHTML = `
      <span class="toast-icon">${icon}</span>
      <div><strong>${escapeHtml(title)}</strong><small>${escapeHtml(message || '')}</small></div>
    `;
    stack.appendChild(el);
    setTimeout(() => {
      el.style.transition = 'opacity .3s, transform .3s';
      el.style.opacity = 0;
      el.style.transform = 'translateX(20px)';
      setTimeout(() => el.remove(), 300);
    }, 3500);
  }

  /* ---------- Clock ---------- */
  function startClock() {
    const el = $('#header-time');
    if (!el) return;
    const tick = () => {
      const d = new Date();
      const opts = { weekday: 'short', day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', second: '2-digit' };
      el.textContent = d.toLocaleString('id-ID', opts);
    };
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- Helpers ---------- */
  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function escapeAttr(s) { return escapeHtml(s); }
  function formatRupiah(n) {
    if (!n) return 'Rp 0';
    return 'Rp ' + Number(n).toLocaleString('id-ID');
  }
  function initials(name) {
    if (!name) return '?';
    return name.trim().split(/\s+/).slice(0, 2).map((w) => w[0].toUpperCase()).join('');
  }
  function avatarColor(name) {
    const colors = [
      'linear-gradient(135deg,#6366f1,#4f46e5)',
      'linear-gradient(135deg,#14b8a6,#0d9488)',
      'linear-gradient(135deg,#f59e0b,#d97706)',
      'linear-gradient(135deg,#ec4899,#db2777)',
      'linear-gradient(135deg,#10b981,#059669)',
      'linear-gradient(135deg,#0ea5e9,#0284c7)',
      'linear-gradient(135deg,#a855f7,#9333ea)',
      'linear-gradient(135deg,#f43f5e,#e11d48)',
    ];
    let h = 0;
    for (const c of (name || '')) h = (h * 31 + c.charCodeAt(0)) >>> 0;
    return colors[h % colors.length];
  }
  function jkBadge(jk) {
    if (jk === 'Laki-laki') return '<span class="badge badge-info">♂ L</span>';
    if (jk === 'Perempuan') return '<span class="badge badge-pink">♀ P</span>';
    return '<span class="badge badge-muted">-</span>';
  }
  function statusBadge(s) {
    if (s === 'Aktif') return '<span class="badge badge-success">● Aktif</span>';
    if (s === 'Non-Aktif') return '<span class="badge badge-danger">● Non-Aktif</span>';
    return `<span class="badge badge-muted">${escapeHtml(s)}</span>`;
  }
  function desilBadge(d) {
    if (!d) return '<span class="badge badge-muted">-</span>';
    return `<span class="badge ${desilClass(d)}">Desil ${escapeHtml(d)}</span>`;
  }
  function desilClass(d) {
    if (!d) return 'badge-muted';
    const norm = String(d).replace(/-/g, '');
    return `desil-${norm}`;
  }
})();
