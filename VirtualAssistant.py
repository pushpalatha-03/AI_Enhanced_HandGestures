import tkinter as tk
from tkinter.simpledialog import askstring
import threading
import os
import datetime
import webbrowser
import time
import cv2
import mediapipe as mp
import pyttsx3
import speech_recognition as sr
import pyautogui
import wikipedia

# ============================================================
#  VOICE ENGINE
# ============================================================
engine = pyttsx3.init()
engine.setProperty("rate", 170)
sleep_mode = False


def speak(text):
    add_message("PROTON", text)
    engine.say(text)
    engine.runAndWait()


# ============================================================
#  OPEN APPS
# ============================================================
def open_app(name):
    try:
        if name == "chrome":
            os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
        elif name == "word":
            os.startfile("winword")
        elif name == "excel":
            os.startfile("excel")
        elif name == "powerpoint":
            os.startfile("powerpnt")
        elif name == "calculator":
            os.startfile("calc")
        speak("Opening " + name)
        time.sleep(2)
    except Exception as e:
        speak("App not found: " + name)


# ============================================================
#  DATE & TIME
# ============================================================
def show_time():
    speak("Time is " + datetime.datetime.now().strftime("%H:%M"))


def show_date():
    speak("Date is " + datetime.datetime.now().strftime("%Y-%m-%d"))


# ============================================================
#  LOCATION
# ============================================================
def find_location_safe():
    root.after(0, ask_location_popup)


def ask_location_popup():
    place = askstring("PROTON", "Enter Location", parent=root)
    if place:
        speak("Finding " + place)
        webbrowser.open("https://www.google.com/maps/search/" + place)


# ============================================================
#  COPY / PASTE
# ============================================================
def copy_text():
    pyautogui.hotkey("ctrl", "c")
    speak("Copied")


def paste_text():
    pyautogui.hotkey("ctrl", "v")
    speak("Pasted")


# ============================================================
#  INTERNET SEARCH
# ============================================================
def search_internet(query):
    try:
        result = wikipedia.summary(query, 2)
        speak(result)
    except Exception:
        speak("Searching Google")
        webbrowser.open("https://www.google.com/search?q=" + query)


# ============================================================
#  FINGER COUNTING  (fixed logic)
# ============================================================
TIP_IDS = [4,  8,  12, 16, 20]   # fingertip landmarks
MCP_IDS = [2,  5,   9, 13, 17]   # base-knuckle landmarks


def count_fingers(hand_landmarks, handedness_label):
    """
    Returns the number of open fingers (0-5).
    Uses MCP base instead of mid-joint for accuracy.
    Handles Left/Right hand correctly after camera flip.
    """
    fingers = []
    lm = hand_landmarks.landmark

    # --- THUMB  (X-axis comparison, mirrored after flip) ---
    if handedness_label == "Right":
        fingers.append(1 if lm[TIP_IDS[0]].x < lm[MCP_IDS[0]].x else 0)
    else:
        fingers.append(1 if lm[TIP_IDS[0]].x > lm[MCP_IDS[0]].x else 0)

    # --- FINGERS 2-5  (Y-axis: tip above base = open) ---
    for i in range(1, 5):
        fingers.append(1 if lm[TIP_IDS[i]].y < lm[MCP_IDS[i]].y else 0)

    return fingers.count(1)


