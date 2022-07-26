import cv2
import numpy as np
# from keras.models import load_model
from tensorflow.keras.models import load_model
from time import sleep
import threading
V_MAX = 80
model = load_model('keras_model.h5')
loop = 1
ret, frame = cv2.VideoCapture(0).read()
print(ret)
#cv2.VideoCapture(0).release()
def Predict(image):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    normalized_image_array = (image.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    return prediction[0]


def PrintPrediction(p):
    m = max(p)

    number = None
    if m > 0.9:
        for i in range(2):
            if p[i] == m:
                number = i + 1
    print(number)
    print(m)
    global loop
    if number ==2 :
        loop = 0


def Crop(frame):
    roi = frame[int(240-112):int(240+112),
                int(320-112):int(320+112)]
    return roi

def main(frame):
    # frame = cv2.imread("1.png")

    # height, width, _ = frame.shape
    # global CENTER_OF_CAM
    # CENTER_OF_CAM = [height / 2,
    #           width / 2]

    dst = Crop(frame)
    p = Predict(dst)
    PrintPrediction(p)
def r():
    global frame
    camera = cv2.VideoCapture(0)
    global loop
    while loop ==1:
        cv2.waitKey(33)
        ret, frame = camera.read()
        #cv2.imshow("Camera", frame)
    camera.release()
    cv2.destroyAllWindows()
def p():
    global loop
    while loop == 1:
        global frame
        main(frame)

def callback():
    keyInput = -1
    keyInput = cv2.waitKey(33)
    thread_list = [r, p]
    for i in thread_list:
        thread = threading.Thread(target=i)
        thread.start()
    while loop == 1:
        pass



    