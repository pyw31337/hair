import os
import io
import subprocess
import numpy as np
from PIL import Image

TARGET_W = 360
TARGET_H = 480
TARGET_HAIR_TOP = 28

PROFILES = ['female-bob', 'female-medium', 'female-long', 'male']

def get_raw_image(filepath):
    # Fetch original uncorrupted source from git commit 5d2f849
    try:
        out = subprocess.check_output(['git', 'show', f'5d2f849:{filepath}'])
        return Image.open(io.BytesIO(out))
    except Exception:
        return Image.open(filepath)

for prof in PROFILES:
    print(f"Processing profile: {prof}...")
    for i in range(12):
        filepath = f"image/catalog-turntable/{prof}-{i:02d}.jpg"
        im = get_raw_image(filepath)
        arr = np.array(im)
        w, h = im.size

        # 1. Detect and cleanly trim all white borders:
        # Left white stripe detection
        lx = 0
        for x in range(35):
            if np.mean(np.all(arr[:150, x] > 230, axis=-1)) > 0.3:
                lx = x + 1
        if lx > 0:
            lx += 2

        # Right white stripe detection
        rx = w
        for x in range(w - 1, w - 35, -1):
            if np.mean(np.all(arr[:150, x] > 230, axis=-1)) > 0.3:
                rx = x
        if rx < w:
            rx -= 2

        # Bottom white stripe/label detection (corners)
        by = h
        for y in range(h - 1, h - 50, -1):
            corner_px = np.concatenate([arr[y, :40], arr[y, w-40:]], axis=0)
            if np.mean(np.all(corner_px > 230, axis=-1)) > 0.3:
                by = y
        if by < h:
            by -= 2

        # Top white stripe detection
        ty = 0
        for y in range(25):
            if np.mean(np.all(arr[y, :40] > 230, axis=-1)) > 0.3:
                ty = y + 1
        if ty > 0:
            ty += 2

        cropped = im.crop((lx, ty, rx, by))
        cw, ch = cropped.size
        c_arr = np.array(cropped)
        bg = np.median(c_arr[:20, :20], axis=(0, 1))

        # Detect top of hair along center column
        ht = 0
        for y in range(ch):
            strip = c_arr[y, max(0, cw//2 - 25):min(cw, cw//2 + 25)]
            if np.mean(np.linalg.norm(strip.astype(float) - bg, axis=-1)) > 25:
                ht = y
                break

        # 2. Scale width to TARGET_W (360px) to completely eliminate any left/right empty bars
        scale = TARGET_W / cw
        new_w = TARGET_W
        new_h = int(ch * scale)
        scaled = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
        s_arr = np.array(scaled)

        # 3. Position head locked at TARGET_HAIR_TOP (28px)
        scaled_ht = int(ht * scale)
        paste_y = TARGET_HAIR_TOP - scaled_ht

        # 4. Canvas creation and seamless edge extension
        canvas_arr = np.zeros((TARGET_H, TARGET_W, 3), dtype=np.uint8)
        canvas_arr[:, :] = bg.astype(np.uint8)

        y1 = max(0, paste_y)
        y2 = min(TARGET_H, paste_y + new_h)
        sy1 = y1 - paste_y
        sy2 = sy1 + (y2 - y1)

        canvas_arr[y1:y2, 0:TARGET_W] = s_arr[sy1:sy2, 0:TARGET_W]

        # Extend top row of studio background upward if needed
        if y1 > 0:
            for y in range(y1):
                canvas_arr[y, :] = canvas_arr[y1, :]

        # Extend bottom row (shirt & background) downward if needed
        if y2 < TARGET_H:
            for y in range(y2, TARGET_H):
                canvas_arr[y, :] = canvas_arr[y2 - 1, :]

        # Save normalized image
        res_im = Image.fromarray(canvas_arr)
        res_im.save(filepath, quality=94)
        print(f"  Processed {prof}-{i:02d}: {cw}x{ch} -> {TARGET_W}x{TARGET_H}, hair_top locked at {TARGET_HAIR_TOP}px")

print("All 48 turntable images successfully normalized and saved without white bars!")
