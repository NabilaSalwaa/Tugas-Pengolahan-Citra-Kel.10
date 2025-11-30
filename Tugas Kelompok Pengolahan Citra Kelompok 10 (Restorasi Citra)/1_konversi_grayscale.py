import os
import numpy as np
from PIL import Image

def rgb_to_grayscale(img):
    if len(img.shape) == 2:
        return img
    gray = 0.299 * img[:,:,0] + 0.587 * img[:,:,1] + 0.114 * img[:,:,2]
    return gray.astype(np.uint8)

def main():
    input_dir = "images"
    output_dir = "images"
    if not os.path.exists(input_dir):
        print(f"Error: Folder '{input_dir}/' tidak ditemukan!")
        return
    img_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not img_files:
        print("Tidak ada file gambar ditemukan di folder 'images/'!")
        return
    for fname in img_files:
        img_path = os.path.join(input_dir, fname)
        img = np.array(Image.open(img_path))
        gray = rgb_to_grayscale(img)
        gray_img = Image.fromarray(gray)
        gray_name = os.path.splitext(fname)[0] + "_grayscale.png"
        gray_img.save(os.path.join(output_dir, gray_name))
        print(f"Citra {fname} dikonversi ke grayscale dan disimpan sebagai {gray_name}")
    print("Selesai konversi grayscale.")

if __name__ == "__main__":
    main()
