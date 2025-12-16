import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.patches import FancyArrowPatch

# Baca data evaluasi
with open('hasil_evaluasi/evaluasi_mse_psnr.json', 'r') as f:
    data = json.load(f)

# Kelompokkan data berdasarkan noise type dan filter
hasil = {}
for item in data:
    path = item['filtered_path']
    
    # Deteksi jenis noise
    if 'gaussian' in path:
        noise_type = 'gaussian'
    elif 'salt_pepper' in path:
        noise_type = 'salt_pepper'
    else:
        continue
    
    # Deteksi jenis filter
    if '/mean/' in path:
        filter_type = 'mean'
    elif '/median/' in path:
        filter_type = 'median'
    elif '/max/' in path:
        filter_type = 'max'
    elif '/min/' in path:
        filter_type = 'min'
    else:
        continue
    
    # Deteksi kategori gambar
    filename = item['filtered'].lower()
    
    # Deteksi RGB vs Grayscale
    if 'grayscale' in filename:
        color_mode = 'Gray'
    else:
        color_mode = 'RGB'
    
    # Deteksi Landscape vs Portrait
    if 'landscape' in filename:
        image_type = 'Landscape'
    else:
        image_type = 'Portrait'
    
    category = f'{image_type} {color_mode}'
    
    key = (noise_type, filter_type, category)
    if key not in hasil:
        hasil[key] = []
    hasil[key].append(item['mse'])

# Hitung rata-rata MSE untuk setiap kombinasi
avg_mse = {}
for key, values in hasil.items():
    avg_mse[key] = np.mean(values)

print("Data MSE berhasil dikelompokkan")
print(f"Total kombinasi: {len(avg_mse)}")

# =====================================================================
# GRAFIK UTAMA: Perbandingan Filter dengan Style Mirip Contoh
# =====================================================================

