import os
import glob
import numpy as np
from PIL import Image, ImageFilter

TARGET_W = 360
TARGET_H = 480
TARGET_HAIR_TOP = 42

PROFILES = {
    "female-bob": {
        "scale": 0.955,
        "default_bg": (194, 182, 182),
        "is_male": False
    },
    "female-medium": {
        "scale": 1.092,
        "default_bg": (202, 188, 188),
        "is_male": False
    },
    "female-long": {
        "scale": 1.180,
        "default_bg": (189, 175, 174),
        "is_male": False
    },
    "male": {
        "scale": 0.931,
        "default_bg": (170, 182, 198),
        "is_male": True
    }
}

def detect_frame_hair_top(arr, bg, center_x):
    h, w, _ = arr.shape
    for y in range(h):
        # sample a 20px wide column in the center
        strip = arr[y, max(0, center_x - 10) : min(w, center_x + 10)]
        diffs = np.linalg.norm(strip.astype(float) - bg, axis=1)
        if np.mean(diffs) > 22:
            return y
    return 0

for prof, cfg in PROFILES.items():
    print(f"Processing profile: {prof}...")
    files = sorted(glob.glob(f"image/catalog-turntable/{prof}-*.jpg"))
    raw_hair_tops = []
    frames_data = []

    for f in files:
        img = Image.open(f)
        w, h = img.size
        # Trim 3px from each side to remove any white border lines
        img_trimmed = img.crop((3, 3, w - 3, h - 3))
        tw, th = img_trimmed.size
        arr = np.array(img_trimmed)
        
        # Sample background from top corners
        bg_sample = np.mean([arr[0, 0], arr[0, -1], arr[5, 0], arr[5, -1]], axis=0)
        
        # Detect hair top
        center_x = tw // 2
        ht = detect_frame_hair_top(arr, bg_sample, center_x)
        raw_hair_tops.append(ht)
        frames_data.append((f, img_trimmed, bg_sample, ht))

    # Calculate a smooth target y-offset for each frame
    # We want the head top to align to TARGET_HAIR_TOP consistently
    smooth_hair_tops = []
    n = len(raw_hair_tops)
    for i in range(n):
        # circular 3-frame average
        prev_i = (i - 1) % n
        next_i = (i + 1) % n
        val = (raw_hair_tops[prev_i] + raw_hair_tops[i]*2 + raw_hair_tops[next_i]) / 4.0
        smooth_hair_tops.append(val)

    # Process and save each frame
    for i, (filepath, img_trimmed, bg_sample, raw_ht) in enumerate(frames_data):
        scale = cfg["scale"]
        new_w = int(img_trimmed.width * scale)
        new_h = int(img_trimmed.height * scale)
        
        img_scaled = img_trimmed.resize((new_w, new_h), Image.Resampling.LANCZOS)
        arr_scaled = np.array(img_scaled)
        
        # Calculate paste position
        scaled_hair_top = int(smooth_hair_tops[i] * scale)
        paste_y = TARGET_HAIR_TOP - scaled_hair_top
        paste_x = (TARGET_W - new_w) // 2

        # Create target canvas filled with seamless studio background
        canvas = Image.new("RGB", (TARGET_W, TARGET_H), tuple(int(c) for c in bg_sample[:3]))
        
        # Paste scaled subject
        canvas.paste(img_scaled, (paste_x, paste_y))
        
        # If subject bottom doesn't reach TARGET_H, extend the bottom edge smoothly
        subj_bottom = paste_y + new_h
        if subj_bottom < TARGET_H:
            # take bottom 2 rows of subject and stretch down
            bottom_strip = img_scaled.crop((0, new_h - 2, new_w, new_h))
            bottom_stretched = bottom_strip.resize((new_w, TARGET_H - subj_bottom + 2))
            canvas.paste(bottom_stretched, (paste_x, subj_bottom - 2))
            
        # Also ensure side edges blend seamlessly if paste_x > 0
        canvas_arr = np.array(canvas)
        # Check and clean any remaining 1px edge artifacts
        canvas_arr[0, :] = bg_sample[:3]
        canvas_arr[:, 0] = bg_sample[:3]
        canvas_arr[:, -1] = bg_sample[:3]
        
        final_img = Image.fromarray(canvas_arr)
        final_img.save(filepath, quality=92)
        print(f"  Saved {os.path.basename(filepath)}: 360x480, hair_top aligned to ~{TARGET_HAIR_TOP}px")

print("All 48 turntable images successfully normalized!")
