#!/usr/bin/env python3
"""
Konten sinopsis tesis S2 - Bahasa manusia 100% akademis
"""
import sys
sys.path.insert(0, '/projects/sandbox/Discuss')
from create_docx import para, empty, make_table


def get_all_paragraphs():
    parts = []
    parts.append(bab_judul())
    parts.append(bab_pendahuluan())
    parts.append(bab_metodologi())
    parts.append(bab_input_output())
    parts.append(bab_kerangka_pikir())
    parts.append(bab_jadwal())
    parts.append(bab_pustaka())
    return '\n'.join(parts)


def bab_judul():
    p = []
    p.append(para("SINOPSIS TESIS MAGISTER", style="Title", bold=True, center=True))
    p.append(empty())
    p.append(para(
        "Kajian Biodiversitas Ikan Demersal, Karakteristik Sedimen, "
        "dan Kontaminasi Mikroplastik di Perairan Fishing Ground Aktif "
        "sebagai Landasan Ilmiah Jaminan Keamanan Pangan "
        "dalam Distribusi Hasil Perikanan melalui Sentra Pengolahan Pangan Gabungan (SPPG) "
        "untuk Mendukung Program Makan Bergizi Gratis (MBG)",
        style="Title", center=True
    ))
    p.append(empty())
    p.append(empty())
    return '\n'.join(p)


