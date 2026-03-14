import rasterio
import numpy as np
import json
import os
from PIL import Image

# 1. Cấu hình đường dẫn
tif_path = r"D:\FPTU\AIS8\TEST\Task1\data\20190920_025411_0e26_3B_AnalyticMS_SR_clip.tif"
stac_json_path = r"D:\FPTU\AIS8\TEST\Task1\data\20190920_025411_0e26.json"
output_dir = r"D:\FPTU\AIS8\TEST\Task1\output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Xử lý STAC JSON
with open(stac_json_path, 'r', encoding='utf-8') as f:
    stac_data = json.load(f)

asset_key = "20190920_025411_0e26_3B_AnalyticMS_SR_clip_tif"
bands_metadata = stac_data['assets'][asset_key]['eo:bands']
band_map = {b['common_name']: i + 1 for i, b in enumerate(bands_metadata)}

# 3. Hàm xử lý Tổ hợp màu tự nhiên (True Color)
def smart_stretch(band_data):
    valid_pixels = band_data[band_data > 0]
    if valid_pixels.size == 0: return band_data.astype(np.uint8)
    p2, p98 = np.percentile(valid_pixels, (2, 98))
    band_rescaled = np.clip(band_data, p2, p98)
    return ((band_rescaled - p2) / (p98 - p2) * 255).astype(np.uint8)

with rasterio.open(tif_path) as src:
    # Đọc kênh màu tự nhiên (Red-Green-Blue)
    r = smart_stretch(src.read(band_map['red']))
    g = smart_stretch(src.read(band_map['green']))
    b = smart_stretch(src.read(band_map['blue']))
    
    rgb_stack = np.stack((r, g, b), axis=0)
    
    # Giữ nguyên CRS cho file .tif
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff", "dtype": "uint8", "count": 3, "nodata": 0})

# --- XUẤT 3 ĐẦU RA THEO YÊU CẦU ---

# ĐẦU RA 1: Ảnh .tif (giữ nguyên CRS)
output_tif = os.path.join(output_dir, "task1_true_color_geo.tif")
with rasterio.open(output_tif, "w", **out_meta) as dst:
    dst.write(rgb_stack)

# ĐẦU RA 2: Ảnh .png (để xem/nộp báo cáo)
output_png = os.path.join(output_dir, "task1_visual_preview.png")
img_preview = Image.fromarray(np.transpose(rgb_stack, (1, 2, 0)))
img_preview.save(output_png)

# ĐẦU RA 3 (Gợi ý): Ảnh tổ hợp màu tự nhiên đã tăng cường độ tương phản (Enhanced)
# Thường giảng viên muốn thấy sự khác biệt, mình sẽ xuất thêm bản Brightened
output_enhanced = os.path.join(output_dir, "task1_natural_color_enhanced.png")
enhanced_img = Image.fromarray(np.transpose(rgb_stack, (1, 2, 0)))
import PIL.ImageEnhance as enhance
enhanced_img = enhance.Contrast(enhanced_img).enhance(1.2)
enhanced_img.save(output_enhanced)

print(f"✅ Hoàn thành! Đã xuất các file tại: {output_dir}")