def create_comparison_chart(noise_type, noise_label, filename):
    """Buat grafik perbandingan dengan style mirip contoh"""
    
    # Definisi kategori dan filter
    categories = ['Landscape RGB', 'Portrait RGB', 'Landscape Gray', 'Portrait Gray']
    filters = ['mean', 'median', 'max', 'min']
    filter_labels = ['Mean', 'Median', 'Max', 'Min']
    colors = ['#E57373', '#FFB74D', '#81C784', '#64B5F6']  # Merah, Orange, Hijau, Biru
    
    # Kumpulkan data
    data_by_filter = {f: [] for f in filters}
    best_filters = []
    
    for cat in categories:
        values_for_cat = []
        for filter_type in filters:
            key = (noise_type, filter_type, cat)
            mse_val = avg_mse.get(key, 0)
            data_by_filter[filter_type].append(mse_val)
            values_for_cat.append(mse_val)
        
        # Tentukan filter terbaik untuk kategori ini
        if values_for_cat:
            min_idx = values_for_cat.index(min([v for v in values_for_cat if v > 0]))
            best_filters.append(filters[min_idx])
    
    # Buat figure dengan border
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor('#D3D3D3')  # Gray background
    
    # Tambahkan border ungu
    border = Rectangle((0, 0), 1, 1, transform=fig.transFigure, 
                       fill=False, edgecolor='#8B5BA5', linewidth=10, zorder=1000)
    fig.patches.append(border)
    
    # Buat axes dengan margin untuk border
    ax = fig.add_axes([0.08, 0.15, 0.84, 0.75])
    ax.set_facecolor('white')
    
    # Plot bars
    x = np.arange(len(categories))
    width = 0.18
    
    for i, (filter_type, filter_label) in enumerate(zip(filters, filter_labels)):
        values = data_by_filter[filter_type]
        bars = ax.bar(x + i*width - 1.5*width, values, width, 
                      label=filter_label, color=colors[i], alpha=0.85, edgecolor='black', linewidth=0.5)
        
        # Tambahkan nilai di atas bar
        for j, (bar, cat) in enumerate(zip(bars, categories)):
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
                
                # Highlight filter terbaik dengan kotak dan panah
                if filter_type == best_filters[j]:
                    # Kotak highlight
                    fancy_box = FancyBboxPatch(
                        (bar.get_x() - 0.02, height + max(values)*0.18),
                        bar.get_width() + 0.04, max(values)*0.10,
                        boxstyle="round,pad=0.01", 
                        edgecolor='#2E7D32', facecolor='#C8E6C9',
                        linewidth=2, zorder=10
                    )
                    ax.add_patch(fancy_box)
                    
                    # Label "Terbaik"
                    ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.40,
                           'TERBAIK',
                           ha='center', va='center', fontsize=9, 
                           fontweight='bold', color='#1B5E20',
                           bbox=dict(boxstyle='round,pad=0.4', facecolor='#90EE90', 
                                   edgecolor='#2E7D32', linewidth=2.5))
                    
                    # Panah pointing ke bar
                    arrow = FancyArrowPatch(
                        (bar.get_x() + bar.get_width()/2., height + max(values)*0.18),
                        (bar.get_x() + bar.get_width()/2., height + max(values)*0.005),
                        arrowstyle='->', mutation_scale=20, linewidth=2,
                        color='#2E7D32', zorder=11
                    )
                    ax.add_patch(arrow)
    
    # Konfigurasi axes
    ax.set_xlabel('Kategori Citra', fontsize=13, fontweight='bold')
    ax.set_ylabel('Nilai MSE (Lebih Rendah = Lebih Baik)', fontsize=12, fontweight='bold')
    
    # Judul dengan style yang lebih menarik
    title_text = f'Analisis Efektivitas Filter (MSE)\n{filter_labels[0]} Filter Dominan, Kecuali pada {noise_label}'
    ax.set_title(title_text, fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95, edgecolor='black')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Tambahkan formula MSE di bagian bawah
    formula_text = r'$MSE = \frac{1}{MN} \sum_{M}^{i=1} \sum_{N}^{j=1} (f(i,j) - \hat{f}(i,j))^2$'
    fig.text(0.5, 0.05, formula_text, ha='center', fontsize=14, 
             bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                      edgecolor='black', linewidth=1.5))
    
    # Tambahkan watermark/logo placeholder di pojok (optional)
    fig.text(0.02, 0.97, '🎯', ha='left', va='top', fontsize=40, alpha=0.3)
    fig.text(0.98, 0.97, '📊', ha='right', va='top', fontsize=40, alpha=0.3)
    
    plt.savefig(f'hasil_evaluasi/{filename}', dpi=300, bbox_inches='tight', 
                facecolor=fig.get_facecolor())
    print(f"✓ Grafik disimpan: hasil_evaluasi/{filename}")
    plt.close()

# Grafik individual tidak perlu karena sudah ada grafik gabungan
# create_comparison_chart('gaussian', 'Portrait Gray', 
#                        'grafik_perbandingan_gaussian.png')
# create_comparison_chart('salt_pepper', 'Landscape RGB',
#                        'grafik_perbandingan_saltpepper.png')

# =====================================================================
# GRAFIK GABUNGAN: Kedua Noise Type
# =====================================================================

categories = ['Landscape RGB', 'Portrait RGB', 'Landscape Gray', 'Portrait Gray']
filters = ['mean', 'median', 'max', 'min']
filter_labels = ['Mean', 'Median', 'Max', 'Min']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Perbandingan Efektivitas Filter pada Berbagai Jenis Noise', 
             fontsize=16, fontweight='bold', y=0.98)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Perbandingan Efektivitas Filter pada Berbagai Jenis Noise', 
             fontsize=16, fontweight='bold', y=0.98)

colors = ['#E57373', '#FFB74D', '#81C784', '#64B5F6']

# Grafik 1: Gaussian Noise
x = np.arange(len(categories))
width = 0.2

