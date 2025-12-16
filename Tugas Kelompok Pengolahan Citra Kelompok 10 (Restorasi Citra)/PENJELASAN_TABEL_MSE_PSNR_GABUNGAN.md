# Penjelasan Tabel Gabungan MSE & PSNR

## 📊 Overview

Tabel ini menggabungkan dua metrik evaluasi penting (MSE dan PSNR) dalam satu visualisasi untuk memudahkan analisis performa filter dalam restorasi citra. Setiap sel menampilkan nilai MSE dan PSNR secara bersamaan, sehingga perbandingan dapat dilakukan dengan lebih komprehensif.

## 🎯 Metrik yang Digunakan

### 1. MSE (Mean Squared Error)
- **Definisi**: Rata-rata kuadrat selisih antara pixel citra asli dan citra hasil filtering
- **Interpretasi**: **Nilai lebih RENDAH = Lebih BAIK**
- **Formula**: MSE = (1/N) Σ(original - filtered)²

**Kategori Kualitas MSE:**
- 🟢 **MSE < 100**: Kualitas sangat baik (sel berwarna hijau)
- 🟡 **MSE 100-500**: Kualitas baik (sel berwarna kuning)
- 🟠 **MSE 500-1000**: Kualitas sedang (sel berwarna orange)
- 🔴 **MSE > 1000**: Kualitas buruk (sel berwarna merah)

### 2. PSNR (Peak Signal-to-Noise Ratio)
- **Definisi**: Rasio antara nilai maksimum pixel dengan MSE (dalam dB)
- **Interpretasi**: **Nilai lebih TINGGI = Lebih BAIK**
- **Formula**: PSNR = 10 × log₁₀(MAX²/MSE) = 20 × log₁₀(MAX/√MSE)

**Kategori Kualitas PSNR:**
- 🟢 **PSNR > 30 dB**: Kualitas sangat baik (restorasi hampir sempurna)
- 🟡 **PSNR 20-30 dB**: Kualitas sedang (restorasi cukup baik)
- 🔴 **PSNR < 20 dB**: Kualitas buruk (restorasi tidak efektif)

## 📈 Hasil Analisis Lengkap

### A. Gaussian Noise

#### 1. **Portrait Images**
| Filter | MSE Rata-rata | PSNR Rata-rata | Kualitas |
|--------|--------------|----------------|----------|
| **Median** ⭐ | **80.38** | **29.38 dB** | **Sangat Baik** |
| Mean | 122.27 | 27.67 dB | Baik |
| Min | 1068.41 | 18.39 dB | Buruk |
| Max | 2114.98 | 15.71 dB | Sangat Buruk |

**Analisis:**
- **Median Filter** unggul dengan MSE hanya 80.38 dan PSNR mendekati 30 dB
- Cocok untuk region homogen seperti kulit wajah karena dapat mengeliminasi outlier
- Mean Filter posisi kedua dengan performa yang masih cukup baik
- Max dan Min Filter gagal total dengan PSNR < 20 dB

#### 2. **Landscape Images**
| Filter | MSE Rata-rata | PSNR Rata-rata | Kualitas |
|--------|--------------|----------------|----------|
| **Mean** ⭐ | **335.72** | **22.91 dB** | **Sedang** |
| Median | 360.89 | 22.60 dB | Sedang |
| Max | 3212.58 | 13.43 dB | Buruk |
| Min | 3309.27 | 13.29 dB | Buruk |

**Analisis:**
- **Mean Filter** lebih efektif untuk tekstur kompleks landscape
- Smoothing-nya cocok untuk variasi detail yang tinggi
- Median Filter sedikit tertinggal tapi masih dalam kategori sedang
- Max dan Min Filter tetap buruk dengan MSE > 3000

### B. Salt & Pepper Noise

#### 1. **Portrait Images**
| Filter | MSE Rata-rata | PSNR Rata-rata | Kualitas |
|--------|--------------|----------------|----------|
| **Median** ⭐ | **43.06** | **32.03 dB** | **Sangat Baik** |
| Mean | 362.94 | 23.26 dB | Sedang |
| Min | 4663.63 | 11.90 dB | Sangat Buruk |
| Max | 23148.60 | 4.99 dB | Extremely Bad |

**Analisis:**
- **Median Filter** dominasi mutlak dengan MSE sangat rendah (43.06)
- PSNR 32.03 dB mengindikasikan restorasi hampir sempurna
- Sifat non-linear-nya sangat efektif mengabaikan nilai ekstrem (0 atau 255)
- Mean Filter jauh tertinggal di posisi kedua
- Max dan Min Filter memperburuk kondisi dengan menyebarkan noise

#### 2. **Landscape Images**
| Filter | MSE Rata-rata | PSNR Rata-rata | Kualitas |
|--------|--------------|----------------|----------|
| **Median** ⭐ | **307.80** | **23.29 dB** | **Baik** |
| Mean | 471.65 | 21.50 dB | Sedang |
| Max | 9503.79 | 8.76 dB | Sangat Buruk |
| Min | 11181.01 | 8.06 dB | Sangat Buruk |

**Analisis:**
- **Median Filter** tetap terbaik meskipun di landscape dengan tekstur kompleks
- Performa tetap konsisten dengan PSNR > 20 dB
- Mean Filter masih bisa digunakan sebagai alternatif
- Max dan Min Filter sama sekali tidak efektif

## 📊 Perbandingan Kernel Size

### Overall Performance

