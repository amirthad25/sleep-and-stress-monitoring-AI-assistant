import cv2
from deepface import DeepFace

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces_and_emotions(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        print("⚠️ No faces detected.")
        return

    for (x, y, w, h) in faces:
        face_crop = image[y:y+h, x:x+w]  # Crop detected face

        # Emotion recognition
        try:
            result = DeepFace.analyze(face_crop, actions=['emotion'], detector_backend='opencv', enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            print(f"🎭 Detected Emotion: {emotion}")

            # Draw face rectangle and emotion label
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        except Exception as e:
            print(f"Emotion detection error: {e}")

    # Show output image
    cv2.imshow("Detected Faces & Emotions", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

detect_faces_and_emotions("test_image.jpg")
