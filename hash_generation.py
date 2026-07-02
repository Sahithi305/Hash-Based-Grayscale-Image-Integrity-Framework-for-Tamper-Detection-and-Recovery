from PIL import Image
import numpy as np
import hashlib

# -------------------------------------------------
# INPUT IMAGE
# -------------------------------------------------
# change this path according to your local system
img_path = r"C:\Users\sathv\OneDrive\Documents\boat\IE_Basics\Gray_test_images_original\task-2\verification\embedded_outputnew2.tif"
img = np.array(Image.open(img_path).convert("L"))

h, w = img.shape
BLOCK = 8

# -------------------------------------------------
# HASH FUNCTION
# -------------------------------------------------
def block_hash(block):
    return hashlib.sha256(block.tobytes()).hexdigest()

# -------------------------------------------------
# OUTPUT FILE
# -------------------------------------------------
out_file = r"hash_with_32bit_msb12.txt"

with open(out_file, "w") as fout:

    for br in range(0, h, BLOCK):
        for bc in range(0, w, BLOCK):

            block = img[br:br+8, bc:bc+8]

            if block.shape != (8, 8):
                continue

            # -------------------------------
            # HASH
            # -------------------------------
            hval = block_hash(block)

            # -------------------------------
            # MSB EXTRACTION
            # -------------------------------
            msb_matrix = []

            for r in range(8):
                row = []
                for c in range(8):
                    px = block[r][c]
                    msb = px >> 4
                    row.append(msb)
                msb_matrix.append(row)

            # -------------------------------
            # COLUMN-WISE AVERAGE
            # -------------------------------
            col_avg = []
            for c in range(8):
                vals = [msb_matrix[r][c] for r in range(8)]
                avg = sum(vals) // 8
                col_avg.append(avg)

            # -------------------------------
            # 32-bit STRING
            # -------------------------------
            msb_32bit = "".join(format(v, '04b') for v in col_avg)

            # -------------------------------
            # WRITE (MATCH RECOVERY CODE)
            # -------------------------------
            block_r = br // 8   # starts from 0
            block_c = bc // 8

            # FORMAT: (r,c):hash msb
            fout.write(f"({block_r},{block_c}):{hval} {msb_32bit}\n")

print("File generated:", out_file)
