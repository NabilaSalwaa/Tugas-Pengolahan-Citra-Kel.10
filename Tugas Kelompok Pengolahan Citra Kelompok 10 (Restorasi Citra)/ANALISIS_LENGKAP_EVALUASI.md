# ANALISIS LENGKAP HASIL EVALUASI RESTORASI CITRA

## 1. PENDAHULUAN

Penelitian ini mengevaluasi efektivitas empat jenis filter spasial (Mean, Median, Max, dan Min) dalam melakukan restorasi citra yang telah terkontaminasi oleh dua jenis noise berbeda, yaitu Gaussian Noise dan Salt & Pepper Noise. Evaluasi dilakukan menggunakan dua metrik kuantitatif standar dalam pengolahan citra digital: Mean Squared Error (MSE) dan Peak Signal-to-Noise Ratio (PSNR). Semakin rendah nilai MSE dan semakin tinggi nilai PSNR, maka kualitas hasil restorasi semakin baik dan mendekati citra asli.

Dataset yang digunakan mencakup empat kategori citra: Landscape RGB, Portrait RGB, Landscape Grayscale, dan Portrait Grayscale. Setiap citra diuji dengan dua intensitas noise (5% dan 15% untuk Salt & Pepper; σ=15 dan σ=30 untuk Gaussian) serta dua ukuran kernel filter (3x3 dan 5x5). Total terdapat 128 kombinasi pengujian yang memberikan pemahaman komprehensif tentang performa masing-masing filter dalam berbagai kondisi.

---

## 2. ANALISIS RESTORASI GAUSSIAN NOISE

### 2.1 Performa pada Citra Portrait

Hasil evaluasi menunjukkan bahwa **Median Filter** memberikan performa superior untuk citra portrait yang terkontaminasi Gaussian Noise. Pada kategori Portrait RGB, Median Filter mencapai nilai MSE rata-rata sebesar **80,38**, yang merupakan nilai terbaik dibandingkan filter lainnya. Nilai PSNR yang dihasilkan mencapai **31,46 dB** pada kondisi terbaik (noise σ=15 dengan kernel 3x3), menunjukkan kualitas restorasi yang sangat baik. Hal serupa juga terlihat pada Portrait Grayscale dengan MSE rata-rata **80,37** dan PSNR hingga **31,45 dB**.

Mean Filter menempati posisi kedua dengan MSE rata-rata sekitar **122,27** untuk seluruh kategori Portrait (RGB dan Grayscale). Pada kondisi optimal (σ=15, kernel 3x3), Mean Filter mencapai MSE hanya **58,44** dengan PSNR **30,46 dB**. Meskipun tidak sebaik Median Filter, nilai ini masih menunjukkan hasil restorasi yang cukup memuaskan dengan PSNR berkisar antara **25-30 dB**. Performa Mean Filter cenderung konsisten pada berbagai intensitas noise, menjadikannya pilihan alternatif yang reliable.

Sebaliknya, Max dan Min Filter menunjukkan performa yang sangat buruk. Max Filter menghasilkan MSE yang sangat tinggi mencapai **2.114,98** untuk Portrait (rata-rata dari semua kondisi). Pada kondisi terburuk (σ=30, kernel 5x5), MSE Max Filter melonjak hingga **4.011,75** dengan PSNR hanya **12,10 dB**. Min Filter menunjukkan MSE rata-rata **1.068,41** dengan PSNR di kisaran **17-19 dB**. Nilai PSNR kedua filter ini turun drastis hingga di bawah **20 dB**, mengindikasikan hasil restorasi yang jauh dari optimal dan cenderung merusak detail citra.

### 2.2 Performa pada Citra Landscape

Berbeda dengan portrait, pada citra landscape, **Mean Filter** justru menunjukkan performa terbaik. Untuk seluruh kategori Landscape (RGB dan Grayscale), Mean Filter mencapai MSE rata-rata **335,72** dengan PSNR terbaik **23,89 dB** (pada Grayscale σ=15, kernel 3x3). Pada kondisi RGB terbaik, Mean Filter mencapai MSE **266,22** dengan PSNR **23,88 dB**. Karakteristik landscape yang memiliki tekstur dan detail kompleks tampaknya lebih cocok dengan mekanisme smoothing Mean Filter yang melakukan averaging pada seluruh pixel dalam kernel.