def bab_pendahuluan():
    p = []
    p.append(para("BAB I  PENDAHULUAN", style="Heading1", bold=True))
    p.append(empty())

    # 1.1 Latar Belakang
    p.append(para("1.1  Latar Belakang", style="Heading2", bold=True))
    p.append(para(
        "Indonesia memiliki wilayah perairan yang sangat luas dengan potensi sumber daya "
        "hayati laut yang melimpah. Di antara berbagai kelompok biota laut, ikan demersal "
        "menempati posisi penting karena menjadi salah satu komoditas perikanan tangkap "
        "yang banyak dimanfaatkan oleh nelayan tradisional maupun komersial. Ikan-ikan "
        "jenis ini hidup dan mencari makan di sekitar dasar perairan, sehingga kondisi "
        "lingkungan bentik sangat menentukan keberadaan dan kualitas hidupnya."
    ))
    p.append(para(
        "Seiring dengan meningkatnya aktivitas manusia di wilayah pesisir dan laut, "
        "permasalahan pencemaran lingkungan perairan semakin mengkhawatirkan. Salah satu "
        "bentuk pencemaran yang dewasa ini mendapat perhatian besar dari komunitas ilmiah "
        "internasional adalah kontaminasi mikroplastik. Partikel plastik berukuran kurang "
        "dari lima milimeter ini telah ditemukan hampir di seluruh ekosistem laut, mulai "
        "dari permukaan air hingga sedimen dasar. Mikroplastik dapat terakumulasi dalam "
        "tubuh organisme laut melalui proses ingesti, dan berpotensi berpindah ke manusia "
        "melalui konsumsi hasil perikanan."
    ))
    p.append(para(
        "Di sisi lain, pemerintah Republik Indonesia telah meluncurkan program Makan "
        "Bergizi Gratis yang disingkat MBG. Program ini dirancang untuk memenuhi kebutuhan "
        "gizi masyarakat, khususnya anak-anak usia sekolah dan kelompok rentan lainnya, "
        "melalui penyediaan makanan yang mengandung nilai gizi seimbang. Protein hewani "
        "dari ikan menjadi salah satu komponen utama yang diharapkan mampu menunjang "
        "kecukupan gizi penerima manfaat program tersebut."
    ))
    p.append(para(
        "Untuk mendukung kelancaran distribusi bahan pangan dalam program MBG, pemerintah "
        "membentuk Sentra Pengolahan Pangan Gabungan atau yang lazim disebut SPPG. Unit "
        "ini bertanggung jawab dalam menerima, mengolah, dan mendistribusikan bahan pangan "
        "kepada satuan pendidikan dan pos pelayanan lainnya. Dalam konteks perikanan, SPPG "
        "menjadi simpul penting yang menghubungkan hasil tangkapan nelayan dengan kebutuhan "
        "konsumsi masyarakat penerima program MBG."
    ))
    p.append(para(
        "Persoalan mendasar yang belum terjawab secara tuntas adalah apakah ikan demersal "
        "yang ditangkap dari perairan fishing ground aktif benar-benar memenuhi persyaratan "
        "keamanan pangan untuk dikonsumsi manusia. Mengingat adanya potensi kontaminasi "
        "mikroplastik pada tubuh ikan serta pengaruh kondisi sedimen terhadap kualitas "
        "biota, maka diperlukan suatu kajian ilmiah yang mampu memberikan jaminan bahwa "
        "hasil perikanan yang disalurkan melalui SPPG ke program MBG adalah aman dan "
        "layak konsumsi. Penelitian inilah yang hendak dilakukan dalam rangka penyusunan "
        "tesis pada program magister ini."
    ))

    # 1.2 Rumusan Masalah
    p.append(para("1.2  Rumusan Masalah", style="Heading2", bold=True))
    p.append(para(
        "Berdasarkan uraian latar belakang di atas, maka rumusan masalah dalam "
        "penelitian ini adalah sebagai berikut:"
    ))
    p.append(para("1)  Bagaimanakah komposisi jenis dan tingkat keanekaragaman ikan demersal yang terdapat pada fishing ground aktif di lokasi penelitian?"))
    p.append(para("2)  Bagaimanakah karakteristik sedimen dasar perairan ditinjau dari jenis substrat, kandungan bahan organik, serta profil kedalaman pada area penangkapan?"))
    p.append(para("3)  Seberapa besar tingkat kontaminasi mikroplastik yang terdapat pada sedimen dasar perairan dan saluran pencernaan ikan demersal di wilayah kajian?"))
    p.append(para("4)  Bagaimanakah kelayakan hasil tangkapan ikan demersal ditinjau dari aspek keamanan pangan sebagai dasar rekomendasi distribusi melalui SPPG dalam mendukung pelaksanaan program MBG?"))

    # 1.3 Tujuan
    p.append(para("1.3  Tujuan Penelitian", style="Heading2", bold=True))
    p.append(para("Penelitian ini dilaksanakan dengan tujuan sebagai berikut:"))
    p.append(para("1)  Mengidentifikasi dan menganalisis komposisi jenis serta indeks keanekaragaman ikan demersal pada fishing ground aktif."))
    p.append(para("2)  Menganalisis karakteristik sedimen yang meliputi tekstur substrat, kandungan bahan organik, dan profil batimetri di area penangkapan ikan."))
    p.append(para("3)  Mengevaluasi tingkat kontaminasi mikroplastik baik pada sedimen dasar perairan maupun pada saluran pencernaan ikan demersal yang tertangkap."))
    p.append(para("4)  Merumuskan rekomendasi keamanan pangan berbasis bukti ilmiah sebagai acuan bagi SPPG dalam mendistribusikan hasil perikanan untuk program MBG."))

    # 1.4 Manfaat
    p.append(para("1.4  Manfaat Penelitian", style="Heading2", bold=True))
    p.append(para("Secara akademis, penelitian ini diharapkan dapat memperkaya khazanah keilmuan di bidang ekologi perairan, biologi perikanan, dan keamanan pangan. Adapun secara praktis, manfaat yang diharapkan meliputi:"))
    p.append(para("1)  Tersedianya basis data ilmiah mengenai biodiversitas ikan demersal dan kondisi lingkungan bentik pada fishing ground aktif yang dapat dimanfaatkan untuk pengelolaan perikanan berkelanjutan."))
    p.append(para("2)  Teridentifikasinya tingkat kontaminasi mikroplastik pada hasil perikanan sehingga dapat menjadi acuan dalam penetapan standar keamanan pangan nasional."))
    p.append(para("3)  Tersusunnya rekomendasi berbasis bukti yang dapat digunakan oleh SPPG sebagai pedoman dalam menyeleksi dan menyalurkan hasil perikanan yang terjamin keamanannya bagi penerima manfaat program MBG."))
    p.append(para("4)  Terdukungnya kebijakan pemerintah dalam mewujudkan program Makan Bergizi Gratis yang tidak hanya bergizi tinggi tetapi juga aman dari kontaminan berbahaya."))

    return '\n'.join(p)


