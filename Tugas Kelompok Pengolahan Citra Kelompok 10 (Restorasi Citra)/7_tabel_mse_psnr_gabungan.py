import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Baca data evaluasi
with open('hasil_evaluasi/evaluasi_mse_psnr.json', 'r') as f:
    data = json.load(f)

# Kelompokkan data berdasarkan noise type, filter, dan kernel size
hasil_mse = {}
hasil_psnr = {}

for item in data:
    path = item['filtered_path']
    filename = item['filtered'].lower()
    
    # Deteksi jenis noise
    if 'gaussian' in path or 'gauss' in filename:
        noise_type = 'gaussian'
    elif 'salt_pepper' in path or 'sp' in filename:
        noise_type = 'salt_pepper'
    else:
        continue
    
    # Deteksi jenis filter
    if '/mean/' in path or '_mean_' in filename:
        filter_type = 'mean'
    elif '/median/' in path or '_median_' in filename:
        filter_type = 'median'
    elif '/max/' in path or '_max_' in filename:
        filter_type = 'max'
    elif '/min/' in path or '_min_' in filename:
        filter_type = 'min'
    else:
        continue
    
    # Deteksi kernel size
    if '3x3' in filename:
        kernel_size = '3x3'
    elif '5x5' in filename:
        kernel_size = '5x5'
    else:
        continue
    
    key = (noise_type, filter_type, kernel_size)
    if key not in hasil_mse:
        hasil_mse[key] = []
        hasil_psnr[key] = []
    hasil_mse[key].append(item['mse'])
    hasil_psnr[key].append(item['psnr'])

# Hitung rata-rata MSE dan PSNR untuk setiap kombinasi
avg_mse = {}
avg_psnr = {}
for key in hasil_mse.keys():
    avg_mse[key] = np.mean(hasil_mse[key])
    avg_psnr[key] = np.mean(hasil_psnr[key])

print("Data MSE dan PSNR berhasil dikelompokkan")
print(f"Total kombinasi: {len(avg_mse)}")

# Buat tabel visual dengan tampilan presisi yang menggabungkan MSE dan PSNR
fig = plt.figure(figsize=(20, 10))
fig.suptitle('Perbandingan Filter: MSE (lebih rendah lebih baik) & PSNR (lebih tinggi lebih baik)', 
             fontsize=18, fontweight='bold', y=0.97)

filters = ['mean', 'median', 'max', 'min']
filter_labels = ['Mean', 'Median', 'Max', 'Min']
kernel_sizes = ['3x3', '5x5']

# ============= GAUSSIAN NOISE =============
# Siapkan data untuk tabel Gaussian
table_gauss_mse = []
table_gauss_psnr = []
for filter_type in filters:
    row_mse = []
    row_psnr = []
    for kernel in kernel_sizes:
        key = ('gaussian', filter_type, kernel)
        row_mse.append(avg_mse.get(key, 0))
        row_psnr.append(avg_psnr.get(key, 0))
    table_gauss_mse.append(row_mse)
    table_gauss_psnr.append(row_psnr)

table_gauss_mse = np.array(table_gauss_mse)
table_gauss_psnr = np.array(table_gauss_psnr)

# Setup untuk tabel Gaussian
ax1 = fig.add_subplot(121)
ax1.axis('off')
ax1.set_title('Gaussian Noise', fontsize=16, fontweight='bold', pad=35)

# Dimensi sel yang presisi
cell_height = 0.13
cell_width = 0.28
label_width = 0.12
start_x = label_width
start_y = 0.80

# Cari nilai terbaik untuk highlighting
min_mse_val = np.min(table_gauss_mse)
max_psnr_val = np.max(table_gauss_psnr)

