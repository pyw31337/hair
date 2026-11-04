#!/usr/bin/env python3
"""
Generate 108 Photorealistic Diagnosis Matrix Images:
3 Textures (straight, wavy, curly)
x 3 Volumes (thin, normal, thick)
x 3 Damages (healthy, colored, bleached)
x 4 Face Shapes (oval, round, square, long)
= 108 Unique High-Resolution Image Files
"""
import os
import cv2
import numpy as np

def build_diagnosis_matrix():
    print("🚀 Starting generation of 108 photorealistic diagnosis matrix images...")
    os.makedirs('image/catalog-turntable', exist_ok=True)

    # Base templates for textures
    # straight: female-lob-00 (sleek straight cut)
    # wavy: female-medium-00 (soft romantic S-wave)
    # curly: female-wave-00 (rich glamorous curl)
    base_templates = {
        'straight': cv2.imread('image/catalog-turntable/female-lob-00.jpg'),
        'wavy': cv2.imread('image/catalog-turntable/female-medium-00.jpg'),
        'curly': cv2.imread('image/catalog-turntable/female-wave-00.jpg')
    }

    Y, X = np.indices((480, 360), dtype=np.float32)

    # Face mask to protect facial features and neck from any deformation
    face_ell = ((X - 180.0) / 52.0)**2 + ((Y - 240.0) / 80.0)**2
    face_weight = np.clip(1.0 - face_ell, 0.0, 1.0)
    face_mask = cv2.GaussianBlur(face_weight, (31, 31), 0)
    face_protected = np.clip(face_mask * 1.5, 0.0, 1.0)

    # Hair mask: area outside face but within head/shoulder silhouette
    hair_weight = np.clip((1.0 - face_protected) * (Y / 380.0), 0.0, 1.0)
    hair_weight[Y > 430] *= 0.1 # Protect white clothing
    hair_weight[Y < 30] = 0

    # Side hair mask: Strictly lateral hair only (X < 120 or X > 240), zero effect on central face
    side_hair_mask = np.clip((np.abs(X - 180.0) - 60.0) / 30.0, 0.0, 1.0) * hair_weight * (1.0 - face_protected)

    textures = ['straight', 'wavy', 'curly']
    volumes = ['thin', 'normal', 'thick']
    damages = ['healthy', 'colored', 'bleached']
    faces = ['oval', 'round', 'square', 'long']

    count = 0

    for tex in textures:
        base_img = base_templates[tex].copy()

        for vol in volumes:
            # 1. Volume Warping: Strictly on outer side hair only, zero facial distortion
            if vol == 'thick':
                # Lateral hair density expansion
                shift_x = np.sin((X - 180.0) / 180.0 * np.pi) * 12.0 * side_hair_mask
                map_x = np.clip(X - shift_x, 0, 359).astype(np.float32)
                vol_img = cv2.remap(base_img, map_x, Y, cv2.INTER_LANCZOS4)
            elif vol == 'thin':
                # Lateral hair density contraction
                shift_x = -np.sin((X - 180.0) / 180.0 * np.pi) * 9.0 * side_hair_mask
                map_x = np.clip(X - shift_x, 0, 359).astype(np.float32)
                vol_img = cv2.remap(base_img, map_x, Y, cv2.INTER_LANCZOS4)
            else: # normal
                vol_img = base_img.copy()

            for dam in damages:
                # 2. Damage Texture & Color Modification
                dam_img = vol_img.astype(np.float32).copy()

                # Get hair region in dam_img
                hair_is_dark = np.clip((130.0 - np.mean(dam_img, axis=-1)) / 70.0, 0.0, 1.0)
                active_hair_mask = hair_weight * hair_is_dark * (1.0 - face_mask)

                if dam == 'healthy':
                    # Rich espresso depth with natural studio hair luster (No artificial forehead lighting)
                    dam_img[:, :, 0] -= active_hair_mask * 10 # Subtle Blue down
                    dam_img[:, :, 1] -= active_hair_mask * 6  # Subtle Green down
                    dam_img[:, :, 2] -= active_hair_mask * 4  # Subtle Red down
                    # Natural wave side gloss only (strictly outside face)
                    side_gloss = np.exp(-((Y - 320.0)**2)/(2*20.0**2)) * np.exp(-((X - 90.0)**2)/(2*25.0**2)) + \
                                 np.exp(-((Y - 320.0)**2)/(2*20.0**2)) * np.exp(-((X - 270.0)**2)/(2*25.0**2))
                    total_gloss = np.clip(side_gloss * 28.0 * active_hair_mask, 0.0, 35.0)
                    dam_img += total_gloss[:, :, None]

                elif dam == 'colored':
                    # Salon warm caramel-brown tone
                    dam_img[:, :, 0] -= active_hair_mask * 18 # Blue down
                    dam_img[:, :, 1] += active_hair_mask * 8  # Green up
                    dam_img[:, :, 2] += active_hair_mask * 28 # Red up

                elif dam == 'bleached':
                    # High-lift bleached blonde tone + Frizzy dry matte texture
                    dam_img[:, :, 0] += active_hair_mask * 45  # Lift Blue
                    dam_img[:, :, 1] += active_hair_mask * 75  # Lift Green
                    dam_img[:, :, 2] += active_hair_mask * 105 # Lift Red (Golden blonde)
                    np.random.seed(42)
                    noise = np.random.normal(0, 15.0, dam_img.shape) * active_hair_mask[:, :, None]
                    dam_img += noise
                    dam_img = dam_img * (1.0 - active_hair_mask[:, :, None] * 0.06)

                dam_img = np.clip(dam_img, 0, 255).astype(np.uint8)

                for face in faces:
                    # 3. Face shape silhouette adaptation
                    out_img = dam_img.copy()

                    if face == 'round':
                        shift_y = np.clip((Y - 240.0)/60.0, 0.0, 1.0) * np.exp(-((X - 180.0)**2)/(2*55.0**2)) * 8.0 * (1.0 - face_protected)
                        map_y_round = np.clip(Y - shift_y, 0, 479).astype(np.float32)
                        out_img = cv2.remap(out_img, X, map_y_round, cv2.INTER_LANCZOS4)
                    elif face == 'square':
                        jaw_in = np.exp(-((Y - 305.0)**2)/(2*25.0**2)) * -np.sin((X - 180.0)/180.0 * np.pi) * 8.0 * (1.0 - face_protected)
                        map_x_square = np.clip(X - jaw_in, 0, 359).astype(np.float32)
                        out_img = cv2.remap(out_img, map_x_square, Y, cv2.INTER_LANCZOS4)
                    elif face == 'long':
                        ear_out = np.exp(-((Y - 240.0)**2)/(2*30.0**2)) * np.sin((X - 180.0)/180.0 * np.pi) * 9.0 * (1.0 - face_protected)
                        map_x_long = np.clip(X - ear_out, 0, 359).astype(np.float32)
                        out_img = cv2.remap(out_img, map_x_long, Y, cv2.INTER_LANCZOS4)

                    filename = f"image/catalog-turntable/diag-{tex}-{vol}-{dam}-{face}.jpg"
                    cv2.imwrite(filename, out_img, [cv2.IMWRITE_JPEG_QUALITY, 94])
                    count += 1

    print(f"🎉 Successfully generated {count} photorealistic diagnosis matrix images!")

if __name__ == '__main__':
    build_diagnosis_matrix()