def bab_metodologi():
    p = []
    p.append(empty())
    p.append(para("BAB II  METODOLOGI PENELITIAN", style="Heading1", bold=True))
    p.append(empty())

    p.append(para("2.1  Lokasi dan Waktu Penelitian", style="Heading2", bold=True))
    p.append(para(
        "Penelitian dilaksanakan pada perairan fishing ground aktif yang secara rutin "
        "dimanfaatkan oleh nelayan setempat untuk kegiatan penangkapan ikan demersal. "
        "Pengambilan data lapangan dilakukan dalam dua periode waktu yang berbeda, yakni "
        "pada Musim Timur dan Musim Peralihan. Pemilihan dua musim ini dimaksudkan untuk "
        "memperoleh gambaran yang lebih representatif mengenai variasi kondisi perairan "
        "dan komposisi hasil tangkapan sepanjang tahun."
    ))

    p.append(para("2.2  Objek dan Subjek Penelitian", style="Heading2", bold=True))
    p.append(para(
        "Objek utama dalam penelitian ini mencakup ikan demersal hasil tangkapan, sedimen "
        "dasar perairan, bahan organik, serta partikel plastik baik dalam skala makro "
        "maupun mikro. Alat tangkap yang digunakan untuk pengambilan sampel ikan adalah "
        "sondong dan jaring insang dasar (bottom gill net), yang merupakan alat tangkap "
        "umum yang dioperasikan oleh nelayan di wilayah kajian."
    ))

    p.append(para("2.3  Pendekatan dan Metode Penelitian", style="Heading2", bold=True))
    p.append(para(
        "Penelitian ini mengadopsi pendekatan deskriptif eksploratif dengan desain "
        "komparatif. Pendekatan ini dipilih karena penelitian bertujuan menggambarkan "
        "kondisi faktual di lapangan sekaligus membandingkan hasil pengamatan antara "
        "dua musim yang berbeda. Metode pengumpulan dan analisis data dirinci sebagai berikut."
    ))

    p.append(para("a.  Pengumpulan Data Biodiversitas Ikan Demersal", bold=True))
    p.append(para(
        "Seluruh ikan demersal yang tertangkap pada setiap operasi penangkapan dicatat "
        "jenis, jumlah individu, dan karakteristik morfologisnya. Identifikasi spesies "
        "dilakukan dengan mengacu pada literatur taksonomi ikan yang berlaku secara "
        "internasional. Data yang diperoleh selanjutnya diolah untuk menghitung indeks "
        "keanekaragaman, indeks keseragaman, dan indeks dominansi."
    ))

    p.append(para("b.  Pengambilan dan Analisis Sampel Sedimen", bold=True))
    p.append(para(
        "Sampel sedimen dasar perairan diambil menggunakan grab sampler pada titik-titik "
        "yang mewakili fishing ground aktif. Analisis yang dilakukan terhadap sampel "
        "sedimen meliputi penentuan tekstur atau granulometri untuk mengetahui komposisi "
        "ukuran butir, serta analisis kandungan bahan organik total. Hasil analisis "
        "sedimen kemudian diintegrasikan dengan data kedalaman perairan untuk menyusun "
        "peta karakteristik habitat bentik."
    ))

    p.append(para("c.  Survei Makroplastik dan Analisis Mikroplastik", bold=True))
    p.append(para(
        "Keberadaan sampah plastik berukuran besar atau makroplastik di area penelitian "
        "didokumentasikan melalui pengamatan langsung dan pengumpulan sampel. Untuk "
        "analisis mikroplastik, sampel diambil dari dua matriks yaitu sedimen dasar "
        "perairan dan isi saluran pencernaan ikan demersal. Ekstraksi mikroplastik "
        "dilakukan menggunakan metode pemisahan densitas, dan identifikasi jenis polimer "
        "dilakukan menggunakan spektroskopi inframerah transformasi Fourier atau FTIR."
    ))

    p.append(para("d.  Penilaian Keamanan Pangan", bold=True))
    p.append(para(
        "Hasil kuantifikasi mikroplastik pada jaringan tubuh ikan dievaluasi terhadap "
        "standar dan regulasi keamanan pangan yang berlaku, baik yang ditetapkan oleh "
        "Badan Pengawas Obat dan Makanan maupun standar nasional Indonesia yang relevan. "
        "Penilaian ini menjadi dasar dalam menyusun rekomendasi kelayakan ikan sebagai "
        "bahan pangan yang akan didistribusikan melalui SPPG."
    ))

    p.append(para("2.4  Teknik Analisis Data", style="Heading2", bold=True))
    p.append(para(
        "Data yang telah dikumpulkan dianalisis menggunakan beberapa pendekatan statistik "
        "dan metode ilmiah, antara lain:"
    ))
    p.append(para("1)  Perhitungan indeks keanekaragaman Shannon-Wiener, indeks keseragaman Pielou, dan indeks dominansi Simpson untuk menggambarkan struktur komunitas ikan demersal."))
    p.append(para("2)  Analisis granulometri dengan metode ayakan bertingkat dan pipet untuk klasifikasi tekstur sedimen."))
    p.append(para("3)  Kuantifikasi dan karakterisasi mikroplastik berdasarkan bentuk, warna, ukuran, dan jenis polimer."))
    p.append(para("4)  Analisis komparatif untuk membandingkan parameter antar musim penangkapan."))
    p.append(para("5)  Pemetaan spasial fishing ground aktif dengan mengintegrasikan data batimetri, sebaran ikan, dan karakteristik sedimen."))

    return '\n'.join(p)


