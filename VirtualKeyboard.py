import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = False

# =============================
# MEDIAPIPE
# =============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.8,
                       min_tracking_confidence=0.8)

draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

shift_on = False
cooldown = 0
last_key = ""

# =============================
# KEYBOARD LAYOUT
# =============================
keyboard = [
['ESC','1','2','3','4','5','6','7','8','9','0','BACK'],
['TAB','Q','W','E','R','T','Y','U','I','O','P'],
['SHIFT','A','S','D','F','G','H','J','K','L','ENTER'],
['Z','X','C','V','B','N','M'],
['SPACE']
]

# =============================
def dist(a,b):
    return math.hypot(a.x-b.x, a.y-b.y)

# =============================
# DRAW KEYBOARD
# =============================
def draw_keyboard(img):

    h,w,_ = img.shape
    key_w,key_h,gap = 45,40,5

    def width(k):
        if k=="SPACE": return key_w*5
        if k in ["BACK","ENTER","SHIFT","TAB","ESC"]:
            return key_w*2
        return key_w

    boxes=[]
    start_y = h - len(keyboard)*(key_h+gap) - 10

    for r,row in enumerate(keyboard):

        row_w=sum(width(k) for k in row)+gap*(len(row)-1)

        # SHIFT KEYBOARD RIGHT (ESC visible)
        x=(w-row_w)//2 + 20

        for key in row:

            w2=width(key)
            y=start_y+r*(key_h+gap)

            cv2.rectangle(img,(x,y),(x+w2,y+key_h),(255,255,255),-1)
            cv2.rectangle(img,(x,y),(x+w2,y+key_h),(0,0,0),1)

            cv2.putText(img,key,(x+5,y+25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,0,0),
                        2)

            boxes.append((key,x,y,x+w2,y+key_h))
            x+=w2+gap

    return boxes

# =============================
while True:

    ret,img=cap.read()
    img=cv2.flip(img,1)

    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=hands.process(rgb)

    boxes=draw_keyboard(img)

    # SHOW LAST PRESSED KEY
    cv2.putText(img,f"Pressed: {last_key}",
                (30,60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0,255,0),
                3)

    if res.multi_hand_landmarks:

        hand=res.multi_hand_landmarks[0]
        lm=hand.landmark

        draw.draw_landmarks(img,hand,mp_hands.HAND_CONNECTIONS)

        h,w,_=img.shape
        cx=int(lm[8].x*w)
        cy=int(lm[8].y*h)

        # PINCH CLICK
        if dist(lm[4],lm[8])<0.03 and time.time()>cooldown:

            for key,x1,y1,x2,y2 in boxes:

                if x1<cx<x2 and y1<cy<y2:

                    if key=="SPACE":
                        pyautogui.write(" ")
                        last_key="SPACE"

                    elif key=="ENTER":
                        pyautogui.press("enter")
                        last_key="ENTER"

                    elif key=="BACK":
                        pyautogui.press("backspace")
                        last_key="BACKSPACE"

                    elif key=="ESC":
                        pyautogui.press("esc")
                        last_key="ESC"

                    elif key=="SHIFT":
                        shift_on=not shift_on
                        last_key="SHIFT"

                    else:
                        char=key if shift_on else key.lower()
                        pyautogui.write(char)
                        last_key=char
                        shift_on=False

                    print("Pressed:", last_key)

                    cooldown=time.time()+0.6

    cv2.imshow("Pushpa Virtual Keyboard",img)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()