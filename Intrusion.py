import cv2
import os
import time
import smtplib
import face_recognition
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import RPi.GPIO as GPIO
from time import sleep
import numpy as np

# GPIO Configuration
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
IR_SENSOR_PIN = 21
IR_SENSOR_PIN1 = 16
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN1, GPIO.IN)
GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)

# Email Configuration
EMAIL_ADDRESS = "tejaswini.rachuluri@gmail.com"
EMAIL_PASSWORD = "zeio vfzg bbqi ztrb"
TO_EMAIL_ADDRESS = "rachuluritejaswini@gmail.com"

# Folder Configuration
output_folder = "detected_frames"
known_faces_folder = "known_faces"
os.makedirs(output_folder, exist_ok=True)
os.makedirs(known_faces_folder, exist_ok=True)

# Log file
LOG_FILE = "detection_log.csv"

# Load known faces
known_face_encodings = []
known_face_names = []

def load_known_faces():
    print("[INFO] Loading known faces...")
    for file in os.listdir(known_faces_folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(known_faces_folder, file)
            image = face_recognition.load_image_file(path)
           
            # Try both HOG and CNN models if needed
            face_locations = face_recognition.face_locations(image, model='hog')
            if not face_locations:
                face_locations = face_recognition.face_locations(image, model='cnn')
                if not face_locations:
                    print(f"[WARNING] No face found in {file}")
                    continue
           
            # Get face encodings
            encodings = face_recognition.face_encodings(image, face_locations)
            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(file)[0])
                print(f"[SUCCESS] Loaded: {file}")
            else:
                print(f"[WARNING] Could not encode face in {file}")
    print(f"[INFO] Total loaded faces: {len(known_face_encodings)}")

def send_email(subject, body, image_path):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL_ADDRESS
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with open(image_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
        msg.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL_ADDRESS, msg.as_string())
        print("[INFO] Email sent successfully")
    except Exception as e:
        print(f"[ERROR] Email failed: {e}")

def recognize_faces(frame):
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
    try:
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        if not face_locations:
            print("[INFO] No face detected")
            return [], False

        # Get face encodings - this is the most reliable method
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if not face_encodings:
            print("[WARNING] No encodings found")
            return [], False

        recognized = []
        for face_encoding in face_encodings:
            # Calculate face distances to all known faces
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            # Find the best match (smallest distance)
            best_match_index = np.argmin(face_distances)
            min_distance = face_distances[best_match_index]
            
            # Use a threshold of 0.6 (can adjust this)
            if min_distance < 0.6:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"
            
            recognized.append(name)
            print(f"[INFO] Face Detected: {name} (Distance: {min_distance:.4f})")

        return recognized, True

    except Exception as e:
        print(f"[ERROR] Face recognition failed: {e}")
        return [], False

def process_detection():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Set width
    cap.set(4, 480)  # Set height
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("[ERROR] Failed to capture frame")
        return None

    # Enhance image quality
    frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=20)
   
    timestamp = int(time.time())
    frame_path = os.path.join(output_folder, f"frame_{timestamp}.jpg")
    cv2.imwrite(frame_path, frame)

    names, found = recognize_faces(frame)
    if not found:
        print("[INFO] No human detected")
        return None

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp},{', '.join(names)},{frame_path}\n")

    subject = "ALERT: Human Detected"
    body = f"Detected at {time.ctime(timestamp)}\nIdentified: {', '.join(names)}"
    send_email(subject, body, frame_path)
    return True

# Initialize
load_known_faces()
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,recognized_names,image_path\n")

# Main loop
try:
    while True:
        if GPIO.input(IR_SENSOR_PIN) == 0:
            print("[EVENT] Motion Detected - Scanning...")
            GPIO.output(20, GPIO.HIGH)
           
            # Try multiple times for better detection
            for _ in range(3):
                result = process_detection()
                if result:
                    print("[INFO] Detection processed.")
                    break
                time.sleep(0.5)
           
            GPIO.output(20, GPIO.LOW)
            sleep(1)

        GPIO.output(3, GPIO.HIGH if GPIO.input(IR_SENSOR_PIN1) == 0 else GPIO.LOW)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n[INFO] Exiting...")

finally:
    GPIO.cleanup()
    print("[INFO] GPIO cleaned up")