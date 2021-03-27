import cv2
import copy
import math
import numpy as np
import atexit
import keyboard
from mover import mover

def onExit(*argv):
    camera.release()
    cv2.destroyAllWindows()
    move.releaseAllKeys()
    print("Window Snapped !")

def banner():
    txt = '''
                            (_)         | |                  
   __ _ _ __ ________      ___ _ __   __| | _____      _____ 
  / _` | '__|______\ \ /\ / / | '_ \ / _` |/ _ \ \ /\ / / __|
 | (_| | |          \ V  V /| | | | | (_| | (_) \ V  V /\__ \\
  \__,_|_|           \_/\_/ |_|_| |_|\__,_|\___/ \_/\_/ |___/
                                           ~by Abhishek vyas 
    '''
    print(f"\n{txt}\n   [*]      press ESC to exit.")

def main():
    while(camera.isOpened()):
        #Main Camera
        ret, frame = camera.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # Smoothing
        frame = cv2.flip(frame, 1)  #Horizontal Flip
        
        #Background Removal
        bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)
        fgmask = bgModel.apply(frame)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        img = cv2.bitwise_and(frame, frame, mask=fgmask)
        
        # Skin detect and thresholding
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 48, 80], dtype="uint8")
        upper = np.array([20, 255, 255], dtype="uint8")
        skinMask = cv2.inRange(hsv, lower, upper)

        # Getting the contours and convex hull
        skinMask1 = copy.deepcopy(skinMask)
        contours, hierarchy = cv2.findContours(skinMask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        if length > 0:
            for i in range(length):
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
                    res = contours[ci]
            hull = cv2.convexHull(res)

            # to select the cordinates of the the top most vertex
            thetaX = math.floor((hull[hull.shape[0]-1][0][0] / frame.shape[0])*100)
            thetaY = math.floor((hull[hull.shape[0]-1][0][1] / frame.shape[1])*100)

            # moving the cursor in sync with the the top most vertex of hull
            move.move(thetaX,thetaY)

            # uncomment to check the point that camera is tracking
            # cv2.circle(frame, (hull[hull.shape[0]-1][0][0],hull[hull.shape[0]-1][0][1]), 40, (0, 20, 200), 5)
            # cv2.imshow('output', frame)

        # for exiting the cv2 preview window
        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            move.mouseUp()
            break

# creating mover object for window movement
move = mover()

# Open Camera
camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(10, 200)

# registering callback for cleanup on exit
atexit.register(onExit)

# registering callback for exit on esc
keyboard.on_press_key("esc",onExit,suppress=True)

if __name__=="__main__":
    banner()
    main()