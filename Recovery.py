from PIL import Image
from collections import Counter
import numpy as np
import hashlib
import os

# -------------------------------------------------
# PATHS
# -------------------------------------------------
data_file =  r"C:\Users\DELL\Downloads\hash_with_32bit_msb12boat.txt"
tampered_path =r"C:\Users\DELL\OneDrive\Documents\MATLAB\faces\INPUTS\INPUTS\cropped\embedded_outputnew2boat_mask_bottom_strip.tif"
# -------------------------------------------------
# LOAD IMAGE
# -------------------------------------------------
tamp_img = np.array(Image.open(tampered_path).convert("L"))
h, w = tamp_img.shape

BLOCK = 8
BLOCK64 = 64 

# -------------------------------------------------
# READ HASH + MSB (SINGLE FILE)
# -------------------------------------------------
hash_and_msb = {}

with open(data_file, "r") as f:
    for line in f:
        parts = line.strip().split(":")
        coords = parts[0][parts[0].find("(")+1:parts[0].find(")")]
        r, c = map(int, coords.split(","))

        values = parts[1].strip().split()

        block_hash_val = values[0]   # SHA-256
        msb_bits = values[1]         # 32-bit MSB

        hash_and_msb[(r+1, c+1)] = (block_hash_val, msb_bits)

# -------------------------------------------------
# HASH FUNCTION
# -------------------------------------------------
def block_hash(block):
    return hashlib.sha256(block.tobytes()).hexdigest()

# -------------------------------------------------
# DETECT TAMPERED BLOCKS
# -------------------------------------------------
tampered_blocks = set()
rows = h // BLOCK
cols = w // BLOCK

for br in range(rows):
    for bc in range(cols):
        block = tamp_img[br*8:(br+1)*8, bc*8:(bc+1)*8]

        stored_hash = hash_and_msb.get((br+1, bc+1), (None, None))[0]

        if block_hash(block) != stored_hash:
            tampered_blocks.add((br+1, bc+1))

print("Total tampered blocks:", len(tampered_blocks))

# -------------------------------------------------
# SUDOKU PATTERN
# -------------------------------------------------
sudoku = [
[3,7,5,1,0,4,2,6],
[2,6,4,0,5,1,3,7],
[7,2,1,5,4,0,6,3],
[6,3,0,4,7,5,1,2],
[5,1,7,6,2,3,4,0],
[4,0,3,2,6,7,5,1],
[0,4,6,3,1,2,7,5],
[1,5,2,7,3,6,0,4]
]

ZERO8 = "00000000"
recovered_img = tamp_img.tolist()

# -------------------------------------------------
# PROCESS IMAGE
# -------------------------------------------------
for BR in range(h // BLOCK64):
    for BC in range(w // BLOCK64):

        bi, bj = BR*64, BC*64

        block64 = [row[bj:bj+64] for row in recovered_img[bi:bi+64]]

        # split into 8x8 blocks
        sub_blocks = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                sub_blocks[r][c] = [block64[r*8+rr][c*8:c*8+8] for rr in range(8)]

        # sudoku shuffle
        shuffled = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                shuffled[r][sudoku[r][c]] = sub_blocks[r][c]

        # extract auth bits
        auth = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                flat = [px for row in shuffled[r][c] for px in row]
                bits = "".join(str(flat[i] & 1) for i in range(56))
                groups7 = [bits[i*8:(i+1)*8] for i in range(7)]

                groups8 = []
                gi = 0
                for k in range(8):
                    if k == r:
                        groups8.append(ZERO8)
                    else:
                        groups8.append(groups7[gi])
                        gi += 1
                auth[r][c] = groups8

        # majority voting
        rec_auth = [[auth[r][c][:] for c in range(8)] for r in range(8)]
        for c in range(8):
            for k in range(8):
                vals = [auth[r][c][k] for r in range(8) if auth[r][c][k] != ZERO8]
                if vals:
                    maj = Counter(vals).most_common(1)[0][0]
                    for r in range(8):
                        if rec_auth[r][c][k] == ZERO8:
                            rec_auth[r][c][k] = maj

        # recovery
        recovered_sub = [[None]*8 for _ in range(8)]

        for r in range(8):
            for c in range(8):

                global_br = BR*8 + r + 1
                global_bc = BC*8 + c + 1

                # If NOT tampered → keep original
                if (global_br, global_bc) not in tampered_blocks:
                    recovered_sub[r][c] = sub_blocks[r][c]
                    continue

                # -------- LSB recovery --------
                all_bits = "".join(rec_auth[r][c])
                values = [int(all_bits[i:i+8], 2) for i in range(0, 64, 8)]
                avg_val = sum(values) // len(values)
                avg_bin = format(avg_val, '08b')
                lsb4 = avg_bin[4:]

                # -------- MSB recovery --------
                mapped_br = BR*8 + r
                mapped_bc = BC*8 + c

                msb_bits = hash_and_msb.get((mapped_br+1, mapped_bc+1), ("", "0"*32))[1]
                msb_cols = [msb_bits[i*4:(i+1)*4] for i in range(8)]

                # reconstruct block
                new_pixels = []
                for row in range(8):
                    for col in range(8):
                        new_bin = msb_cols[col] + lsb4
                        new_pixels.append(int(new_bin, 2))

                blk = [new_pixels[i*8:(i+1)*8] for i in range(8)]
                recovered_sub[r][c] = blk

        # write back
        for r in range(8):
            for c in range(8):
                for rr in range(8):
                    for cc in range(8):
                        recovered_img[bi+r*8+rr][bj+c*8+cc] = recovered_sub[r][c][rr][cc]

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------
out_path = os.path.splitext(tampered_path)[0] + "_final_recovered122.tif"

Image.fromarray(np.array(recovered_img, dtype=np.uint8)).save(out_path)

print("\nRecovery completed")
print("Saved at:", out_path)
