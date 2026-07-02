from PIL import Image

# -------------------------------------------------
# LOAD GRAYSCALE IMAGE
# -------------------------------------------------
#change this path according to your local system
img_path = r"C:\Users\DELL\OneDrive\Documents\MATLAB\faces\Gray_test_images_original\4_boat.TIF"
img_pil = Image.open(img_path).convert("L")
w, h = img_pil.size
pixels = list(img_pil.getdata())

img = [pixels[i*w:(i+1)*w] for i in range(h)]
final_img = [row[:] for row in img]

# -------------------------------------------------
# SUDOKU MAPPING (8×8)
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

printed = False

# -------------------------------------------------
# PROCESS IMAGE IN 64×64 BLOCKS
# -------------------------------------------------
for bi in range(0, 256, 64):
    for bj in range(0, 256, 64):

        block64 = [row[bj:bj+64] for row in img[bi:bi+64]]

        # ---- Divide into 8×8 blocks ----
        sub_blocks = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                sub_blocks[r][c] = [
                    block64[r*8+rr][c*8:c*8+8] for rr in range(8)
                ]
        print("before sudoku",sub_blocks)

        # ---- Sudoku Shuffle ----
        shuffled_blocks = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                shuffled_blocks[r][sudoku[r][c]] = sub_blocks[r][c]
        print("after sudoku",shuffled_blocks)

        # -------------------------------------------------
        # PRINT AFTER SUDOKU (BLOCK 0,0)
        # -------------------------------------------------
        if not printed:
            print("\nAFTER SUDOKU (8×8 BLOCK [0,0])")
            print("Pixel  (Binary)")
            for row in shuffled_blocks[0][0]:
                for px in row:
                    print(f"{px:3d} ({px:08b})", end="  ")
                print()

        # ---- Compute averages ----
        avg = [[0]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                avg[r][c] = sum(sum(row) for row in shuffled_blocks[r][c]) // 64

        bin_avg = [[format(avg[r][c], '08b') for c in range(8)] for r in range(8)]
        print("average",bin_avg)

        if not printed:
            print("\nAVERAGE VALUES (BINARY):")
            for row in bin_avg:
                print(row)

        # ---- EMBEDDING ----
        for r in range(8):
            for c in range(8):

                #  56-bit string
                bit_string = ""
                for rr in range(8):
                    if rr != r:
                        bit_string += bin_avg[rr][c]

                flat = [px for row in shuffled_blocks[r][c] for px in row]

                for i in range(56):
                    flat[i] = (flat[i] & 0xFE) | int(bit_string[i])

                shuffled_blocks[r][c] = [
                    flat[i*8:(i+1)*8] for i in range(8)
                ]

                # -------------------------------------------------
                # PRINT EMBEDDING DETAILS (ONLY FIRST BLOCK)
                # -------------------------------------------------
                if not printed and r == 0 and c == 0:
                    print("\n56-BIT CONCATENATED STRING:")
                    print(bit_string)
                    print("Length:", len(bit_string))

                    print("\nAFTER EMBEDDING (8×8 BLOCK [0,0])")
                    print("Pixel  (Binary)")
                    for row in shuffled_blocks[0][0]:
                        for px in row:
                            print(f"{px:3d} ({px:08b})", end="  ")
                        print()

                    extracted = ""
                    count = 0
                    for rr in range(8):
                        for cc in range(8):
                            if count < 56:
                                extracted += str(shuffled_blocks[0][0][rr][cc] & 1)
                                count += 1

                    print("\nEXTRACTED 56 LSBs FROM BLOCK:")
                    print(extracted)

                    printed = True

        # -------------------------------------------------
        # REVERSE SUDOKU 
        # -------------------------------------------------
        deshuffled = [[None]*8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                orig_col = sudoku[r].index(c)
                deshuffled[r][orig_col] = shuffled_blocks[r][c]

        # ---- Reconstruct 64×64 ----
        reconstructed = [[0]*64 for _ in range(64)]
        for r in range(8):
            for c in range(8):
                blk = deshuffled[r][c]
                for rr in range(8):
                    for cc in range(8):
                        reconstructed[r*8+rr][c*8+cc] = blk[rr][cc]

        for rr in range(64):
            final_img[bi+rr][bj:bj+64] = reconstructed[rr]

# -------------------------------------------------
# SAVE OUTPUT IMAGE
# -------------------------------------------------
out_img = Image.new("L", (w, h))
out_img.putdata([px for row in final_img for px in row])
out_img.save("embedded_outputnew2boat.tif")

print("\n✅ Embedding + reverse Sudoku completed successfully.")
