import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox



class App(QWidget):

    # def __init__(self):
    #     super().__init__()
    #     self.title = 'PyQt5 input dialogs - pythonspot.com'
    #     self.left = 10
    #     self.top = 10
    #     self.width = 640
    #     self.height = 480
    #     self.initUI()
    
    def setupUi(self, third):
        third.setObjectName("third")
        third.resize(290, 377)
        self.centralwidget = QtWidgets.QWidget(third)
        self.centralwidget.setObjectName("centralwidget")
        # self.setWindowTitle(self.title ='Person name')
        # self.setGeometry(self.left=10, self.top10, self.width=640, self.height=480)

        self.getText()
    #     self.retranslateUi(third)
    #     QtCore.QMetaObject.connectSlotsByName(third)

    # def retranslateUi(self, third):
    #     _translate = QtCore.QCoreApplication.translate

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            path = 'dataset/' + text 
            try:
                os.mkdir(path)
            except OSError:
                print ("Creation of the directory %s failed" % path)
                self.close_application()
            else:
                print ("Successfully created the directory %s " % path)
                import cv2
                size = 4
                webcam = cv2.VideoCapture(0) #Use camera 0
# We load the xml file
                classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

                while True:
                    (rval, im) = webcam.read()
                    im=cv2.flip(im,1,0) #Flip to act as a mirror

                # Resize the image to speed up detection
                    mini = cv2.resize(im,(int(im.shape[1] / size), int(im.shape[0] / size)))

                # detect MultiScale / faces
                    faces = classifier.detectMultiScale(mini)
                # Draw rectangles around each face
                    for f in faces:
                        (x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
                        cv2.rectangle(im, (x, y), (x + w, y + h),(0,255,0),thickness=4)
                    #Save just the rectangle faces in SubRecFaces
                        sub_face = im[y:y+h, x:x+w]
                        FaceFileName = "dataset/" + text +"/face_" + str(y) + ".jpg"

                        cv2.imwrite(FaceFileName, sub_face)


                # Show the image
                    cv2.imshow('click picture',   im)
                    key = cv2.waitKey(10)
                # if Esc key is press then break out of the loop
                    if key == 27: #The Esc key
                        break

    def close_application(self):
        choice = QtWidgets.QMessageBox.question(self, 'Extract!',
                                            "Name Already Exists. Try again? ",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            
            self.getText()
        else:
            pass
                
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    third = QtWidgets.QMainWindow()
    ui = App()
    ui.setupUi(third)
    third.show()
    sys.exit(app.exec_())

