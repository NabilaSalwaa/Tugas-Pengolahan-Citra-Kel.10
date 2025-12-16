import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Baca data evaluasi
with open('hasil_evaluasi/evaluasi_mse_psnr.json', 'r') as f:
    data = json.load(f)

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
    if key not in hasil:
        hasil[key] = []
    hasil[key].append(item['mse'])

# Hitung rata-rata MSE untuk setiap kombinasi
avg_mse = {}
for key, values in hasil.items():
    avg_mse[key] = np.mean(values)

print("Data MSE berhasil dikelompokkan")
print(f"Total kombinasi: {len(avg_mse)}")

# Buat tabel visual dengan tampilan presisi
fig = plt.figure(figsize=(16, 8))
fig.suptitle('Perbandingan Rata-rata MSE: Filter vs Kernel Size untuk Semua Kategori Citra', 
             fontsize=17, fontweight='bold', y=0.97)

filters = ['mean', 'median', 'max', 'min']
filter_labels = ['Mean', 'Median', 'Max', 'Min']
kernel_sizes = ['3x3', '5x5']

# Tabel 1: Gaussian Noise
table_gauss = []
for filter_type in filters:
    row = []
    for kernel in kernel_sizes:
        key = ('gaussian', filter_type, kernel)
        row.append(avg_mse.get(key, 0))
    table_gauss.append(row)

table_gauss = np.array(table_gauss)

# Setup untuk tabel 1
ax1 = fig.add_subplot(121)
ax1.axis('off')
ax1.set_title('Gaussian Noise', fontsize=15, fontweight='bold', pad=30)

# Dimensi sel yang presisi
cell_height = 0.16
cell_width = 0.35
label_width = 0.15
start_x = label_width
start_y = 0.75

# Cari nilai minimum (terbaik) untuk highlighting
min_val = np.min(table_gauss)

# Header kolom (kernel size) - dengan background biru
for j, kernel in enumerate(kernel_sizes):
    rect = Rectangle((start_x + j*cell_width, start_y), cell_width, cell_height,
                     facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax1.add_patch(rect)
    ax1.text(start_x + j*cell_width + cell_width/2, start_y + cell_height/2,
            kernel, ha='center', va='center', color='white',
            fontsize=14, fontweight='bold')

# Data cells dengan border presisi
for i, filter_type in enumerate(filter_labels):
    # Header baris (filter name) - dengan background abu-abu
    rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                     facecolor='#D3D3D3', edgecolor='black', linewidth=2)
    ax1.add_patch(rect)
    ax1.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
            filter_type, ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    for j in range(len(kernel_sizes)):
        value = table_gauss[i, j]
        
        # Tentukan warna background berdasarkan kualitas nilai
        if value == min_val:
            color = '#90EE90'  # Hijau muda untuk nilai terbaik
            text_weight = 'bold'
            text_color = '#1B5E20'
        elif value < 100:
            color = '#C8E6C9'  # Hijau sangat muda
            text_weight = 'bold'
            text_color = 'black'
        elif value < 500:
            color = '#FFF9C4'  # Kuning muda
            text_weight = 'normal'
            text_color = 'black'
        elif value < 1000:
            color = '#FFE0B2'  # Orange muda
            text_weight = 'normal'
            text_color = 'black'
        else:
            color = '#FFCDD2'  # Merah muda
            text_weight = 'bold'
            text_color = '#C62828'
        
        rect = Rectangle((start_x + j*cell_width, start_y - (i+1)*cell_height),
                        cell_width, cell_height,
                        facecolor=color, edgecolor='black', linewidth=2)
        ax1.add_patch(rect)
        
        # Tambahkan bintang untuk nilai terbaik
        if value == min_val:
            text_display = f'{value:.2f} ★'
        else:
            text_display = f'{value:.2f}'
        
        ax1.text(start_x + j*cell_width + cell_width/2,
                start_y - (i+1)*cell_height + cell_height/2,
                text_display, ha='center', va='center',
                fontsize=12, fontweight=text_weight, color=text_color)

ax1.set_xlim(-0.02, start_x + 2*cell_width + 0.02)
ax1.set_ylim(start_y - 4.5*cell_height, start_y + cell_height + 0.05)

# Tabel 2: Salt & Pepper Noise
table_sp = []
for filter_type in filters:
    row = []
    for kernel in kernel_sizes:
        key = ('salt_pepper', filter_type, kernel)
        row.append(avg_mse.get(key, 0))
    table_sp.append(row)

table_sp = np.array(table_sp)

# Setup untuk tabel 2
ax2 = fig.add_subplot(122)
ax2.axis('off')
ax2.set_title('Salt & Pepper Noise', fontsize=15, fontweight='bold', pad=30)

# Cari nilai minimum (terbaik) untuk highlighting
min_val_sp = np.min(table_sp)

