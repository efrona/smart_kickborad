import cv2
import numpy as np
car = cv2.VideoCapture(-1)
from time import sleep
while True:
    cv2.waitKey()
    #sleep(1)
    ret, a = car.read()
    cv2.imshow("ddd", a)
    print(a)
car.release()
cv2.destroyAllWindows()