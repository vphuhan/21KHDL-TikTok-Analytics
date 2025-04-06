from transformers import VideoMAEImageProcessor, VideoMAEModel
import cv2
import torch
import numpy as np

# Load a pre-trained object detection model (e.g., YOLO)
# Install ultralytics: pip install ultralytics
from ultralytics import YOLO

# Load VideoMAE model and processor
processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
videomae_model = VideoMAEModel.from_pretrained("MCG-NJU/videomae-base")

# Load YOLO model
yolo_model = YOLO("yolov8n.pt")  # Load a pre-trained YOLO model

def analyze_video(video_path):
    # Load video
    cap = cv2.VideoCapture(video_path)
    frames = []
    detected_objects = []

    # Sample frames
    for _ in range(16):  # Sample 16 frames
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

        # Run object detection on the frame
        results = yolo_model(frame)
        detected_objects.append(results[0].boxes.cls.tolist())  # Get detected object classes

    cap.release()

    # Extract VideoMAE features
    inputs = processor(frames, return_tensors="pt")
    with torch.no_grad():
        outputs = videomae_model(**inputs)
    video_features = outputs.last_hidden_state[:, 0, :].numpy()

    # Analyze detected objects and video features
    print("Detected objects in each frame:", detected_objects)
    print("Video features shape:", video_features.shape)

# Example usage
# analyze_video("C:/Users/nguye/OneDrive/Máy tính/476333982_9238249779602853_5476012565882341889_n.mp4")
# analyze_video("C:/Users/nguye/OneDrive/Máy tính/475715794_28294998100146817_2296967483880380439_n.mp4")
analyze_video("C:/Users/nguye/OneDrive/Máy tính/473687472_29115065711425948_3453487025569279795_n.mp4")