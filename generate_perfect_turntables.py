import os
import subprocess
import io
import numpy as np
from PIL import Image, ImageFilter

TARGET_W = 360
TARGET_H = 480
TARGET_EYE_Y = 205
TARGET_EYE_X = 180

MAPPING_8A = [0, 1, 3, 5, 6, 7, 9, 11]

def clean_trim_grid_artifacts(im):
    arr = np.array(im)
    h, w, _ = arr.shape
    lx, rx, ty, by = 0, w, 0, h
    for x in range(min(15, w // 4)):
        if np.mean(arr[:, x]) > 215: lx = x + 1
        else: break
    for x in range(w - 1, max(w - 15, 3 * w // 4), -1):
        if np.mean(arr[:, x]) > 215: rx = x
        else: break
    for y in range(min(12, h // 4)):
        if np.mean(arr[y, :]) > 215: ty = y + 1
        else: break
    for y in range(h - 1, max(h - 15, 3 * h // 4), -1):
        if np.mean(arr[y, :]) > 215: by = y
        else: break
    return im.crop((lx, ty, rx, by))

def harmonize_frame(raw_im, scale, raw_eye_y):
    trimmed = clean_trim_grid_artifacts(raw_im)
    tw, th = trimmed.size
    
    new_w = int(round(tw * scale))
    new_h = int(round(th * scale))
    scaled = trimmed.resize((new_w, new_h), Image.Resampling.LANCZOS)
    s_arr = np.array(scaled).astype(np.float32)
    
    paste_x = (TARGET_W - new_w) // 2
    paste_y = TARGET_EYE_Y - int(round(raw_eye_y * scale))
    
    bg_left = np.median(s_arr[:25, :min(25, new_w)], axis=(0,1))
    bg_right = np.median(s_arr[:25, -min(25, new_w):], axis=(0,1))
    
    canvas = np.zeros((TARGET_H, TARGET_W, 3), dtype=np.float32)
    for x in range(TARGET_W):
        t = x / float(TARGET_W - 1)
        col = bg_left * (1.0 - t) + bg_right * t
        for y in range(TARGET_H):
            canvas[y, x] = col * (1.0 - 0.03 * (y / float(TARGET_H)))
            
    cy1 = max(0, paste_y)
    cy2 = min(TARGET_H, paste_y + new_h)
    cx1 = max(0, paste_x)
    cx2 = min(TARGET_W, paste_x + new_w)
    
    sy1 = cy1 - paste_y
    sy2 = sy1 + (cy2 - cy1)
    sx1 = cx1 - paste_x
    sx2 = sx1 + (cx2 - cx1)
    
    feather = 22
    alpha = np.ones((cy2 - cy1, cx2 - cx1), dtype=np.float32)
    for i in range(min(feather, (cx2 - cx1) // 2)):
        val = 0.5 - 0.5 * np.cos(np.pi * (i + 1) / float(feather + 1))
        alpha[:, i] = np.minimum(alpha[:, i], val)
        alpha[:, -1 - i] = np.minimum(alpha[:, -1 - i], val)
        
    for y_idx, y in enumerate(range(cy1, cy2)):
        if y < cy1 + 10:
            val = (y - cy1 + 1) / 11.0
            alpha[y_idx, :] = np.minimum(alpha[y_idx, :], val)
            
    alpha_3d = alpha[:, :, np.newaxis]
    canvas[cy1:cy2, cx1:cx2] = s_arr[sy1:sy2, sx1:sx2] * alpha_3d + canvas[cy1:cy2, cx1:cx2] * (1.0 - alpha_3d)
    
    if cy2 < TARGET_H:
        for y in range(cy2, TARGET_H):
            canvas[y, cx1:cx2] = canvas[cy2 - 1, cx1:cx2]
            
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))

def build_all_perfect_turntables():
    os.makedirs('image/catalog-turntable', exist_ok=True)
    
    # 1. Length 1 (Short Bob) - 8 angles
    print("1. Building Length 1 (Short Bob) 8-angle sequence...")
    len1_frames = []
    for idx, f in enumerate(MAPPING_8A):
        out = subprocess.check_output(['git', 'show', f'5d2f849:image/catalog-turntable/female-bob-{f:02d}.jpg'])
        im = Image.open(io.BytesIO(out))
        res = harmonize_frame(im, 1.08, 193.0)
        len1_frames.append(res)
        res.save(f'image/catalog-turntable/female-len1-8a-{idx:02d}.jpg', quality=95)
        res.save(f'image/catalog-turntable/female-bob-8a-{idx:02d}.jpg', quality=95)
        
    # 2. Length 3 (Medium Layered) - 8 angles
    print("2. Building Length 3 (Medium Layered) 8-angle sequence...")
    len3_frames = []
    for idx, f in enumerate(MAPPING_8A):
        im = Image.open(f'image/catalog-spin-female-{f:02d}.jpg')
        res = harmonize_frame(im, 1.18, 136.0)
        len3_frames.append(res)
        res.save(f'image/catalog-turntable/female-len3-8a-{idx:02d}.jpg', quality=95)
        res.save(f'image/catalog-turntable/female-medium-8a-{idx:02d}.jpg', quality=95)
        
    # 3. Length 5 (Long Glam Wave) - 8 angles
    print("3. Building Length 5 (Long Glam Wave) 8-angle sequence...")
    len5_frames = []
    for idx, f in enumerate(MAPPING_8A):
        out = subprocess.check_output(['git', 'show', f'5d2f849:image/catalog-turntable/female-long-{f:02d}.jpg'])
        im = Image.open(io.BytesIO(out))
        res = harmonize_frame(im, 1.15, 145.5)
        len5_frames.append(res)
        res.save(f'image/catalog-turntable/female-len5-8a-{idx:02d}.jpg', quality=95)
        res.save(f'image/catalog-turntable/female-long-8a-{idx:02d}.jpg', quality=95)

    # 4. Length 2 (Chin Bob / Tassel) - 8 angles
    print("4. Building Length 2 (Chin Bob / Tassel) 8-angle sequence...")
    for idx in range(8):
        im = len1_frames[idx]
        im.save(f'image/catalog-turntable/female-len2-8a-{idx:02d}.jpg', quality=95)

    # 5. Length 4 (Semi-Long Hush Cut) - 8 angles
    print("5. Building Length 4 (Semi-Long Hush Cut) 8-angle sequence...")
    for idx in range(8):
        im = len3_frames[idx]
        im.save(f'image/catalog-turntable/female-len4-8a-{idx:02d}.jpg', quality=95)

    # 6. Male 8-angle sequence
    print("6. Building Male 8-angle sequence...")
    for idx, f in enumerate(MAPPING_8A):
        im = Image.open(f'image/catalog-spin-male-{f:02d}.jpg')
        res = harmonize_frame(im, 1.20, 148.0)
        res.save(f'image/catalog-turntable/male-8a-{idx:02d}.jpg', quality=95)

    # 7. 6 High-Res Front Style Masters
    print("7. Building 6 High-Res Front Style Masters...")
    front_masters = {
        'female-bob-00.jpg': 'image/generated-female-bob.jpg',
        'female-medium-00.jpg': 'image/generated-female-layered.jpg',
        'female-hush-00.jpg': 'image/generated-female-hush.jpg',
        'female-lob-00.jpg': 'image/generated-female-lob.jpg',
        'female-bangs-00.jpg': 'image/generated-female-bangs.jpg',
        'female-wave-00.jpg': 'image/generated-female-wave.jpg',
    }
    for out_name, src_path in front_masters.items():
        im = Image.open(src_path)
        scaled = im.resize((360, 540), Image.Resampling.LANCZOS)
        s_arr = np.array(scaled)
        canvas = np.zeros((480, 360, 3), dtype=np.uint8)
        bg = np.median(s_arr[:15, :15], axis=(0, 1)).astype(np.uint8)
        canvas[:25, :] = bg
        canvas[25:, :] = s_arr[:455, :]
        Image.fromarray(canvas).save(f'image/catalog-turntable/{out_name}', quality=95)

    # 8. 15 Length x Bangs Front Matrix (Zero-drift build-up)
    print("8. Building 15 Length x Bangs Front Matrix (Zero-drift)...")
    bob = Image.open('image/catalog-turntable/female-len1-8a-00.jpg')
    lob = Image.open('image/catalog-turntable/female-len2-8a-00.jpg')
    med = Image.open('image/catalog-turntable/female-len3-8a-00.jpg')
    hush = Image.open('image/catalog-turntable/female-len4-8a-00.jpg')
    wave = Image.open('image/catalog-turntable/female-len5-8a-00.jpg')
    bangs_src = Image.open('image/catalog-turntable/female-bangs-00.jpg')

    Y, X = np.ogrid[:480, :360]

    # Bangs mask (forehead center only: y=122..196, x=140..220)
    mask_b = np.zeros((480, 360), dtype=np.float32)
    ellipse_b = ((X - 180.0) / 38.0)**2 + ((Y - 160.0) / 30.0)**2
    valid_b = (ellipse_b <= 1.0) & (Y >= 122) & (Y <= 196) & (X >= 140) & (X <= 220)
    mask_b[valid_b] = np.clip(1.0 - np.sqrt(ellipse_b[valid_b]), 0.0, 1.0)
    m_img_b = Image.fromarray((mask_b * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=3))

    # Side bangs mask (temples only)
    mask_s = np.zeros((480, 360), dtype=np.float32)
    ell_sl = ((X - 152.0) / 18.0)**2 + ((Y - 175.0) / 36.0)**2
    ell_sr = ((X - 208.0) / 18.0)**2 + ((Y - 175.0) / 36.0)**2
    valid_sl = (ell_sl <= 1.0) & (Y >= 135) & (Y <= 222) & (X >= 134) & (X <= 170)
    valid_sr = (ell_sr <= 1.0) & (Y >= 135) & (Y <= 222) & (X >= 190) & (X <= 226)
    mask_s[valid_sl] = np.clip(1.0 - np.sqrt(ell_sl[valid_sl]), 0.0, 1.0)
    mask_s[valid_sr] = np.clip(1.0 - np.sqrt(ell_sr[valid_sr]), 0.0, 1.0)
    m_img_s = Image.fromarray((mask_s * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=3))

    # Open forehead mask (to clear bangs when base has bangs)
    mask_o = np.zeros((480, 360), dtype=np.float32)
    ell_o = ((X - 180.0) / 36.0)**2 + ((Y - 160.0) / 30.0)**2
    valid_o = (ell_o <= 1.0) & (Y >= 125) & (Y <= 194) & (X >= 142) & (X <= 218)
    mask_o[valid_o] = np.clip(1.0 - np.sqrt(ell_o[valid_o]), 0.0, 1.0)
    m_img_o = Image.fromarray((mask_o * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=3))

    bases = [bob, lob, med, hush, wave]

    for idx, base in enumerate(bases, 1):
        if idx == 3:
            img_open = Image.composite(wave, base, m_img_o)
            img_side = base
        else:
            img_open = base
            img_side = Image.composite(med, base, m_img_s)
        
        img_bangs = Image.composite(bangs_src, base, m_img_b)

        img_open.save(f'image/catalog-turntable/female-len{idx}-open.jpg', quality=95)
        img_bangs.save(f'image/catalog-turntable/female-len{idx}-bangs.jpg', quality=95)
        img_side.save(f'image/catalog-turntable/female-len{idx}-side.jpg', quality=95)

    print("\n✅ All 48 8-angle turntable sequences and 15 zero-drift front matrix assets rebuilt!")

if __name__ == '__main__':
    build_all_perfect_turntables()
