import cv2  # OpenCV
import mediapipe as mp
import numpy as np  # Import NumPy
from PIL import Image, ImageDraw


class FaceDetector:
    def __init__(self, source='image', file=None):
        self.source = source
        if self.source == 'webcam':
            self.webcam = cv2.VideoCapture(0)
        elif self.source == 'image' and file:
            self.image = Image.open(file)
            if self.image is None:
                raise ValueError("Invalid image path provided.")
        else:
            raise ValueError("Invalid source. Choose 'webcam' or 'image' and provide an image path.")

        self.face_detection = mp.solutions.face_detection.FaceDetection()
        self.drawing_utils = mp.solutions.drawing_utils

    def process_image(self, image):
        # Convert image to RGB
        image_rgb = image.convert("RGB")
        image_rgb_np = cv2.cvtColor(np.array(image_rgb), cv2.COLOR_RGB2BGR)  # Convert to numpy array
        results = self.face_detection.process(image_rgb_np)
        if results.detections:
            for face in results.detections:
                self.drawing_utils.draw_detection(image_rgb_np, face)
        return Image.fromarray(cv2.cvtColor(image_rgb_np, cv2.COLOR_BGR2RGB))  # Convert back to Pillow Image

    def run_webcam(self):
        while True:
            ret, frame = self.webcam.read()
            if not ret:
                break

            frame = self.process_frame(frame)
            cv2.imshow("Rostos na Webcam", frame)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        self.webcam.release()
        cv2.destroyAllWindows()

    def run_image(self):
        return self.process_image(self.image)

    def run(self):
        if self.source == 'webcam':
            self.run_webcam()
        elif self.source == 'image':
            return self.run_image()