# Header kolom (kernel size) - dengan background biru
for j, kernel in enumerate(kernel_sizes):
    rect = Rectangle((start_x + j*cell_width, start_y), cell_width, cell_height,
                     facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax1.add_patch(rect)
    ax1.text(start_x + j*cell_width + cell_width/2, start_y + cell_height/2,
            kernel, ha='center', va='center', color='white',
            fontsize=14, fontweight='bold')

# Data cells dengan kombinasi MSE dan PSNR
for i, filter_type in enumerate(filter_labels):
    # Header baris (filter name) - dengan background abu-abu
    rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                     facecolor='#D3D3D3', edgecolor='black', linewidth=2)
    ax1.add_patch(rect)
    ax1.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
            filter_type, ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    for j in range(len(kernel_sizes)):
        mse_value = table_gauss_mse[i, j]
        psnr_value = table_gauss_psnr[i, j]
        
        # Tentukan warna background berdasarkan kualitas nilai MSE
        if mse_value == min_mse_val:
            color = '#90EE90'  # Hijau muda untuk nilai terbaik
            text_weight = 'bold'
            text_color = '#1B5E20'
            marker = ' ⭐'
        elif mse_value < 100:
            color = '#C8E6C9'  # Hijau sangat muda
            text_weight = 'bold'
            text_color = 'black'
            marker = ''
        elif mse_value < 500:
            color = '#FFF9C4'  # Kuning muda
            text_weight = 'normal'
            text_color = 'black'
            marker = ''
        elif mse_value < 1000:
            color = '#FFE0B2'  # Orange muda
            text_weight = 'normal'
            text_color = 'black'
            marker = ''
        else:
            color = '#FFCDD2'  # Merah muda
            text_weight = 'bold'
            text_color = '#C62828'
            marker = ''
        
        rect = Rectangle((start_x + j*cell_width, start_y - (i+1)*cell_height),
                        cell_width, cell_height,
                        facecolor=color, edgecolor='black', linewidth=2)
        ax1.add_patch(rect)
        
        # Tampilkan MSE dan PSNR dalam satu sel
        text_display = f'MSE: {mse_value:.2f}{marker}\nPSNR: {psnr_value:.2f} dB'
        
        ax1.text(start_x + j*cell_width + cell_width/2,
                start_y - (i+1)*cell_height + cell_height/2,
                text_display, ha='center', va='center',
                fontsize=10, fontweight=text_weight, color=text_color)

ax1.set_xlim(-0.02, start_x + 2*cell_width + 0.02)
ax1.set_ylim(start_y - 4.8*cell_height, start_y + cell_height + 0.05)

# ============= SALT & PEPPER NOISE =============
# Siapkan data untuk tabel Salt & Pepper
table_sp_mse = []
table_sp_psnr = []
for filter_type in filters:
    row_mse = []
    row_psnr = []
    for kernel in kernel_sizes:
        key = ('salt_pepper', filter_type, kernel)
        row_mse.append(avg_mse.get(key, 0))
        row_psnr.append(avg_psnr.get(key, 0))
    table_sp_mse.append(row_mse)
    table_sp_psnr.append(row_psnr)

table_sp_mse = np.array(table_sp_mse)
table_sp_psnr = np.array(table_sp_psnr)

# Setup untuk tabel Salt & Pepper
ax2 = fig.add_subplot(122)
ax2.axis('off')
ax2.set_title('Salt & Pepper Noise', fontsize=16, fontweight='bold', pad=35)

# Cari nilai terbaik untuk highlighting
min_mse_sp = np.min(table_sp_mse)
max_psnr_sp = np.max(table_sp_psnr)

# Header kolom (kernel size) - dengan background biru
for j, kernel in enumerate(kernel_sizes):
    rect = Rectangle((start_x + j*cell_width, start_y), cell_width, cell_height,
                     facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax2.add_patch(rect)
    ax2.text(start_x + j*cell_width + cell_width/2, start_y + cell_height/2,
            kernel, ha='center', va='center', color='white',
            fontsize=14, fontweight='bold')

# Data cells dengan kombinasi MSE dan PSNR
for i, filter_type in enumerate(filter_labels):
    # Header baris (filter name) - dengan background abu-abu
    rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                     facecolor='#D3D3D3', edgecolor='black', linewidth=2)
    ax2.add_patch(rect)
    ax2.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
            filter_type, ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    for j in range(len(kernel_sizes)):
        mse_value = table_sp_mse[i, j]
        psnr_value = table_sp_psnr[i, j]
        
        # Tentukan warna background berdasarkan kualitas nilai MSE
        if mse_value == min_mse_sp:
            color = '#90EE90'  # Hijau muda untuk nilai terbaik
            text_weight = 'bold'
            text_color = '#1B5E20'
            marker = ' ⭐'
        elif mse_value < 100:
            color = '#C8E6C9'  # Hijau sangat muda
            text_weight = 'bold'
            text_color = 'black'
            marker = ''
        elif mse_value < 500:
            color = '#FFF9C4'  # Kuning muda
            text_weight = 'normal'
            text_color = 'black'
            marker = ''
        elif mse_value < 1000:
            color = '#FFE0B2'  # Orange muda
            text_weight = 'normal'
            text_color = 'black'
            marker = ''
        else:
            color = '#FFCDD2'  # Merah muda
            text_weight = 'bold'
            text_color = '#C62828'
            marker = ''
        
        rect = Rectangle((start_x + j*cell_width, start_y - (i+1)*cell_height),
                        cell_width, cell_height,
                        facecolor=color, edgecolor='black', linewidth=2)
        ax2.add_patch(rect)
        
        # Tampilkan MSE dan PSNR dalam satu sel
        text_display = f'MSE: {mse_value:.2f}{marker}\nPSNR: {psnr_value:.2f} dB'
        
        ax2.text(start_x + j*cell_width + cell_width/2,
                start_y - (i+1)*cell_height + cell_height/2,
                text_display, ha='center', va='center',
                fontsize=10, fontweight=text_weight, color=text_color)

