import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cooldown = 0


def get_position(lm, w, h):
    x = int(lm[8].x * w)   # index finger tip
    y = int(lm[8].y * h)
    return x, y


while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    cv2.rectangle(img, (int(w*0.3),0), (int(w*0.7),h), (0,255,0),2)
    cv2.putText(img,"CENTER SAFE ZONE",(int(w*0.35),40),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    if res.multi_hand_landmarks:

        hand = res.multi_hand_landmarks[0]
        draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        lm = hand.landmark
        x, y = get_position(lm, w, h)

        cv2.circle(img, (x,y), 10, (255,0,0), -1)

        if time.time() > cooldown:

            # ---------- LEFT ----------
            if x < w*0.3:
                pyautogui.press("left")
                cv2.putText(img,"MOVE LEFT",(30,60),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                cooldown = time.time()+0.5

            # ---------- RIGHT ----------
            elif x > w*0.7:
                pyautogui.press("right")
                cv2.putText(img,"MOVE RIGHT",(30,60),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                cooldown = time.time()+0.5

            # ---------- JUMP ----------
            elif y < h*0.3:
                pyautogui.press("up")
                cv2.putText(img,"JUMP",(30,60),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                cooldown = time.time()+0.5

            # ---------- SLIDE ----------
            elif y > h*0.7:
                pyautogui.press("down")
                cv2.putText(img,"SLIDE",(30,60),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                cooldown = time.time()+0.5


        # ---------- HILL CLIMB ----------
        if x > w*0.7:
            pyautogui.keyDown("right")   # Accelerate
            cv2.putText(img,"ACCELERATE",(30,120),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

        elif x < w*0.3:
            pyautogui.keyDown("left")    # Brake
            cv2.putText(img,"BRAKE",(30,120),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
        else:
            pyautogui.keyUp("right")
            pyautogui.keyUp("left")

    cv2.imshow("Pushpa Gaming Gesture Control", img)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()
