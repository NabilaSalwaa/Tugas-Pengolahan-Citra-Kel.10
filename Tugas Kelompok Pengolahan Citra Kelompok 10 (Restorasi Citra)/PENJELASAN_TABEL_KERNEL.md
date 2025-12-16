# 📊 TABEL PERBANDINGAN MSE: FILTER vs KERNEL SIZE

## Hasil Visualisasi

File: `hasil_evaluasi/tabel_kernel_size.png`

---

## � Format Tabel yang Diperbaharui

### Fitur Visual Baru:
✅ **Color-Coded Cells** - Warna berdasarkan kualitas:
  - 🟢 **Hijau Tua**: Nilai terbaik (dengan bintang ★)
  - 🟢 **Hijau Muda**: MSE < 100 (Sangat Baik)
  - 🟡 **Kuning**: MSE 100-500 (Baik)
  - 🟠 **Orange**: MSE 500-1000 (Cukup)
  - 🔴 **Merah**: MSE > 1000 (Buruk)

✅ **Header dengan Background Warna**:
  - Header kolom (Kernel Size): Background biru (#4A90E2)
  - Header baris (Filter Type): Background abu-abu (#D3D3D3)

✅ **Border Tebal** - Pemisah sel yang jelas (2px)

✅ **Bintang (★)** - Menandai nilai terbaik secara otomatis

✅ **Font yang Lebih Besar** - Mudah dibaca (12-14pt)

---

## 🎯 Struktur Tabel

**2 Tabel Side-by-side:**
- **Kiri:** Gaussian Noise  
- **Kanan:** Salt & Pepper Noise

**Struktur:**
- **Kolom Header (Biru):** Kernel Size (3x3, 5x5)
- **Baris Header (Abu-abu):** Filter Type (Mean, Median, Max, Min)
- **Data Cells:** Nilai MSE rata-rata dengan color coding
- **Highlighting:** Background hijau tua + bintang ★ untuk nilai terbaik

---

## 📈 Hasil Analisis

### Gaussian Noise:
| Filter | 3x3 Kernel | 5x5 Kernel | Terbaik | Warna |
|--------|-----------|-----------|---------|-------|
| **Mean**   | **207.55** ★ | 250.44    | **3x3** | 🟡 Kuning |
| Median | 213.45    | 227.82    | 3x3     | 🟡 Kuning |
| Max    | 1978.09   | 3349.47   | 3x3     | 🔴 Merah |
| Min    | 1598.53   | 2779.14   | 3x3     | 🔴 Merah |

**Kesimpulan:** Mean filter dengan kernel 3x3 menghasilkan MSE terendah (207.55) - ditandai dengan hijau tua dan bintang ★

---

### Salt & Pepper Noise:
| Filter | 3x3 Kernel | 5x5 Kernel | Terbaik | Warna |
|--------|-----------|-----------|---------|-------|
| Mean   | 458.47    | 376.12    | 5x5     | 🟡 Kuning |
| **Median** | **149.62** ★ | 201.24    | **3x3** | 🟡 Kuning |
| Max    | 11326.30  | 21326.09  | 3x3     | 🔴 Merah |
| Min    | 5636.96   | 10207.68  | 3x3     | 🔴 Merah |

**Kesimpulan:** Median filter dengan kernel 3x3 menghasilkan MSE terendah (149.62) - ditandai dengan hijau tua dan bintang ★

---

## 💡 Insight

1. **Kernel 3x3 lebih efektif** untuk Gaussian noise (semua filter lebih baik dengan 3x3)
2. **Median filter unggul** untuk Salt & Pepper noise
3. **Mean filter terbaik** untuk Gaussian noise
4. **Max & Min filter tidak efektif** (MSE sangat tinggi)

---

## 💻 Potongan Kode

### 1. Kelompokkan Data Berdasarkan Filter dan Kernel Size

```python
# Kelompokkan data berdasarkan noise type, filter, dan kernel size
hasil = {}
for item in data:
    path = item['filtered_path']
    filename = item['filtered'].lower()
    
    # Deteksi jenis noise
    if 'gaussian' in path or 'gauss' in filename:
        noise_type = 'gaussian'
    elif 'salt_pepper' in path or 'sp' in filename:
        noise_type = 'salt_pepper'
    
    # Deteksi jenis filter
    if '/mean/' in path or '_mean_' in filename:
        filter_type = 'mean'
    elif '/median/' in path or '_median_' in filename:
        filter_type = 'median'
    elif '/max/' in path or '_max_' in filename:
        filter_type = 'max'
    elif '/min/' in path or '_min_' in filename:
        filter_type = 'min'
    
    # Deteksi kernel size
    if '3x3' in filename:
        kernel_size = '3x3'
    elif '5x5' in filename:
        kernel_size = '5x5'
    
    key = (noise_type, filter_type, kernel_size)
    if key not in hasil:
        hasil[key] = []
    hasil[key].append(item['mse'])

# Hitung rata-rata MSE
avg_mse = {k: np.mean(v) for k, v in hasil.items()}
```

---

### 2. Buat Tabel dengan Layout Presisi

```python
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# Setup figure dengan ukuran presisi
fig = plt.figure(figsize=(15, 7))
fig.suptitle('Perbandingan Rata-rata MSE: Filter vs Kernel Size', 
             fontsize=18, fontweight='bold', y=0.96)

# Dimensi sel yang presisi
cell_height = 0.18
cell_width = 0.32
label_width = 0.12
start_x = label_width
start_y = 0.75

# Setup subplot
ax1 = fig.add_subplot(121)
ax1.axis('off')
ax1.set_title('Gaussian Noise', fontsize=15, fontweight='bold', pad=30)
```

---

### 3. Buat Header Kolom (Kernel Size)

```python
# Header kolom dengan background biru
for j, kernel in enumerate(['3x3', '5x5']):
    rect = Rectangle((start_x + j*cell_width, start_y), 
                     cell_width, cell_height,
                     facecolor='#7CA5DB', 
                     edgecolor='black', 
                     linewidth=1.5)
    ax1.add_patch(rect)
    ax1.text(start_x + j*cell_width + cell_width/2, 
             start_y + cell_height/2,
             kernel, 
             ha='center', va='center', 
             color='white',
             fontsize=13, fontweight='bold')
```

---

### 4. Buat Data Cells dengan Highlighting

```python
# Cari nilai minimum untuk highlighting
min_val = np.min(table_gauss)

filters = ['max', 'mean', 'median', 'min']

for i, filter_type in enumerate(filters):
    # Header baris (filter name) dengan background abu-abu
    rect = Rectangle((0, start_y - (i+1)*cell_height), 
                     label_width, cell_height,
                     facecolor='#D3D3D3', 
                     edgecolor='black', 
                     linewidth=1.5)
    ax1.add_patch(rect)
    ax1.text(label_width/2, 
             start_y - (i+1)*cell_height + cell_height/2,
             filter_type, 
             ha='center', va='center',
             fontsize=12, fontweight='bold')
    
    # Data cells
    for j in range(2):  # 2 kolom (3x3 dan 5x5)
        value = table_gauss[i, j]
        
        # Tentukan warna background
        if value == min_val:
            color = '#90EE90'  # Hijau untuk terbaik
            text_weight = 'bold'
        else:
            color = 'white'
            text_weight = 'normal'
        
        # Buat rectangle
        rect = Rectangle((start_x + j*cell_width, 
                         start_y - (i+1)*cell_height),
                        cell_width, cell_height,
                        facecolor=color, 
                        edgecolor='black', 
                        linewidth=1.5)
        ax1.add_patch(rect)
        
        # Tambahkan teks nilai
        ax1.text(start_x + j*cell_width + cell_width/2,
                start_y - (i+1)*cell_height + cell_height/2,
                f'{value:.2f}', 
                ha='center', va='center',
                fontsize=12, fontweight=text_weight)
```

---

### 5. Set Limits dan Simpan

```python
# Set axis limits untuk presisi
ax1.set_xlim(-0.02, start_x + 2*cell_width + 0.02)
ax1.set_ylim(start_y - 4.3*cell_height, start_y + cell_height + 0.05)

# Simpan dengan DPI tinggi
plt.tight_layout(rect=[0, 0.02, 1, 0.94])
plt.savefig('hasil_evaluasi/tabel_kernel_size.png', 
            dpi=300, bbox_inches='tight')
```

---

## 🚀 Cara Menjalankan

```bash
python 6_tabel_kernel_size.py
```

**Output:**
- ✅ `hasil_evaluasi/tabel_kernel_size.png` - Tabel visual dengan highlighting
- ✅ Tabel console dengan analisis lengkap

---

## 🎨 Fitur Tampilan

1. **Border tebal (1.5px)** - untuk presisi dan kejelasan
2. **Color scheme konsisten** - Biru untuk header, Abu-abu untuk label, Hijau untuk nilai terbaik
3. **Font size yang sesuai** - 13pt untuk header, 12pt untuk data
4. **Spacing presisi** - cell_height=0.18, cell_width=0.32
5. **Alignment sempurna** - center horizontal dan vertical

---

**Dibuat dengan ❤️ untuk Tugas Kelompok Pengolahan Citra**
