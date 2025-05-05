import cv2
from ultralytics import YOLO
import random
import sound
from playsound import playsound
import pygame
import threading

# load model
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)
roles = ["Infected", "Traitor", "Robot"]

classes = [
    "person", "book", "knife", "laptop", "cell phone",
    "backpack", "bottle", "cup", "chair", "fire hydrant"
]

colors = {
    "person": (0, 0, 255),       # Red
    "book": (255, 0, 0),         # Blue
    "knife": (0, 255, 255),      # Yellow
    "laptop": (0, 255, 0),       # Green
    "cell phone": (255, 0, 255),  # Pink
    "backpack": (255, 165, 0),   # Orange
    "bottle": (0, 128, 255),     # Blue
    "cup": (255, 255, 0),        # Yellow
    "chair": (128, 0, 255),      # Purple
    "fire hydrant": (255, 0, 127) #Pink
}

sound_map = {
    "person": "motion_detected.wav",      
    "book": "alarm.wav",     
    "skateboard": "alert_ping.mp3",     
    "laptop": "metal_ding.mp3",      
    "cell phone": "metal_ding.mp3",
    "backpack": "radio_static.mp3",   
    "bottle": "alarm.wav",    
    "cup": "alarm.wav",        
    "chair": "metal_ding.mp3",      
    "fire hydrant": "alart_ping.mp3" 
}

custom_labels = {
    "person": "Person",
    "book": "ELIMINATE EXTERNAL KNOWLEDGE",
    "skateboard": "WEAPON DETECTED",
    "laptop": "DESTROY TECHNOLOGY",
    "cell phone": "CELLULAR DEVICE INTERFERENCE",
    "backpack": "X",
    "bottle": "X",
    "cup": "X",
    "chair": "X",
    "fire hydrant": "X"
}

def play_sound(sound_file):
    def _play():
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    threading.Thread(target=_play, daemon=True).start()

if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # inference
    results = model(frame)[0]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = model.names[cls_id]
        if class_name in classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"{custom_labels.get(class_name, class_name)} {conf:.2f}"
            color = colors.get(class_name, (255, 255, 255))  # fallback = white

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 5)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)
            sound = sound_map.get(class_name)
            if sound: 
                play_sound(sound)

    cv2.imshow("Person Detection - YOLOv5", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()