#### Gaussian Noise:
| Filter | 3x3 MSE | 3x3 PSNR | 5x5 MSE | 5x5 PSNR | Terbaik |
|--------|---------|----------|---------|----------|---------|
| **Mean** ⭐ | **207.55** | **25.77 dB** | 250.44 | 24.80 dB | **3x3** |
| Median | 213.45 | 26.10 dB | 227.82 | 25.88 dB | 3x3 |
| Max | 1978.09 | 15.74 dB | 3349.47 | 13.39 dB | 3x3 |
| Min | 1598.53 | 17.17 dB | 2779.14 | 14.51 dB | 3x3 |

#### Salt & Pepper Noise:
| Filter | 3x3 MSE | 3x3 PSNR | 5x5 MSE | 5x5 PSNR | Terbaik |
|--------|---------|----------|---------|----------|---------|
| **Median** ⭐ | **149.62** | **28.57 dB** | 201.24 | 26.76 dB | **3x3** |
| Mean | 458.47 | 21.96 dB | 376.12 | 22.80 dB | 5x5 |
| Max | 11326.30 | 8.31 dB | 21326.09 | 5.44 dB | 3x3 |
| Min | 5636.96 | 11.38 dB | 10207.68 | 8.58 dB | 3x3 |

**Kesimpulan Kernel Size:**
- **Kernel 3x3** secara umum lebih unggul karena:
  - Menjaga keseimbangan antara reduksi noise dan preservasi detail
  - MSE lebih rendah dan PSNR lebih tinggi pada mayoritas kasus
  - Tidak menimbulkan over-smoothing yang berlebihan
  
- **Kernel 5x5** bisa berguna pada:
  - Intensitas noise sangat tinggi
  - Kasus tertentu seperti Mean Filter pada Salt & Pepper Noise
  - Ketika smoothing lebih agresif diperlukan

## 🎯 Kesimpulan Utama

### 1. **Median Filter = Juara Umum** 🏆
- Terbaik untuk **Salt & Pepper Noise** dengan performa luar biasa
- MSE: 43.06 (portrait) dan 307.80 (landscape)
- PSNR: 32.03 dB (portrait) dan 23.29 dB (landscape)
- Sangat baik untuk **Gaussian Noise** pada portrait
- Robustness terbaik terhadap perubahan intensitas noise

### 2. **Mean Filter = Runner-up untuk Gaussian**
- Pilihan terbaik untuk **Gaussian Noise pada landscape**
- Smoothing cocok untuk tekstur kompleks
- Performa konsisten tapi kurang efektif untuk Salt & Pepper

### 3. **Kernel 3x3 = Pilihan Optimal**
- Unggul dalam 90% kasus
- Balance terbaik antara noise reduction dan detail preservation
- Computational cost lebih rendah

### 4. **Max & Min Filter = Tidak Direkomendasikan** ❌
- MSE sangat tinggi (>1000 untuk Gaussian, >5000 untuk Salt & Pepper)
- PSNR sangat rendah (sering < 15 dB)
- Memperburuk kualitas citra alih-alih memperbaiki
- Menyebarkan noise alih-alih menguranginya

## 💡 Rekomendasi Praktis

### Berdasarkan Jenis Noise:

**1. Untuk Gaussian Noise:**
- **First Choice**: Median Filter (3x3) - untuk portrait
- **Alternative**: Mean Filter (3x3) - untuk landscape
- **PSNR Target**: > 25 dB
- **MSE Target**: < 250

**2. Untuk Salt & Pepper Noise:**
- **Only Choice**: Median Filter (3x3) ⭐
- **No Alternative**: Filter lain tidak efektif
- **PSNR Target**: > 28 dB
- **MSE Target**: < 200

### Berdasarkan Jenis Citra:

**1. Portrait/Human Faces:**
- Prioritas: **Detail preservation** (texture kulit, mata, rambut)
- Filter: **Median 3x3**
- Expected PSNR: 29-32 dB
- Expected MSE: < 100

**2. Landscape/Scenery:**
- Prioritas: **Overall smoothness**
- Filter: **Mean 3x3** (Gaussian) atau **Median 3x3** (Salt & Pepper)
- Expected PSNR: 22-24 dB
- Expected MSE: 300-400

## 📌 Catatan Penting

1. **MSE dan PSNR adalah metrik komplementer**
   - MSE memberikan error absolut
   - PSNR memberikan rasio signal-to-noise dalam skala logaritmik
   - Keduanya harus dianalisis bersama untuk evaluasi menyeluruh

2. **Tidak ada perbedaan signifikan RGB vs Grayscale**
   - Metode filtering bekerja konsisten di kedua mode
   - Hasil MSE dan PSNR hampir identik

3. **Peningkatan intensitas noise menurunkan kualitas semua filter**
   - Namun Median Filter menunjukkan degradasi paling lambat
   - Robustness-nya superior terutama pada Salt & Pepper

4. **Trade-off Detail vs Noise Reduction**
   - Kernel 3x3: Lebih preserve detail
   - Kernel 5x5: Lebih agresif reduksi noise
   - Pilih berdasarkan prioritas aplikasi

## 🔬 Metodologi Evaluasi

- **Total Images**: 2 citra (portrait + landscape)
- **Noise Types**: 2 (Gaussian + Salt & Pepper)
- **Intensitas**: 2 level (15% + 30%)
- **Color Modes**: 2 (RGB + Grayscale)
- **Filters**: 4 (Mean, Median, Max, Min)
- **Kernel Sizes**: 2 (3x3 + 5x5)
- **Total Kombinasi**: 128 hasil filtering
- **Metrik**: MSE + PSNR

---

**Generated by**: Script `7_tabel_mse_psnr_gabungan.py`  
**Output**: `hasil_evaluasi/tabel_mse_psnr_gabungan.png`  
**Data Source**: `hasil_evaluasi/evaluasi_mse_psnr.json`