Median Filter berada di posisi kedua dengan MSE rata-rata **360,89** untuk seluruh kategori Landscape. Pada kondisi terbaik (RGB σ=15, kernel 3x3), Median Filter mencapai MSE **283,62** dengan PSNR **23,60 dB**. Meskipun sedikit lebih tinggi dari Mean Filter, perbedaannya tidak signifikan dan Median Filter tetap dapat diandalkan untuk restorasi landscape. PSNR yang dihasilkan berkisar antara **22-24 dB**, menunjukkan kualitas yang masih dapat diterima.

Sama seperti pada portrait, Max dan Min Filter gagal memberikan hasil memuaskan pada landscape. Max Filter menghasilkan MSE ekstrem tinggi dengan rata-rata **3.212,58**, dan pada kondisi terburuk (RGB σ=30, kernel 5x5) mencapai **5.191,36** dengan PSNR hanya **10,98 dB**. Min Filter menunjukkan rata-rata MSE **3.309,27**, dengan nilai terburuk mencapai **5.278,87** dan PSNR **10,91 dB**. Nilai PSNR turun drastis hingga **10-16 dB**, mengindikasikan kerusakan signifikan pada citra hasil restorasi.

### 2.3 Analisis Mendalam Gaussian Noise

Perbedaan performa antara portrait dan landscape dapat dijelaskan dari karakteristik konten citra. Citra portrait umumnya memiliki region homogen yang luas (seperti kulit wajah dan background), sehingga Median Filter yang bersifat non-linear dan mengeliminasi outlier sangat efektif menghilangkan noise tanpa mengaburkan detail wajah. Sebaliknya, landscape dengan tekstur kompleks seperti dedaunan, bebatuan, dan detail arsitektur lebih baik ditangani oleh Mean Filter yang melakukan smoothing merata dan mempertahankan transisi gradual.

Gaussian Noise memiliki distribusi probabilitas normal sehingga nilai noise menyebar secara merata di sekitar nilai asli pixel. Mean Filter yang melakukan averaging cocok untuk jenis noise ini karena proses averaging cenderung mengurangi komponen noise acak. Median Filter juga efektif karena mampu mempertahankan edge sambil mengurangi noise, terutama pada region dengan variasi intensitas rendah.

---

## 3. ANALISIS RESTORASI SALT & PEPPER NOISE

### 3.1 Dominasi Mutlak Median Filter

Hasil evaluasi menunjukkan superioritas **Median Filter** yang sangat jelas dalam menangani Salt & Pepper Noise pada semua kategori citra. Untuk Portrait, Median Filter mencapai MSE luar biasa rendah dengan rata-rata **43,06**. Pada kondisi optimal (intensity 5%, kernel 3x3), Median Filter RGB mencapai MSE hanya **23,07** dengan PSNR **34,50 dB**, sementara Grayscale mencapai MSE **22,77** dengan PSNR **34,56 dB**. Bahkan pada intensitas noise 15%, MSE tetap rendah di kisaran **39-42** dengan PSNR mencapai **31,86-32,14 dB**. Nilai-nilai ini jauh melampaui filter lainnya dan menunjukkan kemampuan Median Filter dalam restorasi hampir sempurna.

Pada kategori landscape, Median Filter tetap unggul dengan MSE rata-rata **307,80**. Pada kondisi terbaik (intensity 5%, kernel 3x3), MSE berkisar **250,55-250,76** dengan PSNR **24,14 dB**. Bahkan dengan intensitas noise 15%, MSE hanya naik menjadi **283-284** dengan PSNR **23,59-23,61 dB**, menunjukkan kualitas restorasi yang sangat baik. Keunggulan Median Filter sangat mencolok ketika dibandingkan dengan filter lainnya – selisih MSE-nya mencapai ratusan hingga ribuan poin.

### 3.2 Performa Filter Lainnya

Mean Filter menempati posisi kedua dengan hasil yang cukup baik namun masih jauh tertinggal dari Median Filter. Untuk Portrait, Mean Filter menghasilkan MSE rata-rata **362,94**. Pada kondisi terbaik (intensity 5%, kernel 5x5), MSE berkisar **150,64-150,92** dengan PSNR **26,34-26,35 dB**. Namun pada intensitas 15% dengan kernel 3x3, MSE melonjak menjadi **657-658** dengan PSNR turun ke **19,94-19,95 dB**. Pada Landscape, MSE Mean Filter rata-rata adalah **471,65**, dengan rentang **351-636** tergantung kondisi. Meskipun demikian, nilai PSNR Mean Filter masih berada di rentang **20-26 dB**, menunjukkan bahwa hasil restorasi masih dapat diterima untuk aplikasi tertentu yang tidak membutuhkan kualitas tinggi.