def bab_input_output():
    p = []
    p.append(empty())
    p.append(para("BAB III  INPUT DAN OUTPUT PENELITIAN", style="Heading1", bold=True))
    p.append(empty())

    p.append(para("3.1  Input Penelitian", style="Heading2", bold=True))
    p.append(para(
        "Berikut adalah komponen data dan material yang menjadi masukan dalam pelaksanaan penelitian ini:"
    ))
    p.append(empty())

    input_data = [
        ("No.", "Komponen Input", "Deskripsi"),
        ("1", "Hasil tangkapan ikan demersal",
         "Spesimen ikan yang diperoleh dari operasi penangkapan menggunakan sondong dan bottom gill net pada dua musim berbeda"),
        ("2", "Sampel sedimen dasar perairan",
         "Material substrat yang diambil dari titik-titik sampling pada fishing ground aktif menggunakan grab sampler"),
        ("3", "Data kedalaman perairan",
         "Informasi batimetri yang diperoleh melalui pengukuran langsung di lapangan pada setiap stasiun pengamatan"),
        ("4", "Sampel bahan organik",
         "Fraksi organik yang terkandung dalam sedimen dasar perairan di area penangkapan"),
        ("5", "Sampel makroplastik",
         "Material plastik berukuran besar yang ditemukan di perairan dan dasar laut area penelitian"),
        ("6", "Sampel mikroplastik",
         "Partikel plastik berukuran kurang dari lima milimeter yang diekstraksi dari sedimen dan saluran pencernaan ikan"),
        ("7", "Data kondisi musim",
         "Parameter oseanografi dan meteorologi pada Musim Timur dan Musim Peralihan sebagai variabel pembanding"),
        ("8", "Regulasi keamanan pangan",
         "Peraturan BPOM, Standar Nasional Indonesia, dan rujukan internasional terkait batas aman kontaminan pada produk perikanan"),
    ]
    p.append(make_table(input_data))

    p.append(empty())
    p.append(para("3.2  Output Penelitian", style="Heading2", bold=True))
    p.append(para(
        "Adapun luaran yang diharapkan dari pelaksanaan penelitian ini adalah sebagai berikut:"
    ))
    p.append(empty())

    output_data = [
        ("No.", "Komponen Output", "Deskripsi"),
        ("1", "Inventarisasi biodiversitas ikan demersal",
         "Daftar spesies lengkap beserta nilai indeks keanekaragaman, keseragaman, dan dominansi pada masing-masing musim"),
        ("2", "Peta sebaran fishing ground aktif",
         "Peta tematik yang menunjukkan lokasi konsentrasi ikan demersal berdasarkan integrasi data tangkapan, batimetri, dan sedimen"),
        ("3", "Profil karakteristik sedimen",
         "Deskripsi tekstur substrat dan kandungan bahan organik pada setiap stasiun pengamatan"),
        ("4", "Status kontaminasi mikroplastik",
         "Data kuantitatif dan kualitatif mengenai kelimpahan, bentuk, dan jenis polimer mikroplastik pada sedimen dan ikan"),
        ("5", "Penilaian kelayakan keamanan pangan",
         "Hasil evaluasi tingkat kontaminasi terhadap ambang batas yang ditetapkan dalam regulasi keamanan pangan"),
        ("6", "Rekomendasi distribusi untuk SPPG",
         "Dokumen pedoman ilmiah bagi SPPG dalam menyeleksi hasil perikanan yang layak didistribusikan untuk program MBG"),
        ("7", "Strategi mitigasi pencemaran",
         "Rumusan langkah-langkah pengendalian dan pengurangan dampak kontaminasi plastik terhadap hasil perikanan"),
    ]
    p.append(make_table(output_data))

    return '\n'.join(p)