for i, (filter_type, filter_label) in enumerate(zip(filters, filter_labels)):
    mse_values = []
    for cat in categories:
        key = ('gaussian', filter_type, cat)
        mse_values.append(avg_mse.get(key, 0))
    
    bars = ax1.bar(x + i*width, mse_values, width, label=filter_label, 
                   color=colors[i], alpha=0.85, edgecolor='black', linewidth=0.5)
    
    # Tambahkan nilai di atas bar
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

ax1.set_xlabel('Kategori Citra', fontsize=12, fontweight='bold')
ax1.set_ylabel('Nilai MSE (Lebih Rendah = Lebih Baik)', fontsize=11, fontweight='bold')
ax1.set_title('Gaussian Noise', fontsize=13, fontweight='bold', pad=15)
ax1.set_xticks(x + width * 1.5)
ax1.set_xticklabels(categories, fontsize=10, rotation=15, ha='right')
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Grafik 2: Salt & Pepper Noise
for i, (filter_type, filter_label) in enumerate(zip(filters, filter_labels)):
    mse_values = []
    for cat in categories:
        key = ('salt_pepper', filter_type, cat)
        mse_values.append(avg_mse.get(key, 0))
    
    bars = ax2.bar(x + i*width, mse_values, width, label=filter_label,
                   color=colors[i], alpha=0.85, edgecolor='black', linewidth=0.5)
    
    # Tambahkan nilai di atas bar
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

ax2.set_xlabel('Kategori Citra', fontsize=12, fontweight='bold')
ax2.set_ylabel('Nilai MSE (Lebih Rendah = Lebih Baik)', fontsize=11, fontweight='bold')
ax2.set_title('Salt & Pepper Noise', fontsize=13, fontweight='bold', pad=15)
ax2.set_xticks(x + width * 1.5)
ax2.set_xticklabels(categories, fontsize=10, rotation=15, ha='right')
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('hasil_evaluasi/grafik_perbandingan_mse.png', dpi=300, bbox_inches='tight')
print("✓ Grafik perbandingan MSE disimpan: hasil_evaluasi/grafik_perbandingan_mse.png")
plt.close()

print("\n" + "="*80)
print("TABEL PERBANDINGAN MSE")
print("="*80)

# Tabel untuk Gaussian Noise
print("\n📊 GAUSSIAN NOISE")
print("-" * 80)
table_data_gauss = []
for cat in categories:
    row = {'Kategori': cat}
    for filter_type in filters:
        key = ('gaussian', filter_type, cat)
        row[filter_type.capitalize()] = avg_mse.get(key, 0)
    table_data_gauss.append(row)

df_gauss = pd.DataFrame(table_data_gauss)
df_gauss = df_gauss.round(2)

# Temukan nilai terbaik (terendah) per kategori
for idx, row in df_gauss.iterrows():
    values = [row['Mean'], row['Median'], row['Max'], row['Min']]
    min_val = min(values)
    best_filter = ['Mean', 'Median', 'Max', 'Min'][values.index(min_val)]
    print(f"\n{row['Kategori']}:")
    print(f"  Mean   : {row['Mean']:>10.2f}")
    print(f"  Median : {row['Median']:>10.2f}")
    print(f"  Max    : {row['Max']:>10.2f}")
    print(f"  Min    : {row['Min']:>10.2f}")
    print(f"  ⭐ TERBAIK: {best_filter} (MSE = {min_val:.2f})")

# Tabel untuk Salt & Pepper Noise
print("\n" + "="*80)
print("\n📊 SALT & PEPPER NOISE")
print("-" * 80)
table_data_sp = []
for cat in categories:
    row = {'Kategori': cat}
    for filter_type in filters:
        key = ('salt_pepper', filter_type, cat)
        row[filter_type.capitalize()] = avg_mse.get(key, 0)
    table_data_sp.append(row)

df_sp = pd.DataFrame(table_data_sp)
df_sp = df_sp.round(2)

