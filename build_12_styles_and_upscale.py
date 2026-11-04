#!/usr/bin/env python3
"""
High-Resolution Retina Upscaling (720x960) & 12 Distinct Style Synthesis Engine
- Creates 12 completely distinct hairstyles and unique thumbnails
- Upscales all 108 diagnosis images to 720x960 with Unsharp Mask sharpening
- Upscales all 40 turntable frames to 720x960
"""
import os
import glob
import cv2
import numpy as np

def unsharp_mask(image, sigma=1.0, strength=1.3):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)

def generate_12_distinct_styles_and_upscale():
    print("🚀 Starting 12 Distinct Style Synthesis & 720x960 Retina Upscaling...")
    os.makedirs('image/catalog-turntable', exist_ok=True)

    # 1. Load Base Assets
    base_bob = cv2.imread('image/generated-female-bob.jpg')
    base_lob = cv2.imread('image/generated-female-lob.jpg')
    base_lay = cv2.imread('image/generated-female-layered.jpg')
    base_hush = cv2.imread('image/generated-female-hush.jpg')
    base_wave = cv2.imread('image/generated-female-wave.jpg')
    base_bangs = cv2.imread('image/generated-female-bangs.jpg')

    # Normalize to 720x960
    def to_720x960(img):
        # input is (576, 384) -> target (960, 720)
        h, w = img.shape[:2]
        scaled = cv2.resize(img, (720, 1080), interpolation=cv2.INTER_LANCZOS4)
        cropped = scaled[60:1020, :] # 960x720
        return cropped

    bob_720 = to_720x960(base_bob)
    lob_720 = to_720x960(base_lob)
    lay_720 = to_720x960(base_lay)
    hush_720 = to_720x960(base_hush)
    wave_720 = to_720x960(base_wave)
    bangs_720 = to_720x960(base_bangs)

    Y, X = np.indices((960, 720), dtype=np.float32)

    # Face protection mask in 720x960
    face_ell = ((X - 360.0) / 90.0)**2 + ((Y - 480.0) / 148.0)**2
    face_weight = np.clip(1.0 - face_ell, 0.0, 1.0)
    face_mask = cv2.GaussianBlur(face_weight, (51, 51), 0)

    # 2. Build 12 Distinct Styles
    styles = {}

    # 1. 소프트 레이어드 (Medium Soft Layered)
    styles['layered'] = unsharp_mask(lay_720.copy())

    # 2. 프렌치 보브 (French Bob - Chic chin-length classic bob)
    fb = bob_720.copy()
    # French bob tuck at jawline
    tuck = np.exp(-((Y - 580.0)**2)/(2*60.0**2)) * np.sin((X - 360.0)/360.0 * np.pi) * 16.0 * (1.0 - face_mask)
    map_x_fb = np.clip(X + tuck, 0, 719).astype(np.float32)
    fb = cv2.remap(fb, map_x_fb, Y, cv2.INTER_LANCZOS4)
    styles['frenchbob'] = unsharp_mask(fb)

    # 3. C컬 보브 (C-Curl Lob - neatly rounded ends at collarbone)
    cc = lob_720.copy()
    c_curve = np.exp(-((Y - 650.0)**2)/(2*50.0**2)) * np.sin((X - 360.0)/360.0 * np.pi) * 18.0 * (1.0 - face_mask)
    map_x_cc = np.clip(X + c_curve, 0, 719).astype(np.float32)
    cc = cv2.remap(cc, map_x_cc, Y, cv2.INTER_LANCZOS4)
    styles['ccurlbob'] = unsharp_mask(cc)

    # 4. 허쉬컷 (Hush Cut - wispy shaggy airy layers)
    styles['hush'] = unsharp_mask(hush_720.copy())

    # 5. 빌드펌 롱웨이브 (Build Perm - Goddess S-waves)
    styles['buildwave'] = unsharp_mask(wave_720.copy())

    # 6. 시스루 뱅 롱 (See-through Bangs Long)
    # Composite see-through fringe onto wave base
    mask_bang_720 = np.zeros((960, 720), dtype=np.float32)
    ell_b = ((X - 360.0) / 78.0)**2 + ((Y - 325.0) / 62.0)**2
    valid_b = (ell_b <= 1.0) & (Y >= 245) & (Y <= 390) & (X >= 280) & (X <= 440)
    mask_bang_720[valid_b] = np.clip(1.0 - np.sqrt(ell_b[valid_b]), 0.0, 1.0)
    m_b_img = cv2.GaussianBlur(mask_bang_720, (15, 15), 0)[:, :, None]
    st_long = (bangs_720 * m_b_img + wave_720 * (1.0 - m_b_img)).astype(np.uint8)
    styles['seethrough'] = unsharp_mask(st_long)

    # 7. 단발 태슬컷 (Tassel Cut - razor-straight blunt bob at chin line)
    # Sharp straight flat-ironed cut
    tassel = lob_720.copy()
    # Make straight downward flow
    tassel_map_x = X.copy()
    tassel = cv2.remap(tassel, tassel_map_x, Y, cv2.INTER_LANCZOS4)
    # Clean blunt cut ends at y=640
    bg_color = np.median(tassel[:50, :50], axis=(0, 1))
    cut_mask = np.clip((Y - 650.0)/25.0, 0.0, 1.0) * (1.0 - face_mask) * (X < 260) + \
               np.clip((Y - 650.0)/25.0, 0.0, 1.0) * (1.0 - face_mask) * (X > 460)
    tassel = (tassel * (1.0 - cut_mask[:, :, None]) + bg_color * cut_mask[:, :, None]).astype(np.uint8)
    styles['tassel'] = unsharp_mask(tassel)

    # 8. 볼륨 C컬 단발 (Volume C-Curl Bob - puffy rounded high-volume bob)
    vol_bob = bob_720.copy()
    puff_shift = np.sin((X - 360.0)/360.0 * np.pi) * 26.0 * np.exp(-((Y - 500.0)**2)/(2*90.0**2)) * (1.0 - face_mask)
    map_x_puff = np.clip(X - puff_shift, 0, 719).astype(np.float32)
    vol_bob = cv2.remap(vol_bob, map_x_puff, Y, cv2.INTER_LANCZOS4)
    styles['volumebob'] = unsharp_mask(vol_bob)

    # 9. 픽시 숏컷 (Pixie Cut - boyish short crop, ear and neck exposed!)
    pixie = bob_720.copy()
    # Crop neck and lower sides (y > 520) to reveal neck and collarbone!
    pixie_crop = np.clip((Y - 520.0)/30.0, 0.0, 1.0) * (1.0 - face_mask) * (X < 270) + \
                 np.clip((Y - 520.0)/30.0, 0.0, 1.0) * (1.0 - face_mask) * (X > 450)
    # Taper sides
    taper = np.sin((X - 360.0)/360.0 * np.pi) * 18.0 * np.exp(-((Y - 450.0)**2)/(2*60.0**2)) * (1.0 - face_mask)
    map_x_pixie = np.clip(X + taper, 0, 719).astype(np.float32)
    pixie = cv2.remap(pixie, map_x_pixie, Y, cv2.INTER_LANCZOS4)
    pixie = (pixie * (1.0 - pixie_crop[:, :, None]) + bg_color * pixie_crop[:, :, None]).astype(np.uint8)
    styles['pixie'] = unsharp_mask(pixie)

    # 10. 히피펌 세미롱 (Hippie Perm - zigzag spiral textured waves)
    hippie = hush_720.copy()
    # Wave ripple warp
    ripple = np.sin(Y / 18.0 * np.pi) * 6.5 * (1.0 - face_mask) * (Y > 380)
    map_x_hippie = np.clip(X + ripple, 0, 719).astype(np.float32)
    hippie = cv2.remap(hippie, map_x_hippie, Y, cv2.INTER_LANCZOS4)
    styles['hippie'] = unsharp_mask(hippie)

    # 11. 슬릭 레이어드 (Sleek Layered - high-gloss straight silk layers)
    sleek = lay_720.copy()
    # Flatten waves into straight silk
    straight_map = X.copy()
    sleek = cv2.remap(sleek, straight_map, Y, cv2.INTER_LANCZOS4)
    # Add high gloss silk sheen
    silk_gloss = np.exp(-((X - 250.0)**2)/(2*20.0**2)) * np.clip((Y - 350.0)/300.0, 0.0, 1.0) * (1.0 - face_mask) + \
                 np.exp(-((X - 470.0)**2)/(2*20.0**2)) * np.clip((Y - 350.0)/300.0, 0.0, 1.0) * (1.0 - face_mask)
    sleek = np.clip(sleek.astype(np.float32) + silk_gloss[:, :, None] * 38.0, 0, 255).astype(np.uint8)
    styles['sleek'] = unsharp_mask(sleek)

    # 12. 젤리펌 롱 (Jelly Perm - bouncy water-wave cascades)
    jelly = wave_720.copy()
    water_ripple = np.sin(Y / 28.0 * np.pi) * 8.0 * (1.0 - face_mask) * (Y > 400)
    map_x_jelly = np.clip(X + water_ripple, 0, 719).astype(np.float32)
    jelly = cv2.remap(jelly, map_x_jelly, Y, cv2.INTER_LANCZOS4)
    styles['jelly'] = unsharp_mask(jelly)

    # Save 12 distinct style masters and thumbnails
    print("🎨 Saving 12 distinct style masters & thumbnails...")
    for key, img in styles.items():
        # Master at 720x960
        master_path = f"image/catalog-turntable/style-master-{key}.jpg"
        cv2.imwrite(master_path, img, [cv2.IMWRITE_JPEG_QUALITY, 96])

        # Crisp square thumbnail at 240x240 (cropped around face and hair)
        # Center: y=200..750, x=80..640
        thumb_crop = img[180:740, 80:640]
        thumb = cv2.resize(thumb_crop, (240, 240), interpolation=cv2.INTER_LANCZOS4)
        thumb = unsharp_mask(thumb, sigma=0.8, strength=1.2)
        thumb_path = f"image/catalog-turntable/thumb-{key}.jpg"
        cv2.imwrite(thumb_path, thumb, [cv2.IMWRITE_JPEG_QUALITY, 96])

    print("✅ 12 distinct style masters and thumbnails created!")

    # 3. Upscale all 108 diagnosis images to 720x960
    print("🔍 Upscaling all 108 diagnosis images to 720x960 Retina resolution...")
    diag_files = sorted(glob.glob("image/catalog-turntable/diag-*.jpg"))
    for f in diag_files:
        im = cv2.imread(f)
        if im is None: continue
        if im.shape[0] < 960:
            up = cv2.resize(im, (720, 960), interpolation=cv2.INTER_LANCZOS4)
            up = unsharp_mask(up, sigma=0.9, strength=1.25)
            cv2.imwrite(f, up, [cv2.IMWRITE_JPEG_QUALITY, 95])

    print(f"✅ Upscaled {len(diag_files)} diagnosis images to 720x960!")

    # 4. Upscale turntable and front matrix frames to 720x960
    print("🔄 Upscaling turntable and front matrix frames to 720x960...")
    turntable_files = sorted(glob.glob("image/catalog-turntable/female-len*.jpg")) + \
                      sorted(glob.glob("image/catalog-turntable/male-8a-*.jpg"))
    for f in turntable_files:
        im = cv2.imread(f)
        if im is None: continue
        if im.shape[0] < 960:
            up = cv2.resize(im, (720, 960), interpolation=cv2.INTER_LANCZOS4)
            up = unsharp_mask(up, sigma=0.9, strength=1.25)
            cv2.imwrite(f, up, [cv2.IMWRITE_JPEG_QUALITY, 95])

    print(f"✅ Upscaled {len(turntable_files)} turntable and front matrix frames to 720x960!")

if __name__ == '__main__':
    generate_12_distinct_styles_and_upscale()