Max dan Min Filter sekali lagi menunjukkan performa yang sangat buruk, bahkan lebih buruk dibandingkan kasus Gaussian Noise. Max Filter menghasilkan MSE yang sangat tinggi dengan rata-rata **23.148,60** untuk Portrait. Pada kondisi terburuk (intensity 15%, kernel 5x5), MSE mencapai **38.928-39.030** dengan PSNR hanya **2,22-2,23 dB**. Untuk Landscape, rata-rata MSE Max Filter adalah **9.503,79**. Min Filter menunjukkan MSE rata-rata **4.663,63** untuk Portrait dan **11.181,01** untuk Landscape. PSNR turun drastis hingga **2-11 dB**, menunjukkan bahwa citra hasil filter hampir tidak dapat dikenali dan mengalami degradasi masif.

### 3.3 Mengapa Median Filter Sangat Efektif?

Superioritas Median Filter pada Salt & Pepper Noise dapat dijelaskan dari karakteristik noise itu sendiri. Salt & Pepper Noise adalah impulse noise yang mengubah pixel menjadi nilai ekstrem (0 untuk "pepper"/hitam atau 255 untuk "salt"/putih) tanpa mempengaruhi pixel di sekitarnya. Median Filter bekerja dengan mengurutkan nilai pixel dalam kernel dan memilih nilai tengah, sehingga pixel noise ekstrem otomatis diabaikan.

Misalnya, dalam kernel 3x3 dengan satu pixel noise (nilai 255) di tengah area gelap (nilai ~50), Median Filter akan memilih nilai sekitar 50 dan mengabaikan 255. Sebaliknya, Mean Filter akan melakukan averaging sehingga hasilnya akan terpengaruh oleh nilai ekstrem tersebut, menghasilkan nilai yang tidak natural (misalnya ~70-80) yang menyebabkan blurring dan artefak visual.

Max dan Min Filter gagal total karena justru memperkuat efek noise. Max Filter akan memilih nilai maksimum dalam kernel, sehingga "salt" noise (nilai 255) akan menyebar ke area sekitarnya. Min Filter melakukan hal sebaliknya dengan menyebarkan "pepper" noise (nilai 0). Ini menyebabkan ekspansi area noise dan kerusakan signifikan pada struktur citra.

---

## 4. PERBANDINGAN UKURAN KERNEL (3x3 vs 5x5)

Analisis terhadap pengaruh ukuran kernel menunjukkan pola yang konsisten di seluruh jenis filter dan noise. Kernel **3x3** secara umum memberikan hasil lebih baik dibandingkan kernel **5x5**, dibuktikan dengan nilai MSE yang lebih rendah dan PSNR yang lebih tinggi. Sebagai contoh, pada Median Filter untuk Portrait dengan Salt & Pepper Noise intensity 5%, kernel 3x3 menghasilkan MSE **23,07** dengan PSNR **34,50 dB**, sedangkan kernel 5x5 menghasilkan MSE **52,09** dengan PSNR **30,96 dB** – perbedaan yang sangat signifikan.

Perbedaan ini disebabkan oleh trade-off antara noise reduction dan preservation of details. Kernel 3x3 hanya melibatkan 9 pixel dalam perhitungan, sehingga dapat mengurangi noise dengan tetap mempertahankan detail halus dan edge pada citra. Kernel 5x5 yang melibatkan 25 pixel cenderung menghasilkan over-smoothing, di mana detail penting seperti tekstur dan edge menjadi kabur.

Namun, dalam beberapa kasus dengan intensitas noise sangat tinggi (15% untuk Salt & Pepper atau σ=30 untuk Gaussian), kernel 5x5 kadang memberikan hasil yang lebih baik karena mampu mengcover area noise yang lebih luas. Tetapi secara keseluruhan, **kernel 3x3 adalah pilihan optimal** untuk sebagian besar aplikasi restorasi citra karena menghasilkan keseimbangan terbaik antara noise reduction dan detail preservation.

---

