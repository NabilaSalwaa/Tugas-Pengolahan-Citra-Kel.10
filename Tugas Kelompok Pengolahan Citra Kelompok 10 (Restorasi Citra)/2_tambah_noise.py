import os
import numpy as np
from PIL import Image

def add_salt_pepper_noise(img, noise_level):
    noisy_img = img.copy().astype(np.float64)
    salt_mask = np.random.random(img.shape[:2]) < (noise_level / 2)
    if len(img.shape) == 3:
        for i in range(img.shape[2]):
            noisy_img[:,:,i][salt_mask] = 255
    else:
        noisy_img[salt_mask] = 255
    pepper_mask = np.random.random(img.shape[:2]) < (noise_level / 2)
    if len(img.shape) == 3:
        for i in range(img.shape[2]):
            noisy_img[:,:,i][pepper_mask] = 0
    else:
        noisy_img[pepper_mask] = 0
    return noisy_img.astype(np.uint8)

def add_gaussian_noise(img, mean=0, sigma=25):
    gaussian = np.random.normal(mean, sigma, img.shape)
    noisy_img = img.astype(np.float64) + gaussian
    noisy_img = np.clip(noisy_img, 0, 255)
    return noisy_img.astype(np.uint8)

def main():
    input_dir = "images"
    output_dir = "images_noise"
    if not os.path.exists(input_dir):
        print(f"Error: Folder '{input_dir}/' tidak ditemukan!")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    print("File yang akan diproses:", img_files)
    if not img_files:
        print("Tidak ada file gambar ditemukan di folder 'images/'!")
        return
    sp_levels = [0.05, 0.15]
    gauss_sigmas = [15, 30]
    for fname in img_files:
        img_path = os.path.join(input_dir, fname)
        img = np.array(Image.open(img_path))
        for nl in sp_levels:
            sp_img = add_salt_pepper_noise(img, nl)
            sp_name = os.path.splitext(fname)[0] + f"_sp_{int(nl*100)}.png"
            Image.fromarray(sp_img).save(os.path.join(output_dir, sp_name))
            print(f"Salt & Pepper noise {nl} pada {fname} -> {sp_name}")
        for sigma in gauss_sigmas:
            gauss_img = add_gaussian_noise(img, mean=0, sigma=sigma)
            gauss_name = os.path.splitext(fname)[0] + f"_gauss_{sigma}.png"
            Image.fromarray(gauss_img).save(os.path.join(output_dir, gauss_name))
            print(f"Gaussian noise sigma={sigma} pada {fname} -> {gauss_name}")
    print("Selesai penambahan noise.")

if __name__ == "__main__":
    main()