def bab_kerangka_pikir():
    p = []
    p.append(empty())
    p.append(para("BAB IV  KERANGKA PIKIR", style="Heading1", bold=True))
    p.append(para("Keamanan Pangan sebagai Dasar Distribusi Hasil Perikanan ke SPPG untuk Program MBG", style="Heading2", bold=True))
    p.append(empty())

    p.append(para("4.1  Landasan Pemikiran", style="Heading2", bold=True))
    p.append(para(
        "Keberhasilan program Makan Bergizi Gratis tidak semata-mata ditentukan oleh "
        "tercukupinya jumlah kalori dan nutrisi, melainkan juga oleh terjaminnya keamanan "
        "bahan pangan yang disajikan. Dalam konteks penyediaan protein hewani dari sektor "
        "perikanan, perlu dipastikan bahwa ikan yang didistribusikan kepada penerima manfaat "
        "tidak mengandung kontaminan yang dapat membahayakan kesehatan. Penelitian ini "
        "dibangun di atas pemikiran bahwa data ilmiah mengenai kondisi lingkungan perairan "
        "dan tingkat kontaminasi pada ikan harus menjadi dasar pengambilan keputusan dalam "
        "rantai distribusi pangan."
    ))

    p.append(para("4.2  Alur Distribusi Berbasis Jaminan Keamanan Pangan", style="Heading2", bold=True))
    p.append(para(
        "Berdasarkan kerangka pemikiran tersebut, alur distribusi hasil perikanan yang "
        "diusulkan dalam penelitian ini terdiri atas tahapan-tahapan berikut:"
    ))
    p.append(para("Tahap Pertama: Penangkapan ikan demersal dilakukan di fishing ground aktif yang telah dipetakan dan dikaji kondisi lingkungannya."))
    p.append(para("Tahap Kedua: Hasil tangkapan menjalani serangkaian uji keamanan pangan yang meliputi pemeriksaan kontaminasi mikroplastik, evaluasi kesegaran organoleptik, dan verifikasi terhadap standar mutu yang berlaku."))
    p.append(para("Tahap Ketiga: Ikan yang dinyatakan memenuhi seluruh persyaratan keamanan pangan diteruskan ke SPPG untuk diproses lebih lanjut."))
    p.append(para("Tahap Keempat: SPPG melakukan pengolahan, pengemasan, dan pendistribusian produk perikanan kepada satuan pendidikan dan pos pelayanan dalam kerangka program MBG."))
    p.append(para("Tahap Kelima: Ikan yang tidak memenuhi standar keamanan pangan dialihkan pemanfaatannya ke sektor non-pangan atau dikembalikan dengan catatan evaluasi."))

    p.append(para("4.3  Parameter Keamanan Pangan untuk Seleksi Distribusi", style="Heading2", bold=True))
    p.append(para("Kriteria yang digunakan sebagai dasar penilaian kelayakan distribusi meliputi:"))
    p.append(para("1)  Jumlah dan jenis partikel mikroplastik yang terdeteksi pada jaringan tubuh ikan tidak melampaui ambang batas yang ditetapkan oleh otoritas keamanan pangan."))
    p.append(para("2)  Fishing ground tempat ikan ditangkap tidak menunjukkan indikasi pencemaran berat berdasarkan hasil analisis sedimen dan bahan organik."))
    p.append(para("3)  Kondisi organoleptik ikan pada saat penerimaan di SPPG memenuhi persyaratan kesegaran sesuai standar yang berlaku."))
    p.append(para("4)  Tidak terdeteksi adanya kontaminan kimia berbahaya lainnya yang melebihi kadar maksimum yang diizinkan."))

    p.append(para("4.4  Kedudukan SPPG dalam Rantai Jaminan Keamanan Pangan", style="Heading2", bold=True))
    p.append(para(
        "Dalam kerangka penelitian ini, SPPG diposisikan sebagai institusi yang memiliki "
        "kewenangan dan tanggung jawab untuk menjamin bahwa setiap produk perikanan yang "
        "memasuki rantai distribusi program MBG telah melalui proses verifikasi keamanan "
        "pangan. Dengan tersedianya data ilmiah dari penelitian ini, SPPG dapat menjalankan "
        "fungsinya secara lebih efektif melalui:"
    ))
    p.append(para("1)  Penetapan daftar fishing ground yang hasil tangkapannya memenuhi syarat untuk masuk ke program MBG berdasarkan kajian lingkungan perairan."))
    p.append(para("2)  Penerapan protokol penerimaan bahan baku ikan yang mencantumkan batas toleransi kontaminasi mikroplastik."))
    p.append(para("3)  Penyusunan kalender pengadaan yang mempertimbangkan musim tangkap dengan kualitas hasil perikanan terbaik."))
    p.append(para("4)  Pemberian sertifikasi kelayakan pangan pada setiap lot produk yang akan didistribusikan kepada penerima manfaat."))

    return '\n'.join(p)


