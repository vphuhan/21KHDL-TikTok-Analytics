import cv2
import numpy as np
import torch
from transformers import (
    VideoMAEImageProcessor, VideoMAEModel,
    AutoFeatureExtractor, AutoModelForAudioClassification,
    AutoImageProcessor, AutoModel
)
from ultralytics import YOLO
import librosa # type: ignore
import ffmpeg
from pydub import AudioSegment
import tempfile
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Configuration
TARGET_FPS = 1  # Frames per second to analyze
AUDIO_SAMPLE_RATE = 16000

# def extract_audio_features(video_path):
#     """Extract audio features including sound type and speech content"""
#     print("\nExtracting audio features...")
    
#     # Extract audio from video
#     video = AudioSegment.from_file(video_path)
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
#         video.export(tmpfile.name, format="wav")
#         waveform, sr = librosa.load(tmpfile.name, sr=AUDIO_SAMPLE_RATE)
#         os.remove(tmpfile.name)

#     # Initialize audio models
#     audio_feature_extractor = AutoFeatureExtractor.from_pretrained("superb/hubert-base-superb-ks")
#     audio_model = AutoModelForAudioClassification.from_pretrained("superb/hubert-base-superb-ks")

#     # Process audio
#     inputs = audio_feature_extractor(
#         waveform,
#         sampling_rate=sr,
#         return_tensors="pt",
#         padding=True,
#         return_attention_mask=True
#     )
    
#     with torch.no_grad():
#         outputs = audio_model(**inputs)
    
#     # Get audio classifications
#     sound_class = audio_model.config.id2label[outputs.logits.argmax(-1).item()]
    
#     return {
#         "sound_type": sound_class,
#         "waveform": waveform,
#         "sample_rate": sr
#     }

def extract_audio_features(video_path):
    """Extract audio features including sound type and speech content"""
    print("\nExtracting audio features...")
    
    # Commented out FFmpeg-dependent audio extraction
    # Placeholder audio feature extraction
    try:
        # Initialize audio models
        audio_feature_extractor = AutoFeatureExtractor.from_pretrained("superb/hubert-base-superb-ks")
        audio_model = AutoModelForAudioClassification.from_pretrained("superb/hubert-base-superb-ks")

        # Generate a dummy waveform for testing
        waveform = np.random.rand(AUDIO_SAMPLE_RATE)
        sr = AUDIO_SAMPLE_RATE

        # Process audio
        inputs = audio_feature_extractor(
            waveform,
            sampling_rate=sr,
            return_tensors="pt",
            padding=True,
            return_attention_mask=True
        )
        
        with torch.no_grad():
            outputs = audio_model(**inputs)
        
        # Get audio classifications
        sound_class = audio_model.config.id2label[outputs.logits.argmax(-1).item()]
        
        return {
            "sound_type": sound_class,
            "waveform": waveform,
            "sample_rate": sr
        }
    except Exception as e:
        print(f"Audio feature extraction error: {e}")
        return {
            "sound_type": "unknown",
            "waveform": None,
            "sample_rate": AUDIO_SAMPLE_RATE
        }

def analyze_lighting(frame):
    """Analyze lighting conditions using brightness and contrast"""
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    # Brightness analysis
    brightness = np.mean(gray)
    
    # Contrast analysis
    contrast = np.std(gray)
    
    return {
        "brightness": float(brightness),
        "contrast": float(contrast),
        "lighting_condition": "low-light" if brightness < 50 else "well-lit"
    }

def analyze_scene(frame):
    """Analyze scene content using Places365 model"""
    scene_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
    scene_model = AutoModel.from_pretrained("google/vit-base-patch16-224-in21k")
    
    inputs = scene_processor(images=frame, return_tensors="pt")
    with torch.no_grad():
        outputs = scene_model(**inputs)
    
    # Get scene embeddings
    scene_features = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return scene_features

def video_analysis(video_path):
    try:
        # Initialize models
        yolo_model = YOLO("yolov8n.pt")
        videomae_processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
        videomae_model = VideoMAEModel.from_pretrained("MCG-NJU/videomae-base")

        # Audio analysis
        audio_results = extract_audio_features(video_path)

        # Video analysis
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frame_interval = int(fps / TARGET_FPS)
        frame_count = 0
        
        results = {
            "visual_features": [],
            "objects": [],
            "lighting": [],
            "scenes": []
        }

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_interval == 0:
                # Convert frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Object detection
                detections = yolo_model(frame_rgb)
                results["objects"].append({
                    "frame": frame_count,
                    "objects": detections[0].names,
                    "confidences": detections[0].boxes.conf.tolist()
                })

                # Lighting analysis
                lighting = analyze_lighting(frame_rgb)
                results["lighting"].append(lighting)

                # Scene analysis
                scene_features = analyze_scene(frame_rgb)
                results["scenes"].append(scene_features.tolist())

                # VideoMAE features
                processed_frame = cv2.resize(frame_rgb, (224, 224)).transpose(2, 0, 1)
                results["visual_features"].append(processed_frame)

            frame_count += 1

        cap.release()

        # Process visual features with VideoMAE
        visual_inputs = videomae_processor(results["visual_features"], return_tensors="pt")
        with torch.no_grad():
            video_features = videomae_model(**visual_inputs).last_hidden_state[:, 0, :].numpy()
        
        return {
            "audio": audio_results,
            "video_features": video_features.tolist(),
            "objects": results["objects"],
            "lighting_stats": {
                "average_brightness": np.mean([x["brightness"] for x in results["lighting"]]),
                "average_contrast": np.mean([x["contrast"] for x in results["lighting"]])
            },
            "scene_embeddings": results["scenes"]
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    analysis_results = video_analysis("C:/Users/nguye/OneDrive/Máy tính/473687472_29115065711425948_3453487025569279795_n.mp4")
    if analysis_results:
        print("\nComplete Analysis Results:")
        print("Audio Features:", analysis_results["audio"]["sound_type"])
        print("Average Brightness:", analysis_results["lighting_stats"]["average_brightness"])
        print("Detected Objects in First Frame:", analysis_results["objects"][0]["objects"])
        print("Video Feature Shape:", np.array(analysis_results["video_features"]).shape)