from transformers import VideoMAEImageProcessor, VideoMAEModel
import numpy as np
import torch
import cv2

def load_and_process_video(video_path):
    print(f"\n1. Loading video from: {video_path}")
    
    # Load video frames
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error: Could not open video file")
    
    frames = []
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video info: {frame_count} frames, {fps:.2f} FPS")
    
    # Sample 16 frames evenly spaced
    indices = np.linspace(0, frame_count - 1, 16, dtype=int)
    print(f"Sampling frames at indices: {indices}")
    
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            # Convert BGR to RGB and resize
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224))
            # Convert to channel-first format
            frame = frame.transpose(2, 0, 1)
            frames.append(frame)
    
    cap.release()
    print(f"Successfully processed {len(frames)} frames")
    return frames

def extract_video_features(frames):
    # Initialize model and processor
    processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
    model = VideoMAEModel.from_pretrained("MCG-NJU/videomae-base")
    
    # Process frames and create tensor
    inputs = processor(frames, return_tensors="pt")
    
    # Forward pass
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Return the [CLS] token embeddings (video-level features)
    return outputs.last_hidden_state[:, 0, :].numpy()

def main():
    video_path = "C:/Users/nguye/OneDrive/Máy tính/476333982_9238249779602853_5476012565882341889_n.mp4"
    
    try:
        # Load and process video
        frames = load_and_process_video(video_path)
        
        # Extract features
        features = extract_video_features(frames)
        
        # Save features
        np.save("video_features.npy", features)
        print("\nFeature extraction completed!")
        print(f"Feature shape: {features.shape}")
        print("Features saved to video_features.npy")
        
    except Exception as e:
        print(f"Error: {str(e)}")

    import numpy as np

    # Load the features
    features = np.load("video_features.npy")

    # Print the shape and content
    print("Feature shape:", features.shape)  # Should be (1, 768)
    print("Feature values:", features)
    
if __name__ == "__main__":
    main()