# Temukan nilai terbaik (terendah) per kategori
for idx, row in df_sp.iterrows():
    values = [row['Mean'], row['Median'], row['Max'], row['Min']]
    min_val = min(values)
    best_filter = ['Mean', 'Median', 'Max', 'Min'][values.index(min_val)]
    print(f"\n{row['Kategori']}:")
    print(f"  Mean   : {row['Mean']:>10.2f}")
    print(f"  Median : {row['Median']:>10.2f}")
    print(f"  Max    : {row['Max']:>10.2f}")
    print(f"  Min    : {row['Min']:>10.2f}")
    print(f"  ⭐ TERBAIK: {best_filter} (MSE = {min_val:.2f})")

print("\n" + "="*80)

# =====================================================================
# TABEL VISUAL DENGAN FORMAT CLEAN DAN MUDAH DIBACA
# =====================================================================

def create_clean_table(noise_type, noise_label, filename, table_data):
    """Buat tabel visual dengan format bersih dan mudah dibaca"""
    
    fig = plt.figure(figsize=(12, 8))
    fig.suptitle(f'Tabel Perbandingan MSE - {noise_label}', 
                fontsize=16, fontweight='bold', y=0.96)
    
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Dimensi sel
    cell_height = 0.14
    cell_width = 0.18
    label_width = 0.2
    start_x = label_width
    start_y = 0.8
    
    # Konversi ke numpy array
    table_array = np.array(table_data)
    
    # Cari nilai minimum untuk highlighting
    min_val = np.min(table_array)
    
    # Header kolom (Kategori Citra) - background biru
    for j, cat in enumerate(categories):
        rect = Rectangle((start_x + j*cell_width, start_y), cell_width, cell_height,
                        facecolor='#4A90E2', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        # Split nama kategori jadi 2 baris
        cat_lines = cat.split()
        if len(cat_lines) == 2:
            cat_text = f"{cat_lines[0]}\n{cat_lines[1]}"
        else:
            cat_text = cat
        ax.text(start_x + j*cell_width + cell_width/2, start_y + cell_height/2,
               cat_text, ha='center', va='center', color='white',
               fontsize=10, fontweight='bold')
    
    # Data cells dengan border presisi
    for i, filter_label in enumerate(filter_labels):
        # Header baris (Filter name) - background abu-abu
        rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                        facecolor='#D3D3D3', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
               filter_label, ha='center', va='center',
               fontsize=11, fontweight='bold')
        
        for j in range(len(categories)):
            value = table_array[i, j]
            
            # Tentukan warna background berdasarkan nilai
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
                           facecolor=color, edgecolor='black', linewidth=1.5)
            ax.add_patch(rect)
            
            # Tambahkan bintang untuk nilai terbaik
            if value == min_val:
                text_display = f'{value:.1f}\n★'
            else:
                text_display = f'{value:.1f}'
            
            ax.text(start_x + j*cell_width + cell_width/2,
                   start_y - (i+1)*cell_height + cell_height/2,
                   text_display, ha='center', va='center',
                   fontsize=10, fontweight=text_weight, color=text_color)
    
    ax.set_xlim(-0.02, start_x + len(categories)*cell_width + 0.02)
    ax.set_ylim(start_y - (len(filter_labels)+1)*cell_height, start_y + cell_height + 0.05)
    
    # Tambahkan legend di bawah
    legend_y = start_y - (len(filter_labels)+1.5)*cell_height
    legend_text = (
        'Kode Warna: Hijau Tua (Terbaik) | Hijau Muda (<100) | '
        'Kuning (100-500) | Orange (500-1000) | Merah (>1000)'
    )
    ax.text(start_x + len(categories)*cell_width/2, legend_y,
           legend_text, ha='center', va='top', fontsize=9,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#F5F5F5',
                    edgecolor='gray', linewidth=1))
    
    plt.savefig(f'hasil_evaluasi/{filename}', dpi=300, bbox_inches='tight')
    print(f"✓ Tabel disimpan: hasil_evaluasi/{filename}")
    plt.close()