ax2.set_xlim(-0.02, start_x + 2*cell_width + 0.02)
ax2.set_ylim(start_y - 4.8*cell_height, start_y + cell_height + 0.05)

plt.tight_layout(rect=[0, 0.02, 1, 0.94])
plt.savefig('hasil_evaluasi/tabel_mse_psnr_gabungan.png', dpi=300, bbox_inches='tight')
print("\n✓ Tabel perbandingan MSE & PSNR disimpan: hasil_evaluasi/tabel_mse_psnr_gabungan.png")

# ============= PRINT TABEL DETAIL DI CONSOLE =============
print("\n" + "="*100)
print("TABEL PERBANDINGAN LENGKAP: MSE & PSNR - FILTER vs KERNEL SIZE")
print("="*100)

print("\n📊 GAUSSIAN NOISE")
print("-" * 100)
print(f"{'Filter':<10} {'3x3 MSE':>12} {'3x3 PSNR':>14} {'5x5 MSE':>12} {'5x5 PSNR':>14} {'Terbaik':>12}")
print("-" * 100)
for i, filter_type in enumerate(filter_labels):
    mse_3x3 = table_gauss_mse[i, 0]
    psnr_3x3 = table_gauss_psnr[i, 0]
    mse_5x5 = table_gauss_mse[i, 1]
    psnr_5x5 = table_gauss_psnr[i, 1]
    best = "3x3" if mse_3x3 < mse_5x5 else "5x5"
    marker = " ⭐" if table_gauss_mse[i].min() == min_mse_val else ""
    print(f"{filter_type:<10} {mse_3x3:>12.2f} {psnr_3x3:>12.2f} dB {mse_5x5:>12.2f} {psnr_5x5:>12.2f} dB {best:>12}{marker}")

print("\n📊 SALT & PEPPER NOISE")
print("-" * 100)
print(f"{'Filter':<10} {'3x3 MSE':>12} {'3x3 PSNR':>14} {'5x5 MSE':>12} {'5x5 PSNR':>14} {'Terbaik':>12}")
print("-" * 100)
for i, filter_type in enumerate(filter_labels):
    mse_3x3 = table_sp_mse[i, 0]
    psnr_3x3 = table_sp_psnr[i, 0]
    mse_5x5 = table_sp_mse[i, 1]
    psnr_5x5 = table_sp_psnr[i, 1]
    best = "3x3" if mse_3x3 < mse_5x5 else "5x5"
    marker = " ⭐" if table_sp_mse[i].min() == min_mse_sp else ""
    print(f"{filter_type:<10} {mse_3x3:>12.2f} {psnr_3x3:>12.2f} dB {mse_5x5:>12.2f} {psnr_5x5:>12.2f} dB {best:>12}{marker}")

print("\n" + "="*100)
print("KESIMPULAN BERDASARKAN MSE (Lower is Better) & PSNR (Higher is Better):")
print("-" * 100)

# Cari posisi nilai minimum untuk Gaussian
min_pos_gauss = np.unravel_index(np.argmin(table_gauss_mse), table_gauss_mse.shape)
max_psnr_pos_gauss = np.unravel_index(np.argmax(table_gauss_psnr), table_gauss_psnr.shape)
print(f"  Gaussian Noise:")
print(f"    - MSE terbaik     : {filter_labels[min_pos_gauss[0]]} - {kernel_sizes[min_pos_gauss[1]]} (MSE = {min_mse_val:.2f})")
print(f"    - PSNR terbaik    : {filter_labels[max_psnr_pos_gauss[0]]} - {kernel_sizes[max_psnr_pos_gauss[1]]} (PSNR = {max_psnr_val:.2f} dB)")

