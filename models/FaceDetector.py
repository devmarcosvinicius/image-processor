import cv2  # OpenCV
import mediapipe as mp
import os


class FaceDetector:
    def __init__(self, source='webcam', image_path=None):
        self.source = source
        if self.source == 'webcam':
            self.webcam = cv2.VideoCapture(0)
        elif self.source == 'image' and image_path:
            self.image_path = image_path
            self.image = cv2.imread(self.image_path)
            if self.image is None:
                raise ValueError("Invalid image path provided.")
        else:
            raise ValueError("Invalid source. Choose 'webcam' or 'image' and provide an image path.")

        self.face_detection = mp.solutions.face_detection.FaceDetection()
        self.drawing_utils = mp.solutions.drawing_utils

    def process_frame(self, frame):
        # Convert frame to RGB as mediapipe expects RGB input
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame_rgb)
        if results.detections:
            for face in results.detections:
                self.drawing_utils.draw_detection(frame, face)
        return frame

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
        processed_image = self.process_frame(self.image)
        # Generate the output file path
        output_dir = os.path.dirname(self.image_path)
        output_filename = 'Reconhecimento_' + os.path.basename(self.image_path)
        output_path = os.path.join(output_dir, output_filename)

        # Save the processed image
        success = cv2.imwrite(output_path, processed_image)
        if success:
            print(f"Imagem gerada e salva como {output_path}!")
        else:
            print("Erro ao salvar a imagem.")

    def run(self):
        if self.source == 'webcam':
            self.run_webcam()
        elif self.source == 'image':
            self.run_image()

