#!/usr/bin/env python3
"""
Membuat SINOPSIS_TESIS_S2.docx - isi PERSIS SAMA seperti SINOPSIS_TESIS.md
Format rapi: Times New Roman 12pt, spasi 1.5, margin normal, tabel rapi.
"""
import zipfile
import os

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

WORD_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/><w:szCs w:val="24"/>
    </w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr>
      <w:spacing w:after="200" w:line="360" w:lineRule="auto"/>
      <w:jc w:val="both"/>
    </w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:pPr><w:jc w:val="center"/><w:spacing w:after="240" w:line="276" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr><w:spacing w:before="480" w:after="240"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr><w:spacing w:before="360" w:after="120"/><w:jc w:val="left"/></w:pPr>
    <w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>
  </w:style>
</w:styles>'''


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def para(text, style=None, bold=False, center=False, italic=False):
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if center:
        ppr_parts.append('<w:jc w:val="center"/>')
    ppr = f'<w:pPr>{"".join(ppr_parts)}</w:pPr>' if ppr_parts else ''
    rpr_parts = []
    if bold:
        rpr_parts.append('<w:b/>')
    if italic:
        rpr_parts.append('<w:i/>')
    rpr = f'<w:rPr>{"".join(rpr_parts)}</w:rPr>' if rpr_parts else ''
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>'


def para_mixed(runs, style=None, center=False):
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if center:
        ppr_parts.append('<w:jc w:val="center"/>')
    ppr = f'<w:pPr>{"".join(ppr_parts)}</w:pPr>' if ppr_parts else ''
    runs_xml = ''
    for text, bold in runs:
        rpr = '<w:rPr><w:b/></w:rPr>' if bold else ''
        runs_xml += f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
    return f'<w:p>{ppr}{runs_xml}</w:p>'


def blank():
    return '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:p>'


def tbl(rows, col_widths, center_cols=None):
    """Tabel rapi dengan cell margin, vertical align top, autofit."""
    if center_cols is None:
        center_cols = []
    total = sum(col_widths)
    t = '<w:tbl><w:tblPr>'
    t += f'<w:tblW w:w="{total}" w:type="dxa"/>'
    t += '<w:tblInd w:w="0" w:type="dxa"/>'
    t += '<w:tblBorders>'
    for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        t += f'<w:{b} w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
    t += '</w:tblBorders>'
    t += '<w:tblCellMar><w:top w:w="60" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="60" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar>'
    t += '</w:tblPr><w:tblGrid>'
    for w in col_widths:
        t += f'<w:gridCol w:w="{w}"/>'
    t += '</w:tblGrid>'

    for i, row in enumerate(rows):
        t += '<w:tr><w:trPr><w:cantSplit/></w:trPr>'
        for j, cell in enumerate(row):
            is_header = (i == 0)
            jc = 'center' if (j in center_cols or is_header) else 'left'
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if is_header else ''
            t += f'<w:tc><w:tcPr><w:tcW w:w="{col_widths[j]}" w:type="dxa"/><w:vAlign w:val="center"/>{shd}</w:tcPr>'
            t += f'<w:p><w:pPr><w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'
            rpr = '<w:rPr><w:b/></w:rPr>' if is_header else ''
            t += f'<w:r>{rpr}<w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p></w:tc>'
        t += '</w:tr>'
    t += '</w:tbl>'
    return t




def build_body():
    b = []

    # ===== JUDUL =====
    b.append(para("SINOPSIS TESIS S2", style="Title", bold=True, center=True))
    b.append(blank())
    b.append(para(
        "Kajian Biodiversitas Ikan Demersal, Kualitas Sedimen, dan Kontaminasi Mikroplastik "
        "sebagai Dasar Keamanan Pangan dalam Distribusi Hasil Perikanan untuk Program "
        "Makan Bergizi Gratis (MBG) melalui Sentra Pengolahan Pangan Gabungan (SPPG)",
        style="Title", bold=True, center=True))
    b.append(blank())

    # ===== BAB I =====
    b.append(para("I. PENDAHULUAN", style="Heading1", bold=True))

    b.append(para("1.1 Latar Belakang", style="Heading2", bold=True))
    b.append(para(
        "Perairan Indonesia menyimpan kekayaan sumber daya ikan demersal yang sangat besar. "
        "Ikan-ikan yang hidup di dasar perairan ini menjadi salah satu sumber protein hewani utama "
        "bagi masyarakat pesisir maupun masyarakat luas. Namun, pemanfaatan hasil tangkapan ikan "
        "demersal untuk konsumsi publik tidak bisa dilakukan begitu saja tanpa memperhatikan aspek keamanan pangan."))
    b.append(para(
        "Dalam beberapa tahun terakhir, pencemaran laut oleh mikroplastik menjadi perhatian serius "
        "di kalangan peneliti dan pemerhati lingkungan. Mikroplastik yang masuk ke dalam tubuh ikan "
        "melalui rantai makanan berpotensi membahayakan kesehatan manusia ketika ikan tersebut dikonsumsi. "
        "Selain itu, kondisi sedimen dan bahan organik di dasar perairan turut mempengaruhi kualitas "
        "ikan yang hidup di zona tersebut."))
    b.append(para(
        "Pemerintah Indonesia saat ini tengah menjalankan program Makan Bergizi Gratis (MBG) yang "
        "bertujuan menyediakan makanan bernutrisi bagi anak-anak sekolah dan kelompok rentan. Salah satu "
        "komponen penting dalam program ini adalah penyediaan protein hewani dari hasil perikanan. "
        "Sentra Pengolahan Pangan Gabungan (SPPG) berperan sebagai unit yang mengolah dan mendistribusikan "
        "bahan pangan, termasuk ikan, untuk mendukung program MBG."))
    b.append(para(
        "Permasalahan muncul ketika ikan yang didistribusikan melalui SPPG belum tentu memenuhi standar "
        "keamanan pangan, terutama terkait kandungan mikroplastik dan kontaminan lainnya. Oleh karena itu, "
        "diperlukan kajian ilmiah yang komprehensif untuk memastikan bahwa ikan demersal yang ditangkap dari "
        "fishing ground aktif layak dan aman untuk dikonsumsi sebelum didistribusikan melalui SPPG ke program MBG."))

    b.append(para("1.2 Rumusan Masalah", style="Heading2", bold=True))
    b.append(para("1. Bagaimana komposisi dan biodiversitas ikan demersal pada fishing ground aktif di wilayah penelitian?"))
    b.append(para("2. Bagaimana kondisi sedimen, bahan organik, dan batimetri pada area penangkapan ikan?"))
    b.append(para("3. Sejauh mana tingkat kontaminasi mikroplastik pada sedimen dan isi perut ikan demersal?"))
    b.append(para("4. Bagaimana kelayakan hasil tangkapan ikan demersal dari aspek keamanan pangan untuk didistribusikan melalui SPPG dalam mendukung program MBG?"))

    b.append(para("1.3 Tujuan Penelitian", style="Heading2", bold=True))
    b.append(para("1. Mengidentifikasi komposisi jenis dan keanekaragaman ikan demersal pada fishing ground aktif."))
    b.append(para("2. Menganalisis karakteristik sedimen, kandungan bahan organik, dan profil batimetri di area penangkapan."))
    b.append(para("3. Mengevaluasi tingkat kontaminasi mikroplastik pada sedimen dasar perairan dan saluran pencernaan ikan demersal."))
    b.append(para("4. Menyusun rekomendasi keamanan pangan sebagai dasar distribusi hasil perikanan melalui SPPG untuk program MBG."))

    b.append(para("1.4 Manfaat Penelitian", style="Heading2", bold=True))
    b.append(para("- Memberikan data ilmiah tentang kondisi sumber daya ikan demersal dan lingkungan perairannya."))
    b.append(para("- Menyediakan informasi tingkat kontaminasi mikroplastik yang dapat digunakan sebagai acuan keamanan pangan."))
    b.append(para("- Menjadi dasar ilmiah bagi SPPG dalam menyeleksi dan mendistribusikan hasil perikanan yang aman untuk program MBG."))
    b.append(para("- Mendukung kebijakan pemerintah dalam menjamin mutu dan keamanan pangan pada program Makan Bergizi Gratis."))

    # ===== BAB II =====
    b.append(para("II. METODOLOGI PENELITIAN", style="Heading1", bold=True))

    b.append(para("2.1 Sumber Data dan Objek Penelitian", style="Heading2", bold=True))
    b.append(para_mixed([
        ("Objek penelitian meliputi ikan demersal, biodiversitas, sedimen, bahan organik, batimetri, "
         "makroplastik, mikroplastik, dan fishing ground aktif. Data diambil dari hasil tangkapan ", False),
        ("sondong", True), (" dan ", False), ("bottom gill net", True),
        (" pada ", False), ("Musim Timur", True), (" dan ", False), ("Musim Peralihan", True), (".", False)]))

    b.append(para("2.2 Metode Penelitian", style="Heading2", bold=True))
    b.append(para("Penelitian ini menggunakan metode deskriptif eksploratif dengan pendekatan komparatif."))

    b.append(para_mixed([("Pengumpulan Data Ikan:", True)]))
    b.append(para("Data ikan dikumpulkan untuk mengetahui biodiversitas ikan demersal. Setiap jenis ikan yang tertangkap dicatat, dihitung, dan diidentifikasi menggunakan buku panduan identifikasi ikan."))

    b.append(para_mixed([("Analisis Sedimen dan Bahan Organik:", True)]))
    b.append(para("Sedimen diambil untuk mengetahui jenis substrat dasar perairan dan kandungan bahan organiknya. Data ini kemudian dikaitkan dengan profil batimetri untuk membuat peta sebaran fishing ground aktif."))

    b.append(para_mixed([("Analisis Makroplastik dan Mikroplastik:", True)]))
    b.append(para("Sampel makroplastik yang ditemukan di area penelitian dikumpulkan, dihitung, dan dikelompokkan berdasarkan jenis dan ukurannya. Mikroplastik dianalisis pada sampel sedimen dan isi perut ikan untuk melihat potensi dampaknya terhadap keamanan pangan."))

    b.append(para_mixed([("Analisis Keamanan Pangan:", True)]))
    b.append(para("Hasil analisis mikroplastik pada ikan dijadikan dasar untuk menilai kelayakan ikan sebagai bahan pangan. Penilaian ini mengacu pada standar keamanan pangan yang berlaku dan menjadi rekomendasi bagi SPPG dalam mendistribusikan hasil perikanan untuk program MBG."))

    b.append(para("2.3 Analisis Data", style="Heading2", bold=True))
    b.append(para("- Indeks keanekaragaman Shannon-Wiener untuk biodiversitas ikan."))
    b.append(para("- Analisis granulometri untuk karakterisasi sedimen."))
    b.append(para("- Identifikasi dan kuantifikasi mikroplastik menggunakan mikroskop dan FTIR."))
    b.append(para("- Analisis deskriptif komparatif antara musim tangkap."))
    b.append(para("- Pemetaan fishing ground menggunakan data batimetri dan sebaran ikan."))

    return '\n'.join(b)



def build_body_part2():
    b = []

    # ===== BAB III =====
    b.append(para("III. INPUT DAN OUTPUT PENELITIAN", style="Heading1", bold=True))

    b.append(para("3.1 Input Penelitian", style="Heading2", bold=True))
    b.append(blank())
    b.append(tbl([
        ("No", "Komponen Input", "Keterangan"),
        ("1", "Data tangkapan ikan demersal", "Hasil tangkapan sondong dan bottom gill net pada Musim Timur dan Musim Peralihan"),
        ("2", "Sampel sedimen dasar perairan", "Diambil dari titik-titik fishing ground aktif"),
        ("3", "Data batimetri", "Kedalaman perairan pada area penangkapan"),
        ("4", "Sampel bahan organik", "Kandungan organik dalam sedimen"),
        ("5", "Sampel makroplastik", "Sampah plastik makro di area penelitian"),
        ("6", "Sampel mikroplastik", "Dari sedimen dan isi perut ikan demersal"),
        ("7", "Data musim penangkapan", "Perbandingan Musim Timur dan Musim Peralihan"),
        ("8", "Standar keamanan pangan", "Regulasi BPOM dan SNI terkait kontaminan pada produk perikanan"),
    ], col_widths=[700, 3100, 5272], center_cols=[0]))
    b.append(blank())

    b.append(para("3.2 Output Penelitian", style="Heading2", bold=True))
    b.append(blank())
    b.append(tbl([
        ("No", "Komponen Output", "Keterangan"),
        ("1", "Daftar jenis dan indeks biodiversitas ikan demersal", "Komposisi spesies beserta nilai keanekaragaman"),
        ("2", "Peta sebaran fishing ground aktif", "Berdasarkan data batimetri dan kepadatan ikan"),
        ("3", "Profil sedimen dan bahan organik", "Karakteristik substrat dasar di area penangkapan"),
        ("4", "Tingkat kontaminasi mikroplastik", "Pada sedimen dan isi perut ikan"),
        ("5", "Penilaian kelayakan keamanan pangan", "Status aman atau tidaknya ikan untuk dikonsumsi"),
        ("6", "Rekomendasi distribusi hasil perikanan untuk SPPG", "Panduan bagi SPPG dalam memilih ikan yang layak untuk program MBG"),
        ("7", "Rekomendasi mitigasi pencemaran", "Langkah-langkah mengurangi dampak mikroplastik terhadap hasil perikanan"),
    ], col_widths=[700, 3600, 4772], center_cols=[0]))
    b.append(blank())

    # ===== BAB IV =====
    b.append(para("IV. KERANGKA PIKIR: KEAMANAN PANGAN UNTUK DISTRIBUSI HASIL PERIKANAN KE SPPG (PROGRAM MBG)", style="Heading1", bold=True))

    b.append(para("4.1 Alur Distribusi yang Diusulkan", style="Heading2", bold=True))
    b.append(blank())

    # Kerangka pikir sebagai tabel vertikal satu kolom (flowchart rapi)
    b.append(tbl([
        ("ALUR DISTRIBUSI HASIL PERIKANAN UNTUK PROGRAM MBG",),
        ("Fishing Ground Aktif",),
        ("\u2193",),
        ("Penangkapan Ikan Demersal (Sondong & Bottom Gill Net)",),
        ("\u2193",),
        ("Uji Kualitas & Keamanan Pangan (Analisis Mikroplastik, Kontaminan, Kesegaran)",),
        ("\u2193",),
        ("[LAYAK] \u2192 Diteruskan ke SPPG (Sentra Pengolahan Pangan Gabungan)",),
        ("[TIDAK LAYAK] \u2192 Ditolak / Dialihkan ke penggunaan non-pangan",),
        ("\u2193",),
        ("Pengolahan & Pengemasan di SPPG",),
        ("\u2193",),
        ("Distribusi ke Program MBG (Sekolah & Kelompok Sasaran)",),
    ], col_widths=[9072], center_cols=[0]))
    b.append(blank())

    b.append(para("4.2 Kriteria Keamanan Pangan untuk Distribusi ke SPPG", style="Heading2", bold=True))
    b.append(para_mixed([("1. Kandungan mikroplastik", True), (" pada isi perut dan daging ikan berada di bawah ambang batas yang ditetapkan.", False)]))
    b.append(para_mixed([("2. Kondisi fishing ground", True), (" tidak tercemar berat berdasarkan analisis sedimen dan bahan organik.", False)]))
    b.append(para_mixed([("3. Kesegaran ikan", True), (" memenuhi standar organoleptik yang berlaku.", False)]))
    b.append(para_mixed([("4. Tidak mengandung kontaminan berbahaya", True), (" lainnya yang melebihi batas aman konsumsi.", False)]))

    b.append(para("4.3 Peran SPPG dalam Program MBG", style="Heading2", bold=True))
    b.append(para("SPPG berfungsi sebagai garda terdepan dalam menjamin mutu pangan yang akan didistribusikan melalui program MBG. Dengan adanya data ilmiah dari penelitian ini, SPPG dapat:"))
    b.append(para("- Menentukan fishing ground mana yang hasil tangkapannya layak digunakan untuk program MBG."))
    b.append(para("- Menetapkan standar penerimaan bahan baku ikan berdasarkan tingkat kontaminasi mikroplastik."))
    b.append(para("- Menyusun jadwal pengadaan ikan berdasarkan musim tangkap yang menghasilkan ikan dengan kualitas terbaik."))
    b.append(para("- Memberikan jaminan keamanan pangan kepada masyarakat penerima manfaat program MBG."))

    # ===== BAB V =====
    b.append(para("V. RENCANA JADWAL PENELITIAN", style="Heading1", bold=True))
    b.append(blank())
    b.append(tbl([
        ("Kegiatan", "Bulan 1-2", "Bulan 3-4", "Bulan 5-6", "Bulan 7-8", "Bulan 9-10"),
        ("Persiapan & survei awal", "X", "", "", "", ""),
        ("Pengambilan data Musim Timur", "", "X", "", "", ""),
        ("Pengambilan data Musim Peralihan", "", "", "X", "", ""),
        ("Analisis laboratorium", "", "", "X", "X", ""),
        ("Pengolahan data & analisis", "", "", "", "X", "X"),
        ("Penulisan tesis", "", "", "", "", "X"),
    ], col_widths=[3572, 1100, 1100, 1100, 1100, 1100], center_cols=[1, 2, 3, 4, 5]))
    b.append(blank())

    # ===== BAB VI =====
    b.append(para("VI. DAFTAR PUSTAKA", style="Heading1", bold=True))
    b.append(blank())
    b.append(para("(Akan dilengkapi sesuai dengan referensi yang digunakan)", italic=True))

    # ===== CATATAN =====
    b.append(blank())
    b.append(para_mixed([
        ("Catatan: ", True),
        ("Sinopsis ini disusun sebagai gambaran umum rencana penelitian tesis S2 yang mengkaji "
         "hubungan antara biodiversitas ikan demersal, kondisi lingkungan perairan, dan keamanan pangan "
         "sebagai landasan ilmiah bagi distribusi hasil perikanan melalui SPPG untuk mendukung program "
         "Makan Bergizi Gratis (MBG) pemerintah Indonesia.", False)]))

    return '\n'.join(b)


def create_docx(output_path):
    body_xml = build_body() + '\n' + build_body_part2()
    doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720"/>
    </w:sectPr>
  </w:body>
</w:document>'''

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', WORD_RELS)
        zf.writestr('word/document.xml', doc)
        zf.writestr('word/styles.xml', STYLES)

    print(f"Berhasil dibuat: {output_path}")
    print(f"Ukuran: {os.path.getsize(output_path):,} bytes")


if __name__ == '__main__':
    create_docx('/projects/sandbox/Discuss/SINOPSIS_TESIS_S2.docx')
