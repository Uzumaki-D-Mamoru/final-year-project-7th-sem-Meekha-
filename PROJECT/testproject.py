from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from imutils.video import VideoStream
from twilio.rest import Client
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import csv

import os
import sys
import time

from ui_main_window import *

from twilio import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            pass #quit

        self.status = QStatusBar()
        self.setStatusBar(self.status)


        self.save_path = ""

        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)
        self.viewfinder.setStatusTip("Test Camera")


        # Set the default camera.
        self.select_camera(0)

        # Setup tools
        camera_toolbar = QToolBar("Camera")
        camera_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(camera_toolbar)

        photo_action = QAction(QIcon(os.path.join('images', 'camera-black.png')), "START...", self)
        photo_action.setStatusTip("facial recongnition")
        photo_action.triggered.connect(self.take_photo)
        camera_toolbar.addAction(photo_action)

        photo_action = QAction(QIcon(os.path.join('images', 'camera-black.png')), "click...", self)
        photo_action.setStatusTip("facial recongnition")
        photo_action.triggered.connect(self.click)
        camera_toolbar.addAction(photo_action)

        

        camera_selector = QComboBox()
        camera_selector.addItems([c.description() for c in self.available_cameras])
        camera_selector.currentIndexChanged.connect( self.select_camera )

        camera_toolbar.addWidget(camera_selector)


        self.setWindowTitle("MIKHA")
        self.show()

    def select_camera(self,i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda i, e, s: self.alert(s))
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image %04d captured" % self.save_seq))

        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0

    def take_photo(self,i):
    	self.camera.stop()
    	ap = argparse.ArgumentParser()
    	ap.add_argument("-e", "--encodings", type=str, default="encodings.pickle",
	help="path to serialized db of facial encodings")
    	ap.add_argument("-o", "--output", type=str, default="output/haha.avi",
	help="path to output video")
    	ap.add_argument("-y", "--display", type=int, default=1,
	help="whether or not to display output frame to screen")
    	ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
    	args = vars(ap.parse_args())
    	print("[INFO] loading encodings...")
    	data = pickle.loads(open(args["encodings"], "rb").read())
    	print("[INFO] starting video stream...")
    	vs = VideoStream(src=0).start()
    	writer = None
    	time.sleep(2.0)

    	while True:
    		frame = vs.read()
    		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    		rgb = imutils.resize(frame, width=750)
    		r = frame.shape[1] / float(rgb.shape[1])
    		boxes = face_recognition.face_locations(rgb,
				model=args["detection_method"])
    		encodings = face_recognition.face_encodings(rgb, boxes)
    		names = []

    		for encoding in encodings:
    			matches = face_recognition.compare_faces(data["encodings"],
					encoding)
    			name = "Unknown"

    			if True in matches:
    				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
    				counts = {}

    				for i in matchedIdxs:
    					name = data["names"][i]
    					counts[name] = counts.get(name, 0) + 1

    				name = max(counts, key=counts.get)

    			names.append(name)

    		for ((top, right, bottom, left), name) in zip(boxes, names):
    			top = int(top * r)
    			right = int(right * r)
    			bottom = int(bottom * r)
    			left = int(left * r)

    			cv2.rectangle(frame, (left, top), (right, bottom),
					(0, 255, 0), 2)
    			y = top - 15 if top - 15 > 15 else top + 15
    			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
					0.75, (0, 255, 0), 2)
    			if name == "Prasanna":
    				duration = 1  # seconds
    				freq = 440  # Hz
    				os.system('spd-say "Blacklisted"'.format(duration, freq))
    				os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    				print("blacklisted face detected at %s" % str(time.ctime()))
                    with open('log.csv', mode='w') as csv_file:
                        fieldnames = ['date_time']
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow({'date_time':str(time.ctime())})

    			if name == "Unknown":
    				duration = 1 
    				freq = 440
                    os.system('spd-say "unknown person"'.format(duration, freq))
    				os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    				print("Unkown face detected at %s" % str(time.ctime()))



    		if writer is None and args["output"] is not None:
    			fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    			writer = cv2.VideoWriter(args["output"], fourcc, 20,
					(frame.shape[1], frame.shape[0]), True)

    		if writer is not None:
    			writer.write(frame)

    		if args["display"] > 0:
    			cv2.imshow("Frame", frame)
    			key = cv2.waitKey(1) & 0xFF

    			if key == ord("q"):
    				break
    				
    	

    	cv2.destroyAllWindows()
    	vs.stop()

    	if writer is not None:
    		writer.release()

    
    def click(self, s):
    	self.camera.stop()
    	class MainWindow(QWidget):
    		def __init__(self):
    			super().__init__()
    			self.ui = Ui_Form()
    			self.ui.setupUi(self)
    			self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    			if self.face_cascade.empty():
    				QMessageBox.information(self, "Error Loading cascade classifier" , "Unable to load the face	cascade classifier xml file")
    				sys.exit()
    				self.timer = QTimer()
    				self.timer.timeout.connect(self.detectFaces)
    				self.ui.control_bt.clicked.connect(self.controlTimer)


    		def detectFaces(self):
    			ret, frame = self.cap.read()
    			scaling_factor = 0.8
    			frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    			face_rects = self.face_cascade.detectMultiScale(gray, 1.3, 5)
    			for (x, y, w, h) in face_rects:
    				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    				height, width, channel = frame.shape
    				step = channel * width
    				qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
    				self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))



    		def controlTimer(self):
    			if not self.timer.isActive():
    				self.cap = cv2.VideoCapture(0)
    				self.timer.start(20)
    				self.ui.control_bt.setText("Stop")
    			else:
    				self.timer.stop()
    				self.cap.release()
    				self.ui.control_bt.setText("Start")


    	if __name__ == '__main__':
    		app = QApplication(sys.argv)
    		mainWindow = MainWindow()
    		mainWindow.show()
    		sys.exit(app.exec_())		


    def alert(self, s):
        """
        Handle errors coming from QCamera dn QCameraImageCapture by displaying alerts.
        """
        err = QErrorMessage(self)
        err.showMessage(s)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("MIKHA")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


    window = MainWindow()
app.exec_()