# ============================================================
#  GESTURE CONTROL  (rewritten with stability & cooldown)
# ============================================================
def gesture_control():
    speak("Gesture control started. Show your hand!")

    mp_hands = mp.solutions.hands
    mp_draw  = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Camera not found. Please check your camera.")
        return

    # ---- Settings ----
    COOLDOWN    = 2.5   # seconds between actions
    BUFFER_SIZE = 12    # frames collected before deciding
    MIN_CONFIRM = 10    # frames needed to confirm gesture

    last_action_time = 0
    gesture_buffer   = []

    # ---- Action map: finger count → function ----
    ACTION_MAP = {
        5: lambda: open_app("chrome"),
        4: lambda: open_app("word"),
        3: lambda: open_app("excel"),
        2: lambda: open_app("powerpoint"),
        1: lambda: open_app("calculator"),
        0: find_location_safe,
    }

    LABELS = {
        5: "Open Chrome",
        4: "Open Word",
        3: "Open Excel",
        2: "Open PowerPoint",
        1: "Open Calculator",
        0: "Show Location",
    }

    while True:
        success, img = cap.read()
        if not success:
            speak("Camera read failed")
            break

        # Mirror image so it feels natural
        img      = cv2.flip(img, 1)
        h, w, _  = img.shape
        imgRGB   = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results  = hands.process(imgRGB)

        if results.multi_hand_landmarks and results.multi_handedness:
            for handLms, handInfo in zip(
                results.multi_hand_landmarks,
                results.multi_handedness
            ):
                # Draw hand skeleton
                mp_draw.draw_landmarks(
                    img, handLms, mp_hands.HAND_CONNECTIONS
                )

                label = handInfo.classification[0].label   # "Left" or "Right"
                total = count_fingers(handLms, label)

                # Fill stability buffer
                gesture_buffer.append(total)
                if len(gesture_buffer) > BUFFER_SIZE:
                    gesture_buffer.pop(0)

                # Find most common count in buffer
                stable     = max(set(gesture_buffer), key=gesture_buffer.count)
                confidence = gesture_buffer.count(stable)
                action_lbl = LABELS.get(stable, "Unknown")

                # ---- Draw HUD ----
                cv2.rectangle(img, (0, 0), (w, 85), (0, 0, 0), -1)
                cv2.putText(img,
                    f"Fingers : {stable}",
                    (12, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 100), 2)
                cv2.putText(img,
                    f"Action  : {action_lbl}  ({confidence}/{BUFFER_SIZE})",
                    (12, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 255, 255), 2)

                # ---- Draw individual finger status ----
                finger_names = ["T", "I", "M", "R", "P"]
                lm = handLms.landmark
                fingers_state = []
                if label == "Right":
                    fingers_state.append(1 if lm[TIP_IDS[0]].x < lm[MCP_IDS[0]].x else 0)
                else:
                    fingers_state.append(1 if lm[TIP_IDS[0]].x > lm[MCP_IDS[0]].x else 0)
                for i in range(1, 5):
                    fingers_state.append(1 if lm[TIP_IDS[i]].y < lm[MCP_IDS[i]].y else 0)

                for idx, (fname, fstate) in enumerate(zip(finger_names, fingers_state)):
                    color = (0, 255, 0) if fstate else (0, 0, 255)
                    cv2.circle(img, (20 + idx * 30, h - 30), 10, color, -1)
                    cv2.putText(img, fname,
                        (14 + idx * 30, h - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (255, 255, 255), 1)

                # ---- Trigger action ----
                now = time.time()
                if (len(gesture_buffer) == BUFFER_SIZE and
                    confidence >= MIN_CONFIRM and
                    now - last_action_time > COOLDOWN and
                    stable in ACTION_MAP):

                    ACTION_MAP[stable]()
                    last_action_time = now
                    gesture_buffer.clear()

        else:
            gesture_buffer.clear()
            cv2.putText(img,
                "No hand detected — show your hand",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (0, 80, 255), 2)

        # ---- Cooldown progress bar ----
        elapsed = time.time() - last_action_time
        bar_pct = min(elapsed / COOLDOWN, 1.0)
        bar_w   = int(w * bar_pct)
        cv2.rectangle(img, (0, h - 12), (w, h), (50, 50, 50), -1)
        cv2.rectangle(img, (0, h - 12), (bar_w, h), (0, 200, 100), -1)
        cv2.putText(img, "Press ESC to exit",
            (w - 155, h - 16),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
            (180, 180, 180), 1)

        cv2.imshow("PROTON Gesture Control", img)
        if cv2.waitKey(1) == 27:   # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()


# ============================================================
#  VOICE COMMAND
# ============================================================
def voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening")
        audio = r.listen(source)
    try:
        cmd = r.recognize_google(audio).lower()
        add_message("You", cmd)
        process_command(cmd)
    except Exception:
        speak("Sorry, I did not understand that")


# ============================================================
#  PROCESS COMMAND
# ============================================================
def process_command(cmd):
    global sleep_mode

    if sleep_mode and "wake" not in cmd:
        return

    if "chrome"       in cmd: open_app("chrome")
    elif "word"       in cmd: open_app("word")
    elif "excel"      in cmd: open_app("excel")
    elif "powerpoint" in cmd: open_app("powerpoint")
    elif "calculator" in cmd: open_app("calculator")
    elif "time"       in cmd: show_time()
    elif "date"       in cmd: show_date()

    elif "location"   in cmd:
        place = cmd.replace("location", "").strip()
        if place:
            webbrowser.open("https://www.google.com/maps/search/" + place)
        else:
            find_location_safe()

    elif "copy"       in cmd: copy_text()
    elif "paste"      in cmd: paste_text()

    elif "gesture"    in cmd:
        threading.Thread(target=gesture_control, daemon=True).start()

    elif "sleep"      in cmd:
        sleep_mode = True
        speak("Going to sleep")

    elif "wake"       in cmd:
        sleep_mode = False
        speak("I am ready")

    elif "exit"       in cmd or "quit" in cmd:
        speak("Goodbye!")
        root.destroy()

    else:
        search_internet(cmd)


# ============================================================
#  CHAT BUBBLE
# ============================================================
def add_message(sender, msg):
    bubble_frame = tk.Frame(chat_frame, bg="#0F172A")
    color        = "#3B82F6" if sender == "You" else "#1E293B"

    bubble = tk.Label(
        bubble_frame,
        text=msg,
        wraplength=240,
        justify="left",
        padx=12, pady=8,
        fg="white",
        bg=color,
        font=("Arial", 10)
    )

    if sender == "You":
        bubble.pack(anchor="e")
        bubble_frame.pack(anchor="e", fill="x", pady=4, padx=5)
    else:
        bubble.pack(anchor="w")
        bubble_frame.pack(anchor="w", fill="x", pady=4, padx=5)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)


