import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint, pyqtSignal

class ImageLabel(QLabel):
    cropSelected = pyqtSignal(tuple)

    def __init__(self, parent):
        super().__init__(parent)
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_drawing = False

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.pixmap():
            painter.drawPixmap(self.rect(), self.pixmap())
        if self.is_drawing:
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(self.start_point.x(), self.start_point.y(), self.end_point.x() - self.start_point.x(), self.end_point.y() - self.start_point.y())

    def mousePressEvent(self, event):
        self.is_drawing = True
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.is_drawing:
            self.is_drawing = False
            self.end_point = event.pos()
            self.update()
            self.cropSelected.emit((self.start_point, self.end_point))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video Cropper with PyQt5 and OpenCV')
        self.setGeometry(100, 100, 800, 600)
        self.image_label = ImageLabel(self)
        self.image_label.setGeometry(10, 10, 780, 480)
        self.image_label.cropSelected.connect(self.on_crop_selected)

        self.btn_open = QPushButton('Open Video', self)
        self.btn_open.setGeometry(10, 500, 390, 40)
        self.btn_open.clicked.connect(self.open_video)

        self.btn_crop = QPushButton('Crop Video', self)
        self.btn_crop.setGeometry(400, 500, 390, 40)
        self.btn_crop.clicked.connect(self.crop_video)
        self.btn_crop.setEnabled(False)

        self.file_path = ""
        self.crop_coordinates = ()

    def open_video(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)")
        if self.file_path:
            cap = cv2.VideoCapture(self.file_path)
            ret, frame = cap.read()
            if ret:
                frame_height, frame_width, _ = frame.shape
                qt_img = self.convert_cv_qt(frame, frame_width, frame_height)
                self.image_label.setPixmap(qt_img)
            cap.release()
            self.btn_crop.setEnabled(True)

    def convert_cv_qt(self, cv_img, width, height):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def on_crop_selected(self, coordinates):
        start_point, end_point = coordinates
        self.crop_coordinates = (start_point.x(), start_point.y(), end_point.x(), end_point.y())

    def crop_video(self):
        if not self.crop_coordinates or not self.file_path:
            return
        
        cap = cv2.VideoCapture(self.file_path)
        ret, frame = cap.read()
        if not ret:
            print("Could not read video file.")
            cap.release()
            return
        
        # Original dimensions of the video frame
        original_height, original_width = frame.shape[:2]
        cap.release()

        # Dimensions of the QLabel where the frame is displayed
        display_width = self.image_label.width()
        display_height = self.image_label.height()

        # Calculate the scaling factors
        scale_w = original_width / display_width
        scale_h = original_height / display_height

        # Adjust the crop coordinates
        x1, y1, x2, y2 = self.crop_coordinates
        actual_x1 = int(x1 * scale_w)
        actual_y1 = int(y1 * scale_h)
        actual_x2 = int(x2 * scale_w)
        actual_y2 = int(y2 * scale_h)

        # Crop and save the video using OpenCV
        self.crop_video_with_opencv(self.file_path, "cropped_video.mp4", actual_x1, actual_y1, actual_x2, actual_y2)


    def crop_video_with_opencv(self, input_video_path, output_video_path, x1, y1, x2, y2):
        cap = cv2.VideoCapture(input_video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        crop_width, crop_height = x2 - x1, y2 - y1
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (crop_width, crop_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cropped_frame = frame[y1:y2, x1:x2]
            out.write(cropped_frame)

        cap.release()
        out.release()
        print("Cropped video saved as cropped_video.mp4")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
