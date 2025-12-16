# 📊 PENJELASAN GRAFIK PERBANDINGAN FILTER

## Gambaran Umum

Grafik perbandingan filter ini menampilkan efektivitas dari **4 jenis filter** yang berbeda dalam mengurangi noise pada citra digital. Evaluasi dilakukan menggunakan metrik **MSE (Mean Squared Error)**, di mana **nilai MSE yang lebih rendah menunjukkan hasil filtering yang lebih baik**.

---

## 🎯 Grafik yang Dihasilkan

### 1. **grafik_perbandingan_gaussian.png**
Grafik khusus untuk **Gaussian Noise** dengan style visual yang menarik:
- ✅ Border ungu di tepi grafik
- ✅ Label "Terbaik" dengan kotak hijau dan panah pada filter dengan MSE terendah
- ✅ Formula MSE ditampilkan di bagian bawah
- ✅ Nilai MSE ditampilkan di atas setiap bar
- ✅ Warna berbeda untuk setiap filter (Merah, Orange, Hijau, Biru)

### 2. **grafik_perbandingan_saltpepper.png**
Grafik khusus untuk **Salt & Pepper Noise** dengan style yang sama

### 3. **grafik_perbandingan_mse.png**
Grafik gabungan yang menampilkan perbandingan kedua jenis noise secara bersamaan

---

## 📋 Kategori Citra yang Dianalisis

Grafik membandingkan efektivitas filter pada **4 kategori citra**:

1. **Landscape RGB** - Citra pemandangan berwarna (RGB)
2. **Portrait RGB** - Citra potret berwarna (RGB)  
3. **Landscape Gray** - Citra pemandangan grayscale
4. **Portrait Gray** - Citra potret grayscale

---

## 🔧 Filter yang Dibandingkan

### 1. **Mean Filter** (Merah)
- Filter rata-rata yang mengganti nilai pixel dengan rata-rata nilai pixel di sekitarnya
- Efektif untuk Gaussian noise pada landscape
- MSE: 334-336 (Landscape), 121-122 (Portrait) untuk Gaussian

### 2. **Median Filter** (Orange)
- Filter yang mengganti nilai pixel dengan nilai median dari pixel di sekitarnya
- **SANGAT EFEKTIF** untuk Salt & Pepper noise
- **TERBAIK** untuk Portrait pada Gaussian noise
- MSE: 42-80 (Portrait), 307-308 (Landscape) untuk Salt & Pepper

### 3. **Max Filter** (Hijau)
- Filter yang mengganti nilai pixel dengan nilai maksimum di sekitarnya
- Kurang efektif untuk semua jenis noise
- MSE tinggi: 2108-23184

### 4. **Min Filter** (Biru)
- Filter yang mengganti nilai pixel dengan nilai minimum di sekitarnya
- Kurang efektif untuk semua jenis noise
- MSE tinggi: 1067-11297

---

## 📈 Hasil Analisis

### **Untuk Gaussian Noise:**

| Kategori | Filter Terbaik | Nilai MSE |
|----------|---------------|-----------|
| Landscape RGB | **Mean** | 336.92 |
| Portrait RGB | **Median** | 80.63 |
| Landscape Gray | **Mean** | 334.51 |
| Portrait Gray | **Median** | 80.13 |

**Kesimpulan:**
- **Mean Filter dominan** pada citra Landscape
- **Median Filter dominan** pada citra Portrait
- Citra Portrait memiliki MSE lebih rendah dibanding Landscape

### **Untuk Salt & Pepper Noise:**

| Kategori | Filter Terbaik | Nilai MSE |
|----------|---------------|-----------|
| Landscape RGB | **Median** | 308.10 |
| Portrait RGB | **Median** | 43.77 |
| Landscape Gray | **Median** | 307.50 |
| Portrait Gray | **Median** | 42.36 |

**Kesimpulan:**
- **Median Filter DOMINAN** untuk semua kategori
- Portrait Gray memiliki hasil TERBAIK (MSE = 42.36)
- Max dan Min filter sangat tidak efektif (MSE > 4000)

---

## 🎨 Fitur Visual Grafik

### Elemen Desain:
1. **Border Ungu** - Frame artistik di tepi grafik
2. **Kotak Hijau "Terbaik"** - Highlight filter dengan MSE terendah
3. **Panah Penunjuk** - Menunjuk ke bar filter terbaik
4. **Formula MSE** - Ditampilkan di bagian bawah
5. **Icon Dekoratif** - Emoji di pojok kanan dan kiri atas
6. **Nilai di Atas Bar** - Menampilkan nilai MSE yang tepat
7. **Grid Background** - Garis bantu horizontal untuk kemudahan membaca

---

## 📊 Interpretasi MSE

### Nilai MSE dan Kualitas:

