import os
import subprocess
import io
import numpy as np
from PIL import Image

TARGET_W = 360
TARGET_H = 480
TARGET_EYE_Y = 205
TARGET_EYE_X = 180

def get_raw_git_image(filepath):
    out = subprocess.check_output(['git', 'show', f'5d2f849:{filepath}'])
    return Image.open(io.BytesIO(out))

def clean_trim_white(im):
    arr = np.array(im)
    w, h = im.size
    lx, rx, ty, by = 0, w, 0, h
    # Left
    for x in range(35):
        if np.mean(np.all(arr[:150, x] > 230, axis=-1)) > 0.3:
            lx = x + 1
    if lx > 0: lx += 2
    # Right
    for x in range(w - 1, w - 35, -1):
        if np.mean(np.all(arr[:150, x] > 230, axis=-1)) > 0.3:
            rx = x
    if rx < w: rx -= 2
    # Bottom corners
    for y in range(h - 1, h - 50, -1):
        corner = np.concatenate([arr[y, :40], arr[y, w-40:]], axis=0)
        if np.mean(np.all(corner > 230, axis=-1)) > 0.3:
            by = y
    if by < h: by -= 2
    # Top
    for y in range(25):
        if np.mean(np.all(arr[y, :40] > 230, axis=-1)) > 0.3:
            ty = y + 1
    if ty > 0: ty += 2
    return im.crop((lx, ty, rx, by)), lx, ty