# Header kolom (kernel size) - dengan background biru
for j, kernel in enumerate(kernel_sizes):
    rect = Rectangle((start_x + j*cell_width, start_y), cell_width, cell_height,
                     facecolor='#4A90E2', edgecolor='black', linewidth=2)
    ax2.add_patch(rect)
    ax2.text(start_x + j*cell_width + cell_width/2, start_y + cell_height/2,
            kernel, ha='center', va='center', color='white',
            fontsize=14, fontweight='bold')

# Data cells dengan border presisi
for i, filter_type in enumerate(filter_labels):
    # Header baris (filter name) - dengan background abu-abu
    rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                     facecolor='#D3D3D3', edgecolor='black', linewidth=2)
    ax2.add_patch(rect)
    ax2.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
            filter_type, ha='center', va='center',
            fontsize=13, fontweight='bold')
    
    for j in range(len(kernel_sizes)):
        value = table_sp[i, j]
        
        # Tentukan warna background berdasarkan kualitas nilai
        if value == min_val_sp:
            color = '#90EE90'  # Hijau muda untuk nilai terbaik
            text_weight = 'bold'
            text_color = '#1B5E20'
        elif value < 100:
            color = '#C8E6C9'  # Hijau sangat muda
            text_weight = 'bold'
            text_color = 'black'
        elif value < 500:
            color = '#FFF9C4'  # Kuning muda
            text_weight = 'normal'
            text_color = 'black'
        elif value < 1000:
            color = '#FFE0B2'  # Orange muda
            text_weight = 'normal'
            text_color = 'black'
        else:
            color = '#FFCDD2'  # Merah muda
            text_weight = 'bold'
            text_color = '#C62828'
        
        rect = Rectangle((start_x + j*cell_width, start_y - (i+1)*cell_height),
                        cell_width, cell_height,
                        facecolor=color, edgecolor='black', linewidth=2)
        ax2.add_patch(rect)
        
        # Tambahkan bintang untuk nilai terbaik
        if value == min_val_sp:
            text_display = f'{value:.2f} ★'
        else:
            text_display = f'{value:.2f}'
        
        ax2.text(start_x + j*cell_width + cell_width/2,
                start_y - (i+1)*cell_height + cell_height/2,
                text_display, ha='center', va='center',
                fontsize=12, fontweight=text_weight, color=text_color)

ax2.set_xlim(-0.02, start_x + 2*cell_width + 0.02)
ax2.set_ylim(start_y - 4.5*cell_height, start_y + cell_height + 0.05)

plt.tight_layout(rect=[0, 0.02, 1, 0.94])
plt.savefig('hasil_evaluasi/tabel_kernel_size.png', dpi=300, bbox_inches='tight')
print("\n✓ Tabel perbandingan kernel size disimpan: hasil_evaluasi/tabel_kernel_size.png")

# Print tabel di console
print("\n" + "="*80)
print("TABEL PERBANDINGAN MSE: FILTER vs KERNEL SIZE")
print("="*80)

print("\n📊 GAUSSIAN NOISE")
print("-" * 50)
print(f"{'Filter':<10} {'3x3':>12} {'5x5':>12} {'Terbaik':>12}")
print("-" * 50)
for i, filter_type in enumerate(filter_labels):
    val_3x3 = table_gauss[i, 0]
    val_5x5 = table_gauss[i, 1]
    best = "3x3" if val_3x3 < val_5x5 else "5x5"
    marker = " ⭐" if table_gauss[i].min() == min_val else ""
    print(f"{filter_type:<10} {val_3x3:>12.2f} {val_5x5:>12.2f} {best:>12}{marker}")

print("\n📊 SALT & PEPPER NOISE")
print("-" * 50)
print(f"{'Filter':<10} {'3x3':>12} {'5x5':>12} {'Terbaik':>12}")
print("-" * 50)
for i, filter_type in enumerate(filter_labels):
    val_3x3 = table_sp[i, 0]
    val_5x5 = table_sp[i, 1]
    best = "3x3" if val_3x3 < val_5x5 else "5x5"
    marker = " ⭐" if table_sp[i].min() == min_val_sp else ""
    print(f"{filter_type:<10} {val_3x3:>12.2f} {val_5x5:>12.2f} {best:>12}{marker}")

print("\n" + "="*80)
print("KESIMPULAN:")

# Cari posisi nilai minimum untuk Gaussian
min_pos_gauss = np.unravel_index(np.argmin(table_gauss), table_gauss.shape)
print(f"  Gaussian Noise    : Filter terbaik = {filter_labels[min_pos_gauss[0]]} dengan kernel {kernel_sizes[min_pos_gauss[1]]} (MSE = {min_val:.2f})")

# Cari posisi nilai minimum untuk Salt & Pepper
min_pos_sp = np.unravel_index(np.argmin(table_sp), table_sp.shape)
print(f"  Salt & Pepper     : Filter terbaik = {filter_labels[min_pos_sp[0]]} dengan kernel {kernel_sizes[min_pos_sp[1]]} (MSE = {min_val_sp:.2f})")
print("="*80)

plt.close()