def bab_jadwal():
    p = []
    p.append(empty())
    p.append(para("BAB V  RENCANA JADWAL PELAKSANAAN PENELITIAN", style="Heading1", bold=True))
    p.append(empty())
    p.append(para(
        "Pelaksanaan penelitian direncanakan berlangsung selama sepuluh bulan dengan "
        "rincian kegiatan sebagai berikut:"
    ))
    p.append(empty())

    jadwal = [
        ("Kegiatan", "Bulan 1-2", "Bulan 3-4", "Bulan 5-6", "Bulan 7-8", "Bulan 9-10"),
        ("Penyusunan proposal dan persiapan alat", "V", "", "", "", ""),
        ("Survei pendahuluan dan penentuan stasiun", "V", "", "", "", ""),
        ("Pengambilan data lapangan Musim Timur", "", "V", "", "", ""),
        ("Pengambilan data lapangan Musim Peralihan", "", "", "V", "", ""),
        ("Analisis laboratorium", "", "", "V", "V", ""),
        ("Pengolahan dan analisis data", "", "", "", "V", "V"),
        ("Penulisan dan penyusunan naskah tesis", "", "", "", "V", "V"),
        ("Seminar hasil dan ujian tesis", "", "", "", "", "V"),
    ]
    p.append(make_table(jadwal))

    return '\n'.join(p)


def bab_pustaka():
    p = []
    p.append(empty())
    p.append(para("BAB VI  DAFTAR PUSTAKA", style="Heading1", bold=True))
    p.append(empty())
    p.append(para(
        "(Daftar pustaka akan disusun dan dilengkapi berdasarkan seluruh sumber referensi "
        "ilmiah yang digunakan dalam penyusunan proposal dan pelaksanaan penelitian, "
        "dengan mengikuti format penulisan yang ditetapkan oleh program studi.)"
    ))
    p.append(empty())
    p.append(empty())
    p.append(para(
        "Sinopsis ini disusun sebagai kerangka awal rencana penelitian tesis magister "
        "yang hendak mengkaji secara komprehensif hubungan antara biodiversitas ikan "
        "demersal, kualitas lingkungan bentik, dan status kontaminasi mikroplastik "
        "sebagai landasan ilmiah dalam menjamin keamanan pangan hasil perikanan yang "
        "didistribusikan melalui Sentra Pengolahan Pangan Gabungan untuk mendukung "
        "keberhasilan program Makan Bergizi Gratis di Indonesia."
    ))
    return '\n'.join(p)
