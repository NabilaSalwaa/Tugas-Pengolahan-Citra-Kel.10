import os
import numpy as np
from PIL import Image
import json

def calculate_mse(original, processed):
    mse = np.mean((original.astype(np.float64) - processed.astype(np.float64)) ** 2)
    return mse

def calculate_psnr(mse):
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def main():
    import glob
    original_dir = "images"
    filtered_dir = "images_filtered"
    output_dir = "hasil_evaluasi"
    if not os.path.exists(original_dir):
        print(f"Error: Folder '{original_dir}/' tidak ditemukan!")
        return
    if not os.path.exists(filtered_dir):
        print(f"Error: Folder '{filtered_dir}/' tidak ditemukan!")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    orig_files = [f for f in os.listdir(original_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    # Cari semua file hasil filter di subfolder
    filtered_files = glob.glob(os.path.join(filtered_dir, "**", "*.png"), recursive=True)
    results = []
    for filt_path in filtered_files:
        f_filt = os.path.basename(filt_path)
        base = f_filt.split('_')[0]
        orig_match = [f for f in orig_files if f.startswith(base)]
        if not orig_match:
            continue
        orig_path = os.path.join(original_dir, orig_match[0])
        orig_img = np.array(Image.open(orig_path))
        filt_img = np.array(Image.open(filt_path))
        # Samakan channel
        if orig_img.shape != filt_img.shape:
            # Jika hasil filter grayscale, konversi original ke grayscale
            if len(filt_img.shape) == 2 and len(orig_img.shape) == 3:
                orig_img = 0.299 * orig_img[:,:,0] + 0.587 * orig_img[:,:,1] + 0.114 * orig_img[:,:,2]
                orig_img = orig_img.astype(np.uint8)
            # Resize jika ukuran berbeda
            min_shape = tuple(min(a, b) for a, b in zip(orig_img.shape, filt_img.shape))
            orig_img = orig_img[:min_shape[0], :min_shape[1]]
            filt_img = filt_img[:min_shape[0], :min_shape[1]]
        mse = calculate_mse(orig_img, filt_img)
        psnr = calculate_psnr(mse)
        results.append({
            "original": orig_match[0],
            "filtered": f_filt,
            "filtered_path": filt_path.replace("\\", "/"),
            "mse": mse,
            "psnr": psnr
        })
    with open(os.path.join(output_dir, "evaluasi_mse_psnr.json"), "w") as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(output_dir, "evaluasi_lengkap.txt"), "w") as f:
        f.write("Analisis Hasil Percobaan:\n\n")
        for r in results:
            f.write(f"Original: {r['original']}, Filtered: {r['filtered']} ({r['filtered_path']}), MSE: {r['mse']:.2f}, PSNR: {r['psnr']:.2f}\n")
        f.write("\nCitra dengan MSE rendah dan PSNR tinggi memiliki kualitas yang lebih baik setelah filtering.\n")
    print("Selesai evaluasi dan analisis. Hasil disimpan di folder 'hasil_evaluasi/'.")

if __name__ == "__main__":
    main()