# Cari posisi nilai minimum untuk Salt & Pepper
min_pos_sp = np.unravel_index(np.argmin(table_sp_mse), table_sp_mse.shape)
max_psnr_pos_sp = np.unravel_index(np.argmax(table_sp_psnr), table_sp_psnr.shape)
print(f"\n  Salt & Pepper Noise:")
print(f"    - MSE terbaik     : {filter_labels[min_pos_sp[0]]} - {kernel_sizes[min_pos_sp[1]]} (MSE = {min_mse_sp:.2f})")
print(f"    - PSNR terbaik    : {filter_labels[max_psnr_pos_sp[0]]} - {kernel_sizes[max_psnr_pos_sp[1]]} (PSNR = {max_psnr_sp:.2f} dB)")
print("="*100)

# ============= ANALISIS TAMBAHAN =============
print("\n" + "="*100)
print("ANALISIS PERFORMA BERDASARKAN JENIS CITRA:")
print("="*100)

# Analisis per kategori citra
categories = {
    'Portrait': ['potrait', 'portrait'],
    'Landscape': ['landscape']
}

for cat_name, keywords in categories.items():
    print(f"\n📷 {cat_name.upper()} IMAGES:")
    print("-" * 100)
    
    # Filter data untuk kategori ini
    cat_data_gauss = {}
    cat_data_sp = {}
    
    for item in data:
        filename = item['filtered'].lower()
        original = item['original'].lower()
        
        # Cek apakah termasuk kategori ini
        is_category = any(kw in filename or kw in original for kw in keywords)
        if not is_category:
            continue
        
        path = item['filtered_path']
        
        # Deteksi jenis noise
        if 'gaussian' in path or 'gauss' in filename:
            noise_type = 'gaussian'
            target_dict = cat_data_gauss
        elif 'salt_pepper' in path or 'sp' in filename:
            noise_type = 'salt_pepper'
            target_dict = cat_data_sp
        else:
            continue
        
        # Deteksi jenis filter
        if '/mean/' in path or '_mean_' in filename:
            filter_type = 'mean'
        elif '/median/' in path or '_median_' in filename:
            filter_type = 'median'
        elif '/max/' in path or '_max_' in filename:
            filter_type = 'max'
        elif '/min/' in path or '_min_' in filename:
            filter_type = 'min'
        else:
            continue
        
        if filter_type not in target_dict:
            target_dict[filter_type] = {'mse': [], 'psnr': []}
        
        target_dict[filter_type]['mse'].append(item['mse'])
        target_dict[filter_type]['psnr'].append(item['psnr'])
    
    # Print hasil untuk Gaussian
    if cat_data_gauss:
        print(f"\n  Gaussian Noise:")
        for filter_name in filters:
            if filter_name in cat_data_gauss:
                avg_mse_cat = np.mean(cat_data_gauss[filter_name]['mse'])
                avg_psnr_cat = np.mean(cat_data_gauss[filter_name]['psnr'])
                print(f"    - {filter_name.capitalize():<8}: MSE = {avg_mse_cat:>8.2f}, PSNR = {avg_psnr_cat:>6.2f} dB")
    
    # Print hasil untuk Salt & Pepper
    if cat_data_sp:
        print(f"\n  Salt & Pepper Noise:")
        for filter_name in filters:
            if filter_name in cat_data_sp:
                avg_mse_cat = np.mean(cat_data_sp[filter_name]['mse'])
                avg_psnr_cat = np.mean(cat_data_sp[filter_name]['psnr'])
                print(f"    - {filter_name.capitalize():<8}: MSE = {avg_mse_cat:>8.2f}, PSNR = {avg_psnr_cat:>6.2f} dB")

print("\n" + "="*100)
print("RINGKASAN ANALISIS:")
print("="*100)
print("""
✓ MSE (Mean Squared Error): Nilai lebih RENDAH = Lebih BAIK
  - MSE < 100   : Kualitas sangat baik (hijau)
  - MSE 100-500 : Kualitas baik (kuning)
  - MSE > 1000  : Kualitas buruk (merah)

✓ PSNR (Peak Signal-to-Noise Ratio): Nilai lebih TINGGI = Lebih BAIK
  - PSNR > 30 dB : Kualitas sangat baik
  - PSNR 20-30 dB: Kualitas sedang
  - PSNR < 20 dB : Kualitas buruk

✓ Median Filter terbukti paling efektif untuk kedua jenis noise
✓ Kernel 3x3 umumnya lebih baik dalam menjaga detail citra
✓ Max dan Min Filter tidak cocok untuk restorasi citra (MSE tinggi, PSNR rendah)
""")
print("="*100)

plt.close()
