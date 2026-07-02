from PIL import Image, ImageDraw
import hashlib
import numpy as np
from collections import deque
import os

# -------------------------------------------------
# LOAD IMAGES
# -------------------------------------------------
# change this path according to your local system
original_path = r"C:\Users\DELL\admininterface\adminapp\embedded_outputnew2aero(new).tif"
tampered_path = r"C:\Users\DELL\admininterface\adminapp\attack_multi_5.tiff"

orig_img = Image.open(original_path).convert("L")
tamp_img = Image.open(tampered_path).convert("L")

orig = np.array(orig_img)
tamp = np.array(tamp_img)

h, w = orig.shape
block_size = 8

# -------------------------------------------------
# HASH FUNCTION
# -------------------------------------------------
def get_block_hash(block):
    return hashlib.sha256(block.tobytes()).hexdigest()

# -------------------------------------------------
# FIND TAMPERED BLOCKS
# -------------------------------------------------
tampered_blocks = set()

for i in range(0, h, block_size):
    for j in range(0, w, block_size):

        orig_block = orig[i:i+block_size, j:j+block_size]
        tamp_block = tamp[i:i+block_size, j:j+block_size]

        if orig_block.shape != (8, 8):
            continue

        if get_block_hash(orig_block) != get_block_hash(tamp_block):
            tampered_blocks.add((i, j))

print("Tampered blocks detected:", len(tampered_blocks))

# -------------------------------------------------
# MERGE NEIGHBORING BLOCKS INTO REGIONS
# -------------------------------------------------
visited = set()
regions = []

directions = [(8,0), (-8,0), (0,8), (0,-8)]

for block in tampered_blocks:
    if block in visited:
        continue

    queue = deque([block])
    region = []

    while queue:
        current = queue.popleft()
        if current in visited:
            continue

        visited.add(current)
        region.append(current)

        for di, dj in directions:
            neighbor = (current[0] + di, current[1] + dj)
            if neighbor in tampered_blocks and neighbor not in visited:
                queue.append(neighbor)

    regions.append(region)

print("Tampered regions found:", len(regions))

# -------------------------------------------------
# DRAW BOUNDING BOX
# -------------------------------------------------
output_img = tamp_img.convert("RGB")
draw = ImageDraw.Draw(output_img)

for region in regions:
    rows = [b[0] for b in region]
    cols = [b[1] for b in region]

    top = min(rows)
    bottom = max(rows) + block_size
    left = min(cols)
    right = max(cols) + block_size

    draw.rectangle([left, top, right, bottom], outline="red", width=3)

# -------------------------------------------------
# SAVE RESULT
# -------------------------------------------------
output_path = r"C:\Users\DELL\OneDrive\Documents\MATLAB\faces\INPUTS\INPUTS\cropping1.png"

output_img.save(output_path)

print("Result saved at:", output_path)

output_img.show()
