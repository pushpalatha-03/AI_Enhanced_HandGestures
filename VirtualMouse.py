# ============================================================
# PUSHPA FINAL STABLE HAND GESTURE SYSTEM
# Cursor + Click + Drag + Scroll + MultiSelect
# Volume + Brightness + Screenshot + Display Text
# ============================================================

import cv2
import mediapipe as mp
import pyautogui
import screen_brightness_control as sbc
import time
import math
import keyboard

pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.8,
                       min_tracking_confidence=0.8)

draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# ---------------- VARIABLES ----------------
dragging = False
last_action = 0
DELAY = 1.2
display_text = ""
display_until = 0

# ---------------- FUNCTIONS ----------------
def show(img):
    if time.time() < display_until:
        cv2.putText(img, display_text,
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)


def set_text(text):
    global display_text, display_until
    display_text = text
    display_until = time.time() + 2


def fingers_up(lm):
    fingers = []

    fingers.append(1 if lm[4].x < lm[3].x else 0)

    tips = [8, 12, 16, 20]
    for t in tips:
        fingers.append(1 if lm[t].y < lm[t - 2].y else 0)

    return fingers


print("👉 Pushpa Gesture System Started")

# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, img = cap.read()
    img = cv2.flip(img, 1)

    res = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:

        lm = res.multi_hand_landmarks[0].landmark

        draw.draw_landmarks(img,
                            res.multi_hand_landmarks[0],
                            mp_hands.HAND_CONNECTIONS)

        fingers = fingers_up(lm)

        x = int(lm[8].x * screen_w)
        y = int(lm[8].y * screen_h)

        # ================= MOVE =================
        if fingers == [0,1,0,0,0]:
            pyautogui.moveTo(x, y)
            set_text("Move Cursor")

        # ================= LEFT CLICK =================
        elif fingers == [0,1,1,0,0] and time.time()-last_action>DELAY:
            pyautogui.click()
            set_text("Left Click")
            last_action = time.time()

        # ================= RIGHT CLICK =================
        elif fingers == [0,1,1,1,0] and time.time()-last_action>DELAY:
            pyautogui.rightClick()
            set_text("Right Click")
            last_action = time.time()

        # ================= DOUBLE CLICK =================
        elif fingers == [0,1,1,1,1] and time.time()-last_action>DELAY:
            pyautogui.doubleClick()
            set_text("Double Click")
            last_action = time.time()

        # ================= DRAG =================
        elif fingers == [0,0,0,0,0]:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True
                set_text("Drag Start")
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False
                set_text("Drag End")

        # ================= MULTI SELECT =================
        if fingers == [1,0,0,0,1] and time.time()-last_action>DELAY:
            pyautogui.keyDown("ctrl")
            pyautogui.click()
            pyautogui.keyUp("ctrl")
            set_text("Multi Select")
            last_action = time.time()

        # ================= SCROLL =================
        if fingers == [1,1,0,0,0]:
            pyautogui.scroll(300)
            set_text("Scroll Up")

        if fingers == [1,1,1,0,0]:
            pyautogui.scroll(-300)
            set_text("Scroll Down")

        # ================= BRIGHTNESS =================
        if fingers == [0,0,1,0,0] and time.time()-last_action > DELAY:
            current = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(min(current + 10, 100))
            set_text("Brightness +")
            last_action = time.time()

        if fingers == [0,0,0,1,0] and time.time()-last_action > DELAY:
            current = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(max(current - 10, 0))
            set_text("Brightness -")
            last_action = time.time()

        # ================= VOLUME =================
        if fingers == [1,1,1,1,1] and time.time()-last_action>DELAY:
            keyboard.send("volume up")
            set_text("Volume Up")
            last_action = time.time()

        if fingers == [1,0,0,0,0] and time.time()-last_action>DELAY:
            keyboard.send("volume down")
            set_text("Volume Down")
            last_action = time.time()

        # ================= MUTE =================
        if math.hypot(lm[4].x-lm[8].x, lm[4].y-lm[8].y) < 0.03:
            keyboard.send("volume mute")
            set_text("Mute")

        # ================= UNMUTE =================
        if fingers == [0,1,0,1,0] and time.time()-last_action>DELAY:
            keyboard.send("volume mute")
            set_text("Unmute")
            last_action = time.time()

        # ================= SCREENSHOT =================
        
        if fingers == [1,0,1,0,1] and time.time()-last_action>DELAY:
            filename = f"screenshot_{int(time.time())}.png"

            # take screenshot
            img_screen = pyautogui.screenshot()
            img_screen.save(filename)

            # convert for opencv display
            img_screen = cv2.cvtColor(
             cv2.imread(filename),
             cv2.COLOR_BGR2RGB
             )

            # show popup window
            cv2.imshow("Screenshot Preview", img_screen)

            set_text("Screenshot Saved & Preview")
            last_action = time.time()

    show(img)
    cv2.imshow("Pushpa Gesture Control", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()