# Siapkan data untuk tabel
table_gauss_data = []
for filter_type in filters:
    row = []
    for cat in categories:
        key = ('gaussian', filter_type, cat)
        row.append(avg_mse.get(key, 0))
    table_gauss_data.append(row)

table_sp_data = []
for filter_type in filters:
    row = []
    for cat in categories:
        key = ('salt_pepper', filter_type, cat)
        row.append(avg_mse.get(key, 0))
    table_sp_data.append(row)

# # Buat tabel individual
# create_clean_table('gaussian', 'Gaussian Noise', 
#                   'tabel_gaussian.png', table_gauss_data)

# create_clean_table('salt_pepper', 'Salt & Pepper Noise',
#                   'tabel_saltpepper.png', table_sp_data)

# Buat tabel gabungan side-by-side
fig = plt.figure(figsize=(18, 9))
fig.suptitle('Perbandingan Lengkap: Nilai MSE untuk Semua Filter dan Kategori Citra', 
            fontsize=16, fontweight='bold', y=0.97)

# Dimensi sel
cell_height = 0.14
cell_width = 0.16
label_width = 0.15
start_y = 0.75

# Tabel 1: Gaussian (kiri)
ax1 = fig.add_subplot(121)
ax1.axis('off')
ax1.text(0.5, 1.04, 'Gaussian Noise', transform=ax1.transAxes,
        ha='center', fontsize=16, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD', 
                 edgecolor='#1976D2', linewidth=2))

start_x = label_width
table_gauss_array = np.array(table_gauss_data)
min_val_gauss = np.min(table_gauss_array)

# Header kolom
for j, cat in enumerate(categories):
    rect = Rectangle((start_x + j*cell_width, start_y), cell_width, cell_height,
                    facecolor='#4A90E2', edgecolor='black', linewidth=1.5)
    ax1.add_patch(rect)
    cat_lines = cat.split()
    cat_text = f"{cat_lines[0]}\n{cat_lines[1]}" if len(cat_lines) == 2 else cat
    ax1.text(start_x + j*cell_width + cell_width/2, start_y + cell_height/2,
           cat_text, ha='center', va='center', color='white',
           fontsize=9, fontweight='bold')

# Data cells
for i, filter_label in enumerate(filter_labels):
    rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                    facecolor='#D3D3D3', edgecolor='black', linewidth=1.5)
    ax1.add_patch(rect)
    ax1.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
           filter_label, ha='center', va='center',
           fontsize=10, fontweight='bold')
    
    for j in range(len(categories)):
        value = table_gauss_array[i, j]
        
        if value == min_val_gauss:
            color = '#90EE90'
            text_weight = 'bold'
            text_color = '#1B5E20'
            text_display = f'{value:,.2f}★'
        elif value < 100:
            color = '#C8E6C9'
            text_weight = 'normal'
            text_color = 'black'
            text_display = f'{value:,.2f}'
        elif value < 500:
            color = '#FFF9C4'
            text_weight = 'normal'
            text_color = 'black'
            text_display = f'{value:,.2f}'
        elif value < 1000:
            color = '#FFE0B2'
            text_weight = 'normal'
            text_color = 'black'
            text_display = f'{value:,.2f}'
        else:
            color = '#FFCDD2'
            text_weight = 'bold'
            text_color = '#C62828'
            text_display = f'{value:,.2f}'
        
        rect = Rectangle((start_x + j*cell_width, start_y - (i+1)*cell_height),
                       cell_width, cell_height,
                       facecolor=color, edgecolor='black', linewidth=1.5)
        ax1.add_patch(rect)
        ax1.text(start_x + j*cell_width + cell_width/2,
               start_y - (i+1)*cell_height + cell_height/2,
               text_display, ha='center', va='center',
               fontsize=10, fontweight=text_weight, color=text_color)

