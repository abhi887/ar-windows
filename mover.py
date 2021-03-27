import win32gui as win
import win32api as winapi
import pyautogui as auto
import math
import time

class mover:

    window_id=0
    is_choosing = True
    initial_x = 0

    def __init__(self):
        auto.FAILSAFE = False
        self.setWindowId()

        # to start the alt+tab window selection screen
        auto.keyDown("alt")
        auto.keyDown("tab")
        auto.keyUp("tab")


    '''to move the cursor and in turn window around screen,
        for choosing the window to control on startup,
        to know when the window is snapped to edge and let go control'''
    def move(self,x,y):
        screen_width = winapi.GetSystemMetrics(0)
        screen_height = winapi.GetSystemMetrics(0)
        X = math.ceil((screen_width * x) / 100)
        Y = math.ceil((screen_height * y) / 100)
        if(self.is_choosing):
            if(self.initial_x==0): 
                print('''\n[ <- -> ]   glide your hand left or right to mark window.''')
                print('''\n  [ ^ ]     raise your hand to select marked window.''')
                self.initial_x = X
            
            if(Y == 0):
                print('''\n   [*]      move your hand to move the window.''')
                print('''\n[<  ^  >]   move window to screen edges to drop.\n''')
                auto.keyUp("alt")
                self.is_choosing = False
                time.sleep(2)
                self.setCursor()
                
            if X < self.initial_x-500:
                auto.press("left")
            elif X > self.initial_x+1000:
                auto.press("right")
        else:
            auto.moveTo(X,Y,0.2,auto.easeInOutQuad)
            if(X == 0 or Y == 0 or X == screen_width):
                self.mouseUp()
                exit(0)

        if(win.GetForegroundWindow()!=self.window_id):
            self.setWindowId()
            self.mouseUp()
            self.setCursor()

    '''to set the cursor down on the title bar of window in
        focus and take control'''
    def setCursor(self):
        x,y,r,b = win.GetWindowRect(win.GetForegroundWindow())
        width = r - x
        height = b - y

        # move the cursor to the spot 3.5% from top and 60% from top-left of active window
        auto.moveTo(x+math.ceil(width/1.75),y+math.floor(0.035*height))
        auto.mouseDown()

    '''to remember the id(hwnd) of the current window to 
        know about window switches'''
    def setWindowId(self):
        self.window_id=win.GetForegroundWindow()

    '''to let go of mouse control'''
    def mouseUp(self):
        auto.mouseUp()

    '''to unregister all controlled keys'''
    def releaseAllKeys(self):
        auto.mouseUp()
        auto.keyUp("alt")
        auto.keyUp("tab")

    '''for inline printing for debugging'''
    def printc(self,*arg):
        print(20*" ","\r",*arg,end="")

# old window movement code using win32api 
# doesn't work as it doesn't support window snapping on edges

# MoveWindow(GetForegroundWindow(),50,50,500,500,0)
# win.SetWindowPos(win.GetForegroundWindow(),0 , 50, 50, 500, 500,0)