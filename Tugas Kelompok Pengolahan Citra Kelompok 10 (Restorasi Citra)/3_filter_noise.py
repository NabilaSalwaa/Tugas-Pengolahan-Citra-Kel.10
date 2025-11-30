import os
import numpy as np
from PIL import Image

def apply_filter_channel(channel, filter_type, window_size, pad):
    padded = np.pad(channel, pad, mode='edge')
    filtered = np.zeros_like(channel)
    h, w = channel.shape
    for i in range(h):
        for j in range(w):
            window = padded[i:i+window_size, j:j+window_size].flatten()
            if filter_type == 'min':
                filtered[i, j] = np.min(window)
            elif filter_type == 'max':
                filtered[i, j] = np.max(window)
            elif filter_type == 'median':
                filtered[i, j] = np.median(window)
            elif filter_type == 'mean':
                filtered[i, j] = np.mean(window)
    return filtered.astype(np.uint8)

def apply_filter(img, filter_type, window_size=3):
    if window_size % 2 == 0:
        window_size += 1
    pad = window_size // 2
    if len(img.shape) == 3:
        filtered = np.zeros_like(img)
        for c in range(img.shape[2]):
            filtered[:,:,c] = apply_filter_channel(img[:,:,c], filter_type, window_size, pad)
        return filtered
    else:
        return apply_filter_channel(img, filter_type, window_size, pad)

def main():
    input_dir = "images_noise"
    output_dir = "images_filtered"
    if not os.path.exists(input_dir):
        print(f"Error: Folder '{input_dir}/' tidak ditemukan!")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not img_files:
        print("Tidak ada file gambar ditemukan di folder 'images_noise/'!")
        return
    window_sizes = [3, 5]
    for fname in img_files:
        img_path = os.path.join(input_dir, fname)
        img = np.array(Image.open(img_path))
        # Tentukan noise type dari nama file
        base_name = os.path.splitext(fname)[0]
        if 'sp' in base_name or 'salt' in base_name:
            noise_type = 'salt_pepper'
        elif 'gauss' in base_name:
            noise_type = 'gaussian'
        else:
            noise_type = 'other'
        for w in window_sizes:
            for ftype in ['min', 'max', 'median', 'mean']:
                filtered = apply_filter(img, ftype, window_size=w)
                # Buat subfolder sesuai filter dan noise type
                subfolder = os.path.join(output_dir, ftype, noise_type)
                if not os.path.exists(subfolder):
                    os.makedirs(subfolder)
                out_name = base_name + f"_{ftype}_{w}x{w}.png"
                out_path = os.path.join(subfolder, out_name)
                Image.fromarray(filtered).save(out_path)
                print(f"Filter {ftype} window {w}x{w} pada {fname} -> {out_path}")
    print("Selesai filtering noise.")

if __name__ == "__main__":
    main()
