import rasterio
import json
import cv2
import numpy as np
import os
from ultralytics import YOLO
from sahi.predict import get_sliced_prediction
from sahi.models.ultralytics import UltralyticsDetectionModel


MODEL_PATH = r'D:\FPTU\AIS8\TEST\Task2\runs\train_ship\weights\best.pt'
IMAGE_PATH = r'D:\FPTU\AIS8\TEST\Task2\data_test\intest\AOI_02.tif'
OUTPUT_GEOJSON = r'D:\FPTU\AIS8\TEST\Task2\data_test\outtest\results.geojson'
OUTPUT_IMAGE = r'D:\FPTU\AIS8\TEST\Task2\data_test\outtest\result_visualized.png'


print("Khởi tạo mô hình YOLOv8-OBB với ngưỡng 70%...")
detection_model = UltralyticsDetectionModel(
    model_path=MODEL_PATH,
    confidence_threshold=0.7,  
    device='cpu'
)

def run_task2():
    print("Đang tiến hành dự đoán cắt mảnh...")
    result = get_sliced_prediction(
        IMAGE_PATH,
        detection_model,
        slice_height=640,
        slice_width=640,
        overlap_height_ratio=0.2
    )
    
    num_ships = len(result.object_prediction_list)
    print(f"Sau khi lọc ngưỡng 70%, đã  thấy {num_ships} con tàu .")

    features = []
    with rasterio.open(IMAGE_PATH) as src:
        for i, pred in enumerate(result.object_prediction_list):
            pixel_coords = pred.mask.segmentation
            geo_coords = []
            for p in pixel_coords:
                lon, lat = src.xy(p[1], p[0])
                geo_coords.append([lon, lat])
            
            if geo_coords[0] != geo_coords[-1]:
                geo_coords.append(geo_coords[0])

            features.append({
                "type": "Feature",
                "id": i,
                "properties": {
                    "confidence": round(float(pred.score.value), 4),
                    "class": "ship"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [geo_coords]
                }
            })

    with open(OUTPUT_GEOJSON, "w", encoding='utf-8') as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, indent=4)
    print(f" Đã lưu GeoJSON chất lượng cao tại: {OUTPUT_GEOJSON}")


    print(" Đang vẽ kết quả lên ảnh minh họa...")
    image_cv = cv2.imread(IMAGE_PATH)
    if image_cv is not None:
        for pred in result.object_prediction_list:
            points = np.array(pred.mask.segmentation, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(image_cv, [points], isClosed=True, color=(0, 255, 0), thickness=2)
            x, y = points[0][0]
            cv2.putText(image_cv, f"{pred.score.value:.2f}", (int(x), int(y) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        
        cv2.imwrite(OUTPUT_IMAGE, image_cv)
        print(f"Đã lưu ảnh minh họa tại: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    run_task2()