# ============================================================
#  SEND MESSAGE
# ============================================================
def send_message():
    msg = entry.get().strip().lower()
    if msg == "" or msg == "enter text":
        return
    entry.delete(0, tk.END)
    add_message("You", msg)
    process_command(msg)


# ============================================================
#  GUI SETUP
# ============================================================
root = tk.Tk()
root.title("PROTON Virtual Assistant")
root.geometry("360x600")
root.configure(bg="#0F172A")

# Header
tk.Label(
    root,
    text="🟢  PROTON Virtual Assistant",
    bg="black",
    fg="#00FF7F",
    font=("Arial", 13, "bold")
).pack(fill="x", pady=(0, 2))

# Gesture guide label
guide_text = (
    "Virtual Assistant"
)
tk.Label(
    root,
    text=guide_text,
    bg="#0F172A",
    fg="#94A3B8",
    font=("Arial", 8),
    justify="left"
).pack(fill="x", padx=8)

# Scrollable chat area
container = tk.Frame(root, bg="#0F172A")
container.pack(fill="both", expand=True)

canvas    = tk.Canvas(container, bg="#0F172A", highlightthickness=0)
scrollbar = tk.Scrollbar(container, command=canvas.yview)
chat_frame = tk.Frame(canvas, bg="#0F172A")

chat_window = canvas.create_window((0, 0), window=chat_frame, anchor="nw")


def resize_chat(event):
    canvas.itemconfig(chat_window, width=event.width)


canvas.bind("<Configure>", resize_chat)
chat_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left",  fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Input area
input_frame = tk.Frame(root, bg="#0F172A")
input_frame.pack(fill="x", padx=10, pady=6)

entry = tk.Entry(input_frame, font=("Arial", 12), fg="gray")
entry.insert(0, "Enter text")
entry.pack(side="left", fill="x", expand=True, padx=(0, 5))


def clear_placeholder(event):
    if entry.get() == "Enter text":
        entry.delete(0, tk.END)
        entry.config(fg="black")


entry.bind("<FocusIn>", clear_placeholder)
entry.bind("<Return>", lambda e: send_message())

btn_style = {
    "fg": "white",
    "font": ("Arial", 11, "bold"),
    "width": 3,
    "bd": 0,
    "cursor": "hand2"
}

tk.Button(input_frame, text="▶",  bg="#16A34A",
          command=send_message, **btn_style).pack(side="left", padx=3)

tk.Button(input_frame, text="🎤", bg="#3B82F6",
          command=lambda: threading.Thread(
              target=voice_command, daemon=True).start(),
          **btn_style).pack(side="left", padx=3)

tk.Button(input_frame, text="✋", bg="#F59E0B",
          command=lambda: threading.Thread(
              target=gesture_control, daemon=True).start(),
          **btn_style).pack(side="left", padx=3)

# Welcome messages
add_message("PROTON", "Hello! 😊 I am PROTON. How can I help you?")
add_message("PROTON", "Type, speak 🎤, or use hand gestures ✋")

root.mainloop()
