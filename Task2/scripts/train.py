from ultralytics import YOLO
import os

model = YOLO("yolov8s-obb.pt") 

def run_training():
    
    base_path = r"D:\FPTU\AIS8\TEST\Task2"
    project_path = os.path.join(base_path, "runs")
    
    model.train(
        data=os.path.join(base_path, "data", "data.yaml"), 
        epochs=10,          
        imgsz=320,          
        batch=4,            
        device="cpu",       
        project=project_path,  
        name="train_ship"      
    )

if __name__ == "__main__":
    run_training()