## 5. PERBANDINGAN RGB vs GRAYSCALE

Perbandingan antara citra RGB dan Grayscale menunjukkan bahwa tidak ada perbedaan signifikan dalam nilai MSE dan PSNR. Sebagai contoh, pada Median Filter untuk Portrait dengan Gaussian Noise σ=15 kernel 3x3, Portrait RGB menghasilkan MSE **46,47** dengan PSNR **31,46 dB**, sedangkan Portrait Grayscale menghasilkan MSE **46,54** dengan PSNR **31,45 dB** – perbedaannya kurang dari 0,2%, yang secara praktis tidak signifikan.

Hal ini menunjukkan bahwa metode filtering yang digunakan (menerapkan filter secara independen pada setiap channel atau pada grayscale) memiliki efektivitas yang setara. Dalam implementasi praktis, pemilihan antara RGB dan Grayscale lebih ditentukan oleh kebutuhan aplikasi: jika informasi warna penting (seperti untuk fotografi atau medical imaging berwarna), maka RGB lebih dipilih; jika hanya struktur dan intensitas yang penting, Grayscale lebih efisien secara komputasi.

---

## 6. ANALISIS INTENSITAS NOISE

Evaluasi menunjukkan bahwa peningkatan intensitas noise secara konsisten meningkatkan nilai MSE dan menurunkan PSNR, sesuai ekspektasi. Untuk Gaussian Noise pada Portrait, peningkatan dari σ=15 ke σ=30 menyebabkan Median Filter (kernel 3x3) meningkat dari MSE **46,47** menjadi **122,83** (164% increase), sementara Mean Filter meningkat dari **58,44** menjadi **166,37** (185% increase). Pada Salt & Pepper Noise, peningkatan dari 5% ke 15% lebih dramatis: Median Filter naik dari MSE **23,07** menjadi **42,36** (84% increase), sementara Mean Filter melonjak dari **202,41** menjadi **658,65** (225% increase).

Namun, Median Filter menunjukkan **robustness yang superior** terhadap peningkatan intensitas noise, terutama pada Salt & Pepper. Sementara filter lain mengalami degradasi performa yang tajam, Median Filter tetap mempertahankan nilai MSE yang relatif rendah. Sebagai contoh, pada Portrait dengan Salt & Pepper 15% kernel 3x3, Median Filter RGB masih menghasilkan MSE hanya **42,36** dengan PSNR **31,86 dB**, sedangkan Mean Filter melonjak ke **658,65** dengan PSNR **19,94 dB**, dan Max Filter mencapai **22.366,53** dengan PSNR **4,63 dB** – perbedaan lebih dari 500 kali lipat!

---

## 7. TEMUAN PENTING DAN INSIGHTS

### 7.1 Karakteristik Filter

**Median Filter:**
- **Terbaik untuk Salt & Pepper Noise** pada semua kondisi (MSE 23-284, PSNR 24-35 dB)
- **Terbaik untuk Gaussian Noise pada Portrait** (MSE rata-rata 80,38, PSNR hingga 31,46 dB)
- **Non-linear dan robust** terhadap outlier dan peningkatan intensitas noise
- Mempertahankan edge dengan baik tanpa over-smoothing
- Dapat menghilangkan impulse noise hampir sempurna dengan kernel 3x3

**Mean Filter:**
- **Terbaik untuk Gaussian Noise pada Landscape** (MSE rata-rata 335,72, PSNR hingga 23,89 dB)
- Performa konsisten pada berbagai intensitas noise (MSE 58-658 tergantung kondisi)
- **Linear dan komputasi efisien** dibanding Median Filter
- Cocok untuk smooth regions dengan tekstur kompleks seperti landscape
- Trade-off: slight blurring untuk noise reduction, kurang efektif untuk Salt & Pepper

**Max dan Min Filter:**
- **Tidak efektif untuk noise reduction** pada semua kondisi
- Cenderung merusak citra lebih lanjut dengan menyebarkan noise
- MSE sangat tinggi: Gaussian (1.068-5.278), Salt & Pepper (4.663-39.030)
- PSNR sangat rendah: Gaussian (11-19 dB), Salt & Pepper (2-11 dB)
- Max Filter terburuk pada Salt & Pepper (MSE hingga 39.030, PSNR 2,22 dB)
- Hanya cocok untuk aplikasi khusus (morphological operations, bukan denoising)