ax1.set_xlim(-0.01, start_x + len(categories)*cell_width + 0.01)
ax1.set_ylim(start_y - (len(filter_labels)+1)*cell_height, start_y + cell_height + 0.02)

# Tabel 2: Salt & Pepper (kanan)
ax2 = fig.add_subplot(122)
ax2.axis('off')
ax2.text(0.5, 1.04, 'Salt & Pepper Noise', transform=ax2.transAxes,
        ha='center', fontsize=16, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE0B2', 
                 edgecolor='#E65100', linewidth=2))

table_sp_array = np.array(table_sp_data)
min_val_sp = np.min(table_sp_array)

# Gunakan start_x yang sama seperti Gaussian
start_x_sp = label_width  # Sama dengan tabel Gaussian

# Header kolom
for j, cat in enumerate(categories):
    rect = Rectangle((start_x_sp + j*cell_width, start_y), cell_width, cell_height,
                    facecolor='#4A90E2', edgecolor='black', linewidth=1.5)
    ax2.add_patch(rect)
    cat_lines = cat.split()
    cat_text = f"{cat_lines[0]}\n{cat_lines[1]}" if len(cat_lines) == 2 else cat
    ax2.text(start_x_sp + j*cell_width + cell_width/2, start_y + cell_height/2,
           cat_text, ha='center', va='center', color='white',
           fontsize=9, fontweight='bold')

# Data cells
for i, filter_label in enumerate(filter_labels):
    rect = Rectangle((0, start_y - (i+1)*cell_height), label_width, cell_height,
                    facecolor='#D3D3D3', edgecolor='black', linewidth=1.5)
    ax2.add_patch(rect)
    ax2.text(label_width/2, start_y - (i+1)*cell_height + cell_height/2,
           filter_label, ha='center', va='center',
           fontsize=10, fontweight='bold')
    
    for j in range(len(categories)):
        value = table_sp_array[i, j]
        
        if value == min_val_sp:
            color = '#90EE90'
            text_weight = 'bold'
            text_color = '#1B5E20'
            text_display = f'{value:,.2f}★'
        elif value < 100:
            color = '#C8E6C9'
            text_weight = 'normal'
            text_color = 'black'
            text_display = f'{value:,.2f}'
        elif value < 500:
            color = '#FFF9C4'
            text_weight = 'normal'
            text_color = 'black'
            text_display = f'{value:,.2f}'
        elif value < 1000:
            color = '#FFE0B2'
            text_weight = 'normal'
            text_color = 'black'
            text_display = f'{value:,.2f}'
        else:
            color = '#FFCDD2'
            text_weight = 'bold'
            text_color = '#C62828'
            text_display = f'{value:,.2f}'
        
        rect = Rectangle((start_x_sp + j*cell_width, start_y - (i+1)*cell_height),
                       cell_width, cell_height,
                       facecolor=color, edgecolor='black', linewidth=1.5)
        ax2.add_patch(rect)
        ax2.text(start_x_sp + j*cell_width + cell_width/2,
               start_y - (i+1)*cell_height + cell_height/2,
               text_display, ha='center', va='center',
               fontsize=10, fontweight=text_weight, color=text_color)

ax2.set_xlim(-0.01, start_x_sp + len(categories)*cell_width + 0.01)
ax2.set_ylim(start_y - (len(filter_labels)+1)*cell_height, start_y + cell_height + 0.02)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('hasil_evaluasi/tabel_perbandingan_mse.png', dpi=300, bbox_inches='tight')
print("✓ Tabel gabungan disimpan: hasil_evaluasi/tabel_perbandingan_mse.png")
plt.close()

print("\n" + "="*80)
print("SELESAI! File yang dihasilkan:")
print("  1. hasil_evaluasi/grafik_perbandingan_mse.png")
print("  2. hasil_evaluasi/tabel_perbandingan_mse.png")
print("="*80)
