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
   ```
3. Hasil akan tersimpan di folder output masing-masing.

## Analisis
- Nilai MSE rendah dan PSNR tinggi menunjukkan hasil filtering yang baik.
- Filter median dan mean umumnya lebih efektif untuk menghilangkan noise dibandingkan min dan max.
- Window yang lebih besar dapat menghilangkan noise lebih baik, namun berpotensi mengurangi detail citra.
- Analisis lengkap dapat dilihat di file `hasil_evaluasi/evaluasi_lengkap.txt`.

---
Pipeline ini sepenuhnya otomatis dan dapat digunakan untuk eksperimen pengolahan citra digital dasar.