def run_normalization():
    # 1. Normalize the 6 high-res front style images
    # All 6 images have size 384x576, eye_y=192, eye_dist=80
    front_styles = {
        'female-bob-00.jpg': 'image/generated-female-bob.jpg',
        'female-medium-00.jpg': 'image/generated-female-layered.jpg',
        'female-hush-00.jpg': 'image/generated-female-hush.jpg',
        'female-lob-00.jpg': 'image/generated-female-lob.jpg',
        'female-bangs-00.jpg': 'image/generated-female-bangs.jpg',
        'female-wave-00.jpg': 'image/generated-female-wave.jpg',
    }

    print("=== Normalizing Front Style Images ===")
    for out_name, src_path in front_styles.items():
        im = Image.open(src_path)
        # Scaling: 384 -> 360 (scale = 360/384)
        # eye level on scaled image is 192 * (360/384) = 180px
        # to place eye at TARGET_EYE_Y = 205px, paste_y = 25px
        new_w = 360
        new_h = 540
        scaled = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        s_arr = np.array(scaled)
        
        canvas = np.zeros((TARGET_H, TARGET_W, 3), dtype=np.uint8)
        bg = np.median(s_arr[:15, :15], axis=(0, 1)).astype(np.uint8)
        canvas[:25, :] = bg
        canvas[25:, :] = s_arr[:455, :]
        
        out_path = f"image/catalog-turntable/{out_name}"
        res = Image.fromarray(canvas)
        res.save(out_path, quality=95)
        print(f"Saved {out_path} (locked eye_y=205, width=360)")

    # 2. Normalize Turntable Sequences (00..11) for bob, medium, long, male
    profiles_meta = {
        'female-bob': {
            'scale': 1.25874,
            'eye_raw_y': 193.0,
            'ref_front': 'image/catalog-turntable/female-bob-00.jpg'
        },
        'female-medium': {
            'scale': 1.25874,
            'eye_raw_y': 138.5,
            'ref_front': 'image/catalog-turntable/female-medium-00.jpg'
        },
        'female-long': {
            'scale': 1.25874,
            'eye_raw_y': 145.5,
            'ref_front': 'image/catalog-turntable/female-bangs-00.jpg'
        },
        'male': {
            'scale': 1.25874,
            'eye_raw_y': 148.0,
            'ref_front': 'image/catalog-turntable/male-00.jpg'
        }
    }

    # For female-long and male, process frame 00 first so ref_front exists
    for prof in ['female-long', 'male']:
        meta = profiles_meta[prof]
        scale = meta['scale']
        eye_raw_y = meta['eye_raw_y']
        paste_y = TARGET_EYE_Y - int(round(eye_raw_y * scale))
        rel_path = f"image/catalog-turntable/{prof}-00.jpg"
        im = get_raw_git_image(rel_path)
        trimmed, lx, ty = clean_trim_white(im)
        tw, th = trimmed.size
        new_w = int(round(tw * scale))
        new_h = int(round(th * scale))
        scaled = trimmed.resize((new_w, new_h), Image.Resampling.LANCZOS)
        s_arr = np.array(scaled)
        paste_x = (TARGET_W - new_w) // 2
        
        canvas = np.zeros((TARGET_H, TARGET_W, 3), dtype=np.uint8)
        bg = np.median(s_arr[:20, :20], axis=(0, 1)).astype(np.uint8)
        canvas[:, :] = bg
        
        cx1 = max(0, paste_x)
        cx2 = min(TARGET_W, paste_x + new_w)
        cy1 = max(0, paste_y)
        cy2 = min(TARGET_H, paste_y + new_h)
        sx1 = cx1 - paste_x
        sx2 = sx1 + (cx2 - cx1)
        sy1 = cy1 - paste_y
        sy2 = sy1 + (cy2 - cy1)
        canvas[cy1:cy2, cx1:cx2] = s_arr[sy1:sy2, sx1:sx2]
        if cy2 < TARGET_H:
            for y in range(cy2, TARGET_H):
                canvas[y, cx1:cx2] = canvas[cy2 - 1, cx1:cx2]
        Image.fromarray(canvas).save(rel_path, quality=95)

    print("\n=== Normalizing 360 Turntable Sequences with Ref Blend ===")
    for prof, meta in profiles_meta.items():
        scale = meta['scale']
        eye_raw_y = meta['eye_raw_y']
        paste_y = TARGET_EYE_Y - int(round(eye_raw_y * scale))
        ref_im = Image.open(meta['ref_front'])
        ref_canvas_base = np.array(ref_im).astype(float)
        
        for i in range(12):
            if i == 0 and prof in ['female-bob', 'female-medium', 'female-long', 'male']:
                continue
                
            rel_path = f"image/catalog-turntable/{prof}-{i:02d}.jpg"
            im = get_raw_git_image(rel_path)
            trimmed, lx, ty = clean_trim_white(im)
            tw, th = trimmed.size
            
            new_w = int(round(tw * scale))
            new_h = int(round(th * scale))
            scaled = trimmed.resize((new_w, new_h), Image.Resampling.LANCZOS)
            s_arr = np.array(scaled).astype(float)
            
            paste_x = (TARGET_W - new_w) // 2
            canvas = ref_canvas_base.copy()
            
            cx1 = max(0, paste_x)
            cx2 = min(TARGET_W, paste_x + new_w)
            cy1 = max(0, paste_y)
            cy2 = min(TARGET_H, paste_y + new_h)
            
            sx1 = cx1 - paste_x
            sx2 = sx1 + (cx2 - cx1)
            sy1 = cy1 - paste_y
            sy2 = sy1 + (cy2 - cy1)
            
            # Feather alpha mask on left and right borders of model
            feather_len = 12
            alpha_mask = np.ones((new_h, new_w), dtype=float)
            for x in range(min(feather_len, new_w // 2)):
                a = (x + 1) / (feather_len + 1)
                alpha_mask[:, x] = np.minimum(alpha_mask[:, x], a)
                alpha_mask[:, new_w - 1 - x] = np.minimum(alpha_mask[:, new_w - 1 - x], a)
            
            for c in range(3):
                blended = (s_arr[sy1:sy2, sx1:sx2, c] * alpha_mask[sy1:sy2, sx1:sx2] + 
                           canvas[cy1:cy2, cx1:cx2, c] * (1.0 - alpha_mask[sy1:sy2, sx1:sx2]))
                canvas[cy1:cy2, cx1:cx2, c] = blended
            
            # Extend bottom if needed
            if cy2 < TARGET_H:
                for y in range(cy2, TARGET_H):
                    canvas[y, cx1:cx2] = canvas[cy2 - 1, cx1:cx2]
                    
            out_im = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
            out_im.save(rel_path, quality=95)
            print(f"  Processed {rel_path}: {new_w}x{new_h} pasted at ({paste_x}, {paste_y}) with ref_blend")

    # 3. Generate 15 Length x Bangs Matrix Images
    print("\n=== Generating 15 Length x Bangs Matrix Images ===")
    from PIL import ImageFilter
    bob = Image.open('image/catalog-turntable/female-bob-00.jpg')
    lob = Image.open('image/catalog-turntable/female-lob-00.jpg')
    med = Image.open('image/catalog-turntable/female-medium-00.jpg')
    hush = Image.open('image/catalog-turntable/female-hush-00.jpg')
    wave = Image.open('image/catalog-turntable/female-wave-00.jpg')
    bangs_src = Image.open('image/catalog-turntable/female-bangs-00.jpg')

    mask_bangs = Image.new('L', (360, 480), 0)
    m_arr = np.array(mask_bangs)
    Y, X = np.ogrid[:480, :360]
    dist_b = ((X - 180) / 44.0)**2 + ((Y - 155) / 42.0)**2
    valid = (dist_b < 1.0) & (Y < 202) & (Y > 115)
    m_arr[valid] = (255 * (1.0 - dist_b[valid])).astype(np.uint8)
    mask_bangs = Image.fromarray(m_arr).filter(ImageFilter.GaussianBlur(radius=6))

    mask_side = Image.new('L', (360, 480), 0)
    s_arr = np.array(mask_side)
    dist_l = ((X - 155) / 22.0)**2 + ((Y - 170) / 35.0)**2
    dist_r = ((X - 205) / 22.0)**2 + ((Y - 170) / 35.0)**2
    valid_l = (dist_l < 1.0) & (Y < 215) & (Y > 125)
    valid_r = (dist_r < 1.0) & (Y < 215) & (Y > 125)
    s_arr[valid_l] = (255 * (1.0 - dist_l[valid_l])).astype(np.uint8)
    s_arr[valid_r] = (255 * (1.0 - dist_r[valid_r])).astype(np.uint8)
    mask_side = Image.fromarray(s_arr).filter(ImageFilter.GaussianBlur(radius=6))

    # Length 1
    bob.save('image/catalog-turntable/female-len1-open.jpg', quality=95)
    Image.composite(bangs_src, bob, mask_bangs).save('image/catalog-turntable/female-len1-bangs.jpg', quality=95)
    Image.composite(med, bob, mask_side).save('image/catalog-turntable/female-len1-side.jpg', quality=95)
    # Length 2
    lob.save('image/catalog-turntable/female-len2-open.jpg', quality=95)
    Image.composite(bangs_src, lob, mask_bangs).save('image/catalog-turntable/female-len2-bangs.jpg', quality=95)
    Image.composite(med, lob, mask_side).save('image/catalog-turntable/female-len2-side.jpg', quality=95)
    # Length 3
    Image.composite(bob, med, mask_side).save('image/catalog-turntable/female-len3-open.jpg', quality=95)
    Image.composite(bangs_src, med, mask_bangs).save('image/catalog-turntable/female-len3-bangs.jpg', quality=95)
    med.save('image/catalog-turntable/female-len3-side.jpg', quality=95)
    # Length 4
    hush.save('image/catalog-turntable/female-len4-open.jpg', quality=95)
    Image.composite(bangs_src, hush, mask_bangs).save('image/catalog-turntable/female-len4-bangs.jpg', quality=95)
    Image.composite(med, hush, mask_side).save('image/catalog-turntable/female-len4-side.jpg', quality=95)
    # Length 5
    wave.save('image/catalog-turntable/female-len5-open.jpg', quality=95)
    bangs_src.save('image/catalog-turntable/female-len5-bangs.jpg', quality=95)
    Image.composite(med, wave, mask_side).save('image/catalog-turntable/female-len5-side.jpg', quality=95)
    print("  Saved 15 length + bangs matrix images successfully!")

    print("\nAll 360 turntable assets and front styles normalized with identical eye level and head scale!")

if __name__ == '__main__':
    run_normalization()