### 7.2 Rekomendasi Praktis

**Untuk Salt & Pepper Noise:**
- **Gunakan Median Filter dengan kernel 3x3** (wajib, no alternative)
- Hasil optimal pada semua jenis citra dan intensitas
- MSE rendah: 23-284 (intensity 5% hingga 15%, kernel 3x3)
- PSNR tinggi: 24-35 dB
- Pada intensity 5%, Portrait: MSE 23, PSNR 34,50 dB (hampir sempurna)

**Untuk Gaussian Noise:**
- **Portrait**: Median Filter (MSE rata-rata 80,38, PSNR hingga 31,46 dB)
  - Optimal: σ=15, kernel 3x3 → MSE 46,47, PSNR 31,46 dB
- **Landscape**: Mean Filter (MSE rata-rata 335,72, PSNR hingga 23,89 dB)
  - Optimal: σ=15, kernel 3x3 → MSE 265,69, PSNR 23,89 dB
- Kernel 3x3 lebih direkomendasikan (7-8% lebih baik dari 5x5)

**Pertimbangan Tambahan:**
- Jika kecepatan komputasi kritis: Mean Filter (linear, lebih cepat)
- Jika kualitas mutlak diperlukan: Median Filter (hasil lebih baik, sedikit lebih lambat)
- Jika noise intensity tidak diketahui: Median Filter (lebih robust)
- Hindari Max dan Min Filter untuk denoising

---

## 8. KESIMPULAN

Berdasarkan evaluasi komprehensif terhadap 128 kombinasi pengujian yang melibatkan empat jenis filter, dua jenis noise, empat kategori citra, berbagai intensitas noise, dan dua ukuran kernel, dapat disimpulkan bahwa **Median Filter adalah pilihan terbaik untuk restorasi citra secara keseluruhan**.

Median Filter menunjukkan performa superior pada Salt & Pepper Noise dengan MSE yang sangat rendah (23,07 untuk intensity 5% hingga 284,72 untuk intensity 15% pada landscape) dan PSNR tinggi (24-35 dB) yang mengindikasikan restorasi hampir sempurna. Pada kondisi optimal Portrait intensity 5%, Median Filter mencapai MSE hanya **23,07** dengan PSNR **34,50 dB**. Pada Gaussian Noise, Median Filter juga unggul untuk citra portrait dengan MSE rata-rata **80,38** dan PSNR hingga **31,46 dB**, meskipun Mean Filter sedikit lebih baik untuk landscape (MSE **335,72** vs **360,89**).

Mean Filter merupakan alternatif yang baik dengan performa konsisten dan efisiensi komputasi tinggi, terutama untuk aplikasi real-time atau ketika slight blurring dapat diterima. Pada Gaussian Noise landscape, Mean Filter unggul dengan MSE **335,72** dibanding Median **360,89**. Sebaliknya, Max dan Min Filter terbukti tidak efektif untuk noise reduction. Untuk Gaussian Noise, MSE berkisar **1.068-5.278** dengan PSNR **11-19 dB**. Untuk Salt & Pepper, performanya lebih buruk lagi dengan MSE **4.663-39.030** dan PSNR **2-11 dB**, menunjukkan kerusakan citra yang sangat parah.

**Rekomendasi Akhir:**
- **Aplikasi Umum**: Median Filter dengan kernel 3x3
- **Real-time Processing**: Mean Filter dengan kernel 3x3
- **Gaussian Noise pada Landscape**: Mean Filter
- **Salt & Pepper Noise (semua kasus)**: Median Filter
- **Hindari**: Max dan Min Filter untuk denoising

Pemilihan kernel 3x3 direkomendasikan karena menghasilkan keseimbangan optimal antara noise reduction dan detail preservation. Perbedaan antara RGB dan Grayscale tidak signifikan, sehingga pemilihannya dapat disesuaikan dengan kebutuhan aplikasi spesifik.

Hasil penelitian ini memberikan panduan praktis yang jelas bagi praktisi pengolahan citra digital dalam memilih metode filtering yang tepat berdasarkan jenis noise, karakteristik citra, dan requirement kualitas output.

---

**Catatan:** Analisis ini didasarkan pada data evaluasi kuantitatif lengkap dengan total 128 pengujian yang tersimpan dalam file `evaluasi_mse_psnr.json` dan `evaluasi_lengkap.txt`.
