# SPPG Battuwinangun — Profil Mitra Dashboard

Web app modern untuk mengelola data **Profil Mitra & SPPG**. Dapat dijalankan langsung dari browser tanpa server backend, dengan keamanan login admin.

## ✨ Fitur

- **Login Admin** — autentikasi dengan password ter-hash (SHA-256), session di browser.
- **Dashboard Realtime** — statistik total mitra, mitra aktif, total honor, peserta BPJS + chart distribusi desil, jenis tugas, jenis kelamin & status.
- **Daftar Mitra** — tabel lengkap, search, filter status / jenis tugas / desil, paginasi.
- **CRUD Mitra** — tambah, edit, hapus dengan validasi & konfirmasi.
- **Impor Excel** — unggah `.xlsx` dengan format sama (header otomatis terdeteksi). Pilihan replace/append.
- **Ekspor Excel & JSON** — unduh data dengan dropdown desil aktif.
- **Reset Data** — kembalikan ke 52 data awal (seed).
- **Pengaturan Password** — ubah password admin (min. 6 karakter).
- **UI Modern** — gradient, glassmorphism, responsive, dark sidebar, color-coded badges.
- **Realtime Cross-Tab** — buka di banyak tab, perubahan langsung sinkron.

## 🚀 Akses

Setelah aktifkan GitHub Pages, link Anda akan menjadi:

```
https://sppgbattuwinangun-lang.github.io/Discuss/
```

### Cara aktifkan GitHub Pages
1. Buka repo: <https://github.com/sppgbattuwinangun-lang/Discuss>
2. **Settings** → **Pages** (sidebar kiri)
3. Pilih **Source: Deploy from a branch**
4. Pilih **Branch: `sinopsis-tesis-s2`** (atau `main` setelah merge), folder **`/docs`**
5. **Save**. Tunggu ~1 menit, refresh halaman → akan muncul URL publik.

## 🔐 Kredensial Default

| Field | Nilai |
|---|---|
| Username | `admin` |
| Password | `sppg2026` |

> **Wajib diganti** setelah login pertama lewat menu **Pengaturan → Ubah Password Admin**.

Password disimpan **hanya di browser** (localStorage) dalam bentuk hash SHA-256. Tidak ada server, tidak ada data dikirim ke pihak luar.

## 📊 Format Data Excel yang Didukung untuk Impor

Header yang dikenali otomatis (case-insensitive):

- `No.` / `Nomor`
- `Kode Validasi` / `Kode`
- `Jenis Tugas` / `Jabatan`
- `Nomor SK Tugas` / `No. SK`
- `Tanggal SK Tugas`
- `Nama` / `Nama Lengkap` / `Nama Penerima`
- `Jenis Kelamin` / `JK`
- `Tanggal Lahir`
- `Usia`
- `Alamat`
- `Telepon` / `No. HP`
- `e-Mail` / `Email`
- `Honor`
- `No. BPJS Ketenagakerjaan` / `BPJS`
- `Status`
- `Desil`

Baris yang mengandung "DOKUMEN INTERNAL" akan dilewati otomatis (footer).

## 🛠 Teknologi

- **Vanilla JavaScript** — tidak ada framework, ringan & cepat.
- **[SheetJS (xlsx)](https://github.com/SheetJS/sheetjs)** — baca & tulis file Excel.
- **[Chart.js 4](https://www.chartjs.org/)** — visualisasi statistik.
- **HTML / CSS3** — Inter & Plus Jakarta Sans, gradient & glassmorphism.

## 📁 Struktur File

```
docs/
├── index.html      # Layout SPA (login + dashboard + tabel + form)
├── styles.css      # UI modern (gradient, glassmorphism, responsive)
├── auth.js         # Login & session management (SHA-256)
├── data.js         # CRUD + import/export Excel + filter
├── app.js          # Controller UI, charts, navigation, toasts
├── seed.json       # Data awal (52 mitra dari Excel)
└── README.md       # Dokumen ini
```

## 🧪 Menjalankan Lokal

Cukup buka `docs/index.html` di Chrome — atau jalankan static server:

```bash
cd docs
python3 -m http.server 8000
# buka http://localhost:8000
```

> Catatan: untuk fitur impor seed.json saat pertama kali, hindari membuka file langsung via `file://` di sebagian browser. Pakai static server atau GitHub Pages.

## 🔄 Reset Data

Untuk kembali ke 52 data awal: **Impor / Ekspor → Reset Data**.
Atau hapus localStorage di DevTools: `localStorage.clear()`.

## 📝 Lisensi

Internal — SPPG Battuwinangun. © 2026
