import sys
import cv2
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMessageBox


class VideoToImageConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP4 to JPG Converter")
        self.setGeometry(300, 200, 400, 200)
        self.setStyleSheet("background-color: #c0c7d1;")

        self.label = QLabel("Select a video file to convert frames:", self)
        self.label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.select_button = QPushButton("Select Video", self)
        self.select_button.setStyleSheet("background-color: #34495E; color: white; font-size: 12px; padding: 5px;")
        self.select_button.clicked.connect(self.get_filename)

        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("font-size: 12px; color: blue;")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def get_filename(self):
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "MP4 Files (*.mp4);;All Files (*)", options=options)

        if filepath:
            self.status_label.setText("Processing video...")
            self.mp42jpg(filepath)
        else:
            QMessageBox.warning(self, "Input Error", "No file selected. Please select a valid video file.")

    def mp42jpg(self, filepath):
        video = cv2.VideoCapture(filepath)

        if not video.isOpened():
            QMessageBox.critical(self, "Error", f"Cannot open the video file:\n{filepath}")
            return

        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video.get(cv2.CAP_PROP_FPS))

        print(f"Video Info: length={length}, width={width}, height={height}, FPS={fps}")

        filename = os.path.splitext(os.path.basename(filepath))[0]
        output_dir = os.path.join("output_frames", filename)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        count = 0

        while video.isOpened():
            ret, image = video.read()
            if not ret:
                break

            if count % fps == 0:
                frame_filename = os.path.join(output_dir, f"frame{count}.jpg")
                cv2.imwrite(frame_filename, image)
                print(f"Saved: {frame_filename}")

            count += 1

        video.release()
        self.status_label.setText(f"Frames saved in: {output_dir}")
        QMessageBox.information(self, "Process Completed", f"Frames saved in folder:\n{output_dir}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoToImageConverter()
    window.show()
    sys.exit(app.exec_())
