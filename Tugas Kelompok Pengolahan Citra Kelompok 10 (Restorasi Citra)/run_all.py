import os
import subprocess

def run_script(script_name):
    print(f"\nMenjalankan {script_name} ...")
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    print(f"Selesai {script_name}\n{'='*60}")

if __name__ == "__main__":
    scripts = [
        "1_konversi_grayscale.py",
        "2_tambah_noise.py",
        "3_filter_noise.py",
        "4_evaluasi_mse.py",
        "5_visualisasi_mse.py",
        "6_tabel_kernel_size.py",
        "7_tabel_mse_psnr_gabungan.py"
    ]
    for script in scripts:
        run_script(script)
    print("Pipeline selesai. Semua hasil ada di folder output masing-masing.")