- **MSE < 100**: Kualitas SANGAT BAIK ⭐⭐⭐⭐⭐
- **MSE 100-500**: Kualitas BAIK ⭐⭐⭐⭐
- **MSE 500-1000**: Kualitas CUKUP ⭐⭐⭐
- **MSE 1000-5000**: Kualitas KURANG ⭐⭐
- **MSE > 5000**: Kualitas BURUK ⭐

### Contoh dari Data:
- **Portrait Gray + Median + S&P**: MSE = 42.36 → Kualitas SANGAT BAIK ⭐⭐⭐⭐⭐
- **Landscape RGB + Mean + Gaussian**: MSE = 336.92 → Kualitas BAIK ⭐⭐⭐⭐
- **Portrait RGB + Max + S&P**: MSE = 23112.41 → Kualitas BURUK ⭐

---

## 💡 Rekomendasi Penggunaan

### Untuk Gaussian Noise:
```
✅ Gunakan Mean Filter untuk Landscape (RGB/Gray)
✅ Gunakan Median Filter untuk Portrait (RGB/Gray)
❌ Hindari Max dan Min Filter
```

### Untuk Salt & Pepper Noise:
```
✅ SELALU gunakan Median Filter (untuk semua jenis citra)
❌ JANGAN gunakan Max atau Min Filter
⚠️  Mean Filter boleh, tapi Median jauh lebih baik
```

---

## 🔬 Formula MSE

Formula yang digunakan untuk menghitung MSE:

$$MSE = \frac{1}{MN} \sum_{i=1}^{M} \sum_{j=1}^{N} (f(i,j) - \hat{f}(i,j))^2$$

Dimana:
- $M \times N$ = Dimensi citra
- $f(i,j)$ = Nilai pixel citra asli pada posisi (i,j)
- $\hat{f}(i,j)$ = Nilai pixel citra hasil filtering pada posisi (i,j)

MSE mengukur rata-rata kuadrat perbedaan antara citra asli dan citra hasil filtering.

---

## 📁 Lokasi File

Semua grafik dan tabel disimpan di folder:
```
hasil_evaluasi/
├── grafik_perbandingan_gaussian.png      (Grafik khusus Gaussian - Style premium)
├── grafik_perbandingan_saltpepper.png    (Grafik khusus Salt & Pepper - Style premium)
├── grafik_perbandingan_mse.png          (Grafik gabungan kedua noise)
├── tabel_gaussian.png                   (Tabel heatmap Gaussian dengan highlight)
├── tabel_saltpepper.png                 (Tabel heatmap Salt & Pepper dengan highlight)
└── tabel_perbandingan_mse.png           (Tabel gabungan side-by-side)
```

### 🎨 Fitur Tabel Visual:
1. **Heatmap dengan Gradient Warna** - Hijau (baik) ke Merah (buruk)
2. **Kotak Hijau "TERBAIK"** - Highlight otomatis pada nilai MSE terendah
3. **Color-coded Values** - Merah untuk nilai >1000, Orange untuk >500, Hitam untuk nilai bagus
4. **Grid Lines** - Pemisah antar sel yang jelas
5. **Colorbar** - Skala warna dengan log scale
6. **Border Ungu** - Frame artistik seperti pada grafik
7. **Interpretasi Kualitas** - Legend di bagian bawah tabel

---

## 🚀 Cara Regenerasi Grafik dan Tabel

Untuk membuat ulang semua visualisasi:

```bash
python 5_visualisasi_mse.py
```

Script akan otomatis:
1. ✅ Membaca data dari `evaluasi_mse_psnr.json`
2. ✅ Mengelompokkan data berdasarkan noise type, filter, dan kategori
3. ✅ Membuat **3 grafik perbandingan** dengan style visual premium
4. ✅ Membuat **3 tabel heatmap** dengan highlight otomatis
5. ✅ Menyimpan semua hasil ke folder `hasil_evaluasi/`

### Output yang Dihasilkan:
- **6 file visualisasi** (3 grafik + 3 tabel)
- **Format PNG berkualitas tinggi** (300 DPI)
- **Siap untuk presentasi dan laporan**

---

## 📌 Catatan Penting

1. **Median Filter adalah juara untuk Salt & Pepper Noise** - Tidak ada kompromi!
2. **Mean Filter bagus untuk Gaussian Noise** - Terutama pada landscape
3. **Portrait citra lebih mudah di-filter** - MSE lebih rendah dibanding landscape
4. **Max dan Min filter tidak direkomendasikan** - Menghasilkan MSE sangat tinggi
5. **Mode warna (RGB vs Gray) tidak signifikan mempengaruhi hasil** - Perbedaan kecil

---

**Dibuat oleh:** Kelompok 10 - Pengolahan Citra Digital  
**Tanggal:** Desember 2025  
**Tools:** Python, Matplotlib, NumPy, Pandas
