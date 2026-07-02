import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# -----------------------------
# Load Images
# -----------------------------
original = cv2.imread(r"C:\Users\DELL\OneDrive\Documents\MATLAB\faces\Gray_test_images_original\4_boat.TIF", cv2.IMREAD_GRAYSCALE)
tampered = cv2.imread(r"C:\Users\DELL\OneDrive\Documents\MATLAB\faces\INPUTS\INPUTS\cropped\embedded_outputnew2boat_mask_bottom_strip.tif",cv2.IMREAD_GRAYSCALE)
recovered = cv2.imread(r"C:\Users\DELL\OneDrive\Documents\MATLAB\faces\INPUTS\INPUTS\cropped\embedded_outputnew2boat_mask_bottom_strip_final_recovered122.tif", cv2.IMREAD_GRAYSCALE)

if original is None or tampered is None or recovered is None:
    print("Error loading images")
    exit()

# -----------------------------
# (Optional) Post-processing ONLY for recovered
# -----------------------------
# Try one of these:
#recovered_med = cv2.medianBlur(recovered, 5)          # good for salt & pepper
# recovered_med = cv2.GaussianBlur(recovered, (5,5), 0)  # smoother look

# -----------------------------
# Metrics
# -----------------------------
def calculate_mse(img1, img2):
    return np.mean((img1.astype(np.float32) - img2.astype(np.float32)) ** 2)

def calculate_psnr(img1, img2):
    mse = calculate_mse(img1, img2)
    if mse == 0:
        return 100
    return 10 * np.log10((255 * 255) / mse)

def calculate_ssim(img1, img2):
    val, _ = ssim(img1, img2, full=True)
    return val

# -----------------------------
# Compute & Print
# -----------------------------
def report(name, ref, test):
    print(f"\n{name}")
    print(f"MSE  : {calculate_mse(ref, test):.4f}")
    print(f"PSNR : {calculate_psnr(ref, test):.4f} dB")
    print(f"SSIM : {calculate_ssim(ref, test):.4f}")

print("===== RESULTS =====")
report("Original vs Tampered", original, tampered)
report("Original vs Recovered (raw)", original, recovered)
#report("Original vs Recovered (post-processed)", original, recovered_med)
