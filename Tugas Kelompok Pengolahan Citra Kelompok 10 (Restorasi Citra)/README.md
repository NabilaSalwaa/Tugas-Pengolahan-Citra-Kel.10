# Tugas Pengolahan Citra: Pipeline Otomatis

## Deskripsi Percobaan

Percobaan ini bertujuan untuk memahami proses pengolahan citra digital, khususnya dalam hal konversi grayscale, penambahan noise, filtering manual, dan evaluasi kualitas citra menggunakan MSE dan PSNR.

### 1. Pengambilan dan Konversi Citra
- Dua citra digunakan: satu pemandangan (landscape) dan satu objek dekat (potrait).
- Kedua citra dikonversi ke grayscale sehingga didapatkan 4 citra: landscape berwarna, landscape grayscale, potrait berwarna, potrait grayscale.

### 2. Penambahan Noise
- Pada keempat citra, ditambahkan dua jenis noise: salt & pepper dan Gaussian.
- Masing-masing noise diberikan dua tingkatan (level) berbeda.
- Hasil citra ber-noise disimpan di folder `images_noise/`.

### 3. Penghilangan Noise (Filtering)
- Setiap citra ber-noise difilter menggunakan min, max, median, dan mean filter.
- Filtering dilakukan dengan window 3x3 dan 5x5, tanpa menggunakan fungsi filter dari library.
- Hasil filtering disimpan di folder `images_filtered/`.

### 4. Evaluasi dan Analisis
- Kualitas citra hasil filtering dievaluasi dengan menghitung nilai MSE dan PSNR terhadap citra asli.
- Hasil evaluasi dan analisis otomatis tersimpan di folder `hasil_evaluasi/`.
- Visualisasi perbandingan disajikan dalam grafik dan tabel interaktif.
- Tabel gabungan MSE & PSNR memudahkan analisis komprehensif performa filter.

## Cara Menjalankan
1. Pastikan folder `images/` berisi `landscape.jpeg` dan `potrait.jpeg`.
2. Jalankan pipeline dengan perintah:
   ```powershell
   python run_all.py
   ```
   atau jalankan file satu per satu:
   ```powershell
   python 1_konversi_grayscale.py
   python 2_tambah_noise.py
   python 3_filter_noise.py
   python 4_evaluasi_mse.py
   python 5_visualisasi_mse.py
   python 6_tabel_kernel_size.py
   python 7_tabel_mse_psnr_gabungan.py
   ```
3. Hasil akan tersimpan di folder output masing-masing.

## Struktur Output

### File Python
1. **1_konversi_grayscale.py** - Konversi citra ke grayscale
2. **2_tambah_noise.py** - Menambahkan Gaussian dan Salt & Pepper noise
3. **3_filter_noise.py** - Filtering dengan Mean, Median, Max, Min (kernel 3x3 & 5x5)
4. **4_evaluasi_mse.py** - Menghitung MSE dan PSNR
5. **5_visualisasi_mse.py** - Membuat grafik perbandingan MSE
6. **6_tabel_kernel_size.py** - Tabel perbandingan kernel size (MSE only)
7. **7_tabel_mse_psnr_gabungan.py** - Tabel gabungan MSE & PSNR ⭐ **NEW**

### Hasil Visualisasi
- `hasil_evaluasi/grafik_perbandingan_mse.png` - Grafik perbandingan MSE
- `hasil_evaluasi/tabel_kernel_size.png` - Tabel perbandingan kernel (MSE)
- `hasil_evaluasi/tabel_mse_psnr_gabungan.png` - Tabel gabungan MSE & PSNR ⭐ **NEW**

### Dokumentasi Analisis
- `ANALISIS_LENGKAP_EVALUASI.md` - Analisis lengkap semua hasil
- `PENJELASAN_GRAFIK_PERBANDINGAN.md` - Penjelasan detail grafik MSE
- `PENJELASAN_TABEL_KERNEL.md` - Penjelasan tabel kernel size
- `PENJELASAN_TABEL_MSE_PSNR_GABUNGAN.md` - Penjelasan tabel gabungan ⭐ **NEW**

## Analisis

### Kesimpulan Utama (Berdasarkan MSE & PSNR)

#### 🏆 Filter Terbaik: **Median Filter**
- **Gaussian Noise (Portrait)**: MSE = 80.38, PSNR = 29.38 dB
- **Salt & Pepper (Portrait)**: MSE = 43.06, PSNR = 32.03 dB ⭐
- **Robustness**: Performa konsisten di semua kondisi

#### 📊 Perbandingan Per Noise Type:

**1. Gaussian Noise:**
- **Portrait**: Median Filter unggul (MSE ~80, PSNR ~29 dB)
- **Landscape**: Mean Filter lebih efektif (MSE ~336, PSNR ~23 dB)
- **Alasan**: Karakteristik tekstur citra mempengaruhi performa

**2. Salt & Pepper Noise:**
- **Semua Kategori**: Median Filter dominasi mutlak
- **Portrait**: MSE 43.06, PSNR 32.03 dB (hampir sempurna)
- **Landscape**: MSE 307.80, PSNR 23.29 dB (sangat baik)
- **Alasan**: Sifat non-linear mengabaikan nilai ekstrem

#### ⚠️ Filter yang Tidak Efektif: Max & Min
- **Gaussian**: MSE > 2100 (portrait), > 3100 (landscape)
- **Salt & Pepper**: MSE > 4600 (portrait), > 9500 (landscape)
- **PSNR**: Sering < 15 dB (sangat buruk)
- **Kesimpulan**: Memperburuk kualitas citra

### Rekomendasi Kernel Size:
- **Kernel 3x3**: Optimal untuk preservasi detail (90% kasus terbaik)
- **Kernel 5x5**: Berguna pada noise intensitas sangat tinggi
- **Trade-off**: Detail preservation vs Noise reduction

### Metrik Evaluasi:
- **MSE (Lower is Better)**:
  - < 100: Sangat baik
  - 100-500: Baik
  - > 1000: Buruk
  
- **PSNR (Higher is Better)**:
  - > 30 dB: Sangat baik
  - 20-30 dB: Sedang
  - < 20 dB: Buruk

### Detail Analisis:
- Nilai MSE rendah dan PSNR tinggi menunjukkan hasil filtering yang baik.
- Filter median dan mean umumnya lebih efektif untuk menghilangkan noise dibandingkan min dan max.
- Window yang lebih besar dapat menghilangkan noise lebih baik, namun berpotensi mengurangi detail citra.
- Analisis lengkap dapat dilihat di file `hasil_evaluasi/evaluasi_lengkap.txt` dan `PENJELASAN_TABEL_MSE_PSNR_GABUNGAN.md`.

---
Pipeline ini sepenuhnya otomatis dan dapat digunakan untuk eksperimen pengolahan citra digital dasar.
