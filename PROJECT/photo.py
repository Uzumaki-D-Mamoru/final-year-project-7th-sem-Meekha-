# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OtherWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class photo(object):
    def setupUi(self, OtherWindow):
        OtherWindow.setObjectName("OtherWindow")
        OtherWindow.resize(500, 500)
        self.centralwidget = QtWidgets.QWidget(OtherWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.QInputDialog = QtWidgets.QWidget(self.centralwidget)
        self.getText()
        
        
    def getText(self):
        text, okPressed = self.QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            path = text
            try:
                os.mkdir(text)
            except OSError:
                print ("Creation of the directory %s failed" % path)
            else:
                print ("Successfully created the directory %s " % path)
            import cv2
            size = 4
            webcam = cv2.VideoCapture(0) #Use camera 0

# We load the xml file
            classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#  Above line normalTest
#classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#Above line test with different calulation
#classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')
#classifier = cv2.CascadeClassifier('lbpcascade_frontalface.xml')


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
                    FaceFileName = text +"/face_" + str(y) + ".jpg"
                    cv2.imwrite(FaceFileName, sub_face)

                # Show the image
                cv2.imshow('lijaa',   im)
                key = cv2.waitKey(10)
                # if Esc key is press then break out of the loop
                if key == 27: #The Esc key
                    exit()

                # Show the image
                cv2.imshow('lijaa',   im)
                key = cv2.waitKey(10)
                # if Esc key is press then break out of the loop
                if key == ord("q"): #The Esc key
                        exit()

        self.retranslateUi(OtherWindow)
        QtCore.QMetaObject.connectSlotsByName(OtherWindow)

    def retranslateUi(self, OtherWindow):
        _translate = QtCore.QCoreApplication.translate
        OtherWindow.setWindowTitle(_translate("OtherWindow", "Developer"))
        





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OtherWindow = QtWidgets.QMainWindow()
    ui = photo()
    ui.setupUi(OtherWindow)
    OtherWindow.show()
    sys.exit(app.exec_())
