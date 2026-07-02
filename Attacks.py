import cv2
import numpy as np
import random

# -----------------------------
# INPUT IMAGE PATH (TIFF)
# -----------------------------
#change this path according to your local system
input_path = (r"C:\Users\DELL\admininterface\adminapp\Final review\embedded_outputnew2barbara.tif")  # change this to your file

# Load image (works for grayscale or color)
img = cv2.imread(input_path)
if img is None:
    print("Error loading image")
    exit()

h, w = img.shape[:2]

# -----------------------------
# FUNCTION: Compute region size
# -----------------------------
def get_region_size(h, w, percent):
    total_pixels = h * w
    target_pixels = int((percent / 100) * total_pixels)

    # square approximation
    side = int(np.sqrt(target_pixels))
    return max(1, side), max(1, side)

# -----------------------------
# 1. COPY-MOVE ATTACK
# -----------------------------
def copy_move_attack(image, percent):
    img_copy = image.copy()
    h, w = img_copy.shape[:2]

    rh, rw = get_region_size(h, w, percent)

    # Source patch
    x1 = random.randint(0, w - rw)
    y1 = random.randint(0, h - rh)
    patch = img_copy[y1:y1+rh, x1:x1+rw]

    # Destination patch
    x2 = random.randint(0, w - rw)
    y2 = random.randint(0, h - rh)

    img_copy[y2:y2+rh, x2:x2+rw] = patch
    return img_copy

# -----------------------------
# 2. SINGLE CROP ATTACK
# -----------------------------
def crop_attack(image, percent):
    img_crop = image.copy()
    h, w = img_crop.shape[:2]

    rh, rw = get_region_size(h, w, percent)

    x = random.randint(0, w - rw)
    y = random.randint(0, h - rh)

    img_crop[y:y+rh, x:x+rw] = 0  # black region
    return img_crop

# -----------------------------
# 3. MULTIPLE CROP ATTACK
# -----------------------------
def multiple_crop_attack(image, percent, parts=3):
    img_multi = image.copy()
    h, w = img_multi.shape[:2]

    each_percent = percent / parts

    for _ in range(parts):
        rh, rw = get_region_size(h, w, each_percent)

        x = random.randint(0, w - rw)
        y = random.randint(0, h - rh)

        img_multi[y:y+rh, x:x+rw] = 0

    return img_multi

# -----------------------------
# APPLY ATTACKS
# -----------------------------
percent_5 = 5
percent_137 = 1.37
percent_10=10

# --- 5% ---
copy_5 = copy_move_attack(img, percent_5)
crop_5 = crop_attack(img, percent_5)
multi_5 = multiple_crop_attack(img, percent_5)

# --- 1.37% ---
copy_137 = copy_move_attack(img, percent_137)
crop_137 = crop_attack(img, percent_137)
multi_137 = multiple_crop_attack(img, percent_137)


copy_10 = copy_move_attack(img, percent_10)
crop_10 = crop_attack(img, percent_10)
multi_10 = multiple_crop_attack(img, percent_10)

# -----------------------------
# SAVE OUTPUTS (TIFF)
# -----------------------------
cv2.imwrite("copy_5c.tif", copy_5)
cv2.imwrite("crop_5c.tif", crop_5)
cv2.imwrite("multi_5c.tif", multi_5)

cv2.imwrite("copy_1_37c.tif", copy_137)
cv2.imwrite("crop_1_37c.tif", crop_137)
cv2.imwrite("multi_1_37c.tif", multi_137)

cv2.imwrite("copy_10c.tif", copy_10)
cv2.imwrite("crop_10c.tif", crop_10)
cv2.imwrite("multi_10c.tif", multi_10)

print("All TIFF attack images generated successfully!")
