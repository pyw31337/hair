#!/usr/bin/env python3
"""Preview matrix pipeline: resize raw renders to 600x800 and extract hair-only alpha masks (-mask.png) and person/foreground masks (-fg.png, used by volume preview)
with MediaPipe selfie_multiclass (class 1 = hair). Masks drive hair-only color tinting in the app.
Usage: python build_masks.py <raw_dir> <out_dir> <model.tflite>"""
import sys, glob, os, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
raw, out, model = sys.argv[1:4]
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=model), output_confidence_masks=True))
for f in sorted(glob.glob(os.path.join(raw, '*.jpg'))):
    name = os.path.basename(f)[:-4]
    img = cv2.resize(cv2.imread(f), (600, 800), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f'{out}/{name}.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 86])
    res = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))
    hair = res.confidence_masks[1].numpy_view()
    m = (np.clip(cv2.GaussianBlur(hair, (0, 0), 1.5), 0, 1) * 255).astype(np.uint8)
    cv2.imwrite(f'{out}/{name}-mask.png', m)
    fg = 1 - res.confidence_masks[0].numpy_view()
    cv2.imwrite(f'{out}/{name}-fg.png', (np.clip(cv2.GaussianBlur(fg, (0, 0), 1.5), 0, 1) * 255).astype(np.uint8))
    print(name, 'hair px', int((m > 128).sum()))
