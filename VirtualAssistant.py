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
from geopy.geocoders import Nominatim

# ---------- VOICE ----------
engine = pyttsx3.init()
engine.setProperty("rate",170)
sleep_mode=False

def speak(text):
    add_message("PROTON", text)
    engine.say(text)
    engine.runAndWait()

# ---------- OPEN APPS ----------
def open_app(name):
    try:
        if name=="chrome":
            os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
        elif name=="word":
            os.startfile("winword")
        elif name=="excel":
            os.startfile("excel")
        elif name=="powerpoint":
            os.startfile("powerpnt")
        elif name=="calculator":
            os.startfile("calc")
        speak("Opening "+name)
        time.sleep(2)
    except:
        speak("App not found")

# ---------- DATE & TIME ----------
def show_time():
    speak("Time is "+datetime.datetime.now().strftime("%H:%M"))

def show_date():
    speak("Date is "+datetime.datetime.now().strftime("%Y-%m-%d"))

# ---------- LOCATION ----------
def find_location_safe():
    root.after(0, ask_location_popup)

def ask_location_popup():
    place = askstring("PROTON", "Enter Location", parent=root)
    if place:
        speak("Finding " + place)
        webbrowser.open("https://www.google.com/maps/search/" + place)

# ---------- COPY PASTE ----------
def copy_text():
    pyautogui.hotkey("ctrl","c")
    speak("Copied")

def paste_text():
    pyautogui.hotkey("ctrl","v")
    speak("Pasted")

# ---------- INTERNET SEARCH ----------
def search_internet(query):
    try:
        result = wikipedia.summary(query,2)
        speak(result)
    except:
        speak("Searching Google")
        webbrowser.open("https://www.google.com/search?q="+query)

# ---------- GESTURE CONTROL ----------
def gesture_control():
    speak("Gesture started")

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    cap = cv2.VideoCapture(0)

    tipIds=[4,8,12,16,20]

    while True:
        success,img = cap.read()
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                fingers=[]

                if handLms.landmark[4].x < handLms.landmark[3].x:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1,5):
                    if handLms.landmark[tipIds[id]].y < handLms.landmark[tipIds[id]-2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total=fingers.count(1)

                if total==5: open_app("chrome")
                elif total==4: open_app("word")
                elif total==3: open_app("excel")
                elif total==2: open_app("powerpoint")
                elif total==1: open_app("calculator")
                elif total==0: find_location_safe()

        cv2.imshow("PROTON Gesture",img)
        if cv2.waitKey(1)==27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------- VOICE COMMAND ----------
def voice_command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening")
        audio=r.listen(source)
    try:
        cmd=r.recognize_google(audio).lower()
        add_message("You",cmd)
        process_command(cmd)
    except:
        speak("Not understood")

# ---------- COMMAND PROCESS ----------
def process_command(cmd):
    global sleep_mode

    if sleep_mode and "wake" not in cmd:
        return

    if "chrome" in cmd: open_app("chrome")
    elif "word" in cmd: open_app("word")
    elif "excel" in cmd: open_app("excel")
    elif "powerpoint" in cmd: open_app("powerpoint")
    elif "calculator" in cmd: open_app("calculator")
    elif "time" in cmd: show_time()
    elif "date" in cmd: show_date()

    elif "location" in cmd:
        place = cmd.replace("location","").strip()
        if place:
            webbrowser.open("https://www.google.com/maps/search/" + place)
        else:
            find_location_safe()

    elif "copy" in cmd: copy_text()
    elif "paste" in cmd: paste_text()

    elif "gesture" in cmd:
        threading.Thread(target=gesture_control).start()

    elif "sleep" in cmd:
        sleep_mode=True
        speak("Sleeping")

    elif "wake" in cmd:
        sleep_mode=False
        speak("I am ready")

    elif "exit" in cmd:
        speak("Goodbye")
        root.destroy()

    else:
        search_internet(cmd)

# ---------- CHAT MESSAGE (BUBBLE STYLE) ----------
def add_message(sender,msg):

    bubble_frame=tk.Frame(chat_frame,bg="#0F172A")

    color="#3B82F6" if sender=="You" else "#1E293B"

    bubble=tk.Label(
        bubble_frame,
        text=msg,
        wraplength=240,
        justify="left",
        padx=12,
        pady=8,
        fg="white",
        bg=color,
        font=("Arial",10)
    )

    if sender=="You":
        bubble.pack(anchor="e")
        bubble_frame.pack(anchor="e",fill="x",pady=4,padx=5)
    else:
        bubble.pack(anchor="w")
        bubble_frame.pack(anchor="w",fill="x",pady=4,padx=5)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# ---------- SEND MESSAGE ----------
def send_message():
    msg=entry.get().lower()

    if msg=="enter text":
        return

    entry.delete(0,tk.END)
    add_message("You",msg)
    process_command(msg)

# ---------- WINDOW ----------
root=tk.Tk()
root.title("PROTON Virtual Assistant")
root.geometry("360x600")
root.configure(bg="#0F172A")

tk.Label(root,
text="🟢 PROTON Welcomes you!",
bg="black",
fg="#00FF7F",
font=("Arial",14,"bold")).pack(fill="x")

# ---------- SCROLLABLE CHAT ----------
container=tk.Frame(root,bg="#0F172A")
container.pack(fill="both",expand=True)

canvas=tk.Canvas(container,bg="#0F172A",highlightthickness=0)
scrollbar=tk.Scrollbar(container,command=canvas.yview)

chat_frame=tk.Frame(canvas,bg="#0F172A")

chat_window=canvas.create_window((0,0),window=chat_frame,anchor="nw")

def resize_chat(event):
    canvas.itemconfig(chat_window,width=event.width)

canvas.bind("<Configure>",resize_chat)

chat_frame.bind(
"<Configure>",
lambda e:canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left",fill="both",expand=True)
scrollbar.pack(side="right",fill="y")

# ---------- INPUT AREA ----------
input_frame=tk.Frame(root,bg="#0F172A")
input_frame.pack(fill="x",padx=10,pady=5)

entry=tk.Entry(input_frame,font=("Arial",12),fg="gray")
entry.insert(0,"Enter text")
entry.pack(side="left",fill="x",expand=True,padx=(0,5))

def clear_placeholder(event):
    if entry.get()=="Enter text":
        entry.delete(0,tk.END)
        entry.config(fg="black")

entry.bind("<FocusIn>",clear_placeholder)
entry.bind("<Return>",lambda e:send_message())

btn_style={
"fg":"white",
"font":("Arial",11,"bold"),
"width":3,
"bd":0,
"cursor":"hand2"
}

tk.Button(input_frame,text="▶",bg="#16A34A",command=send_message,**btn_style).pack(side="left",padx=3)

tk.Button(input_frame,text="🎤",bg="#3B82F6",
command=lambda:threading.Thread(target=voice_command).start(),
**btn_style).pack(side="left",padx=3)

tk.Button(input_frame,text="✋",bg="#F59E0B",
command=lambda:threading.Thread(target=gesture_control).start(),
**btn_style).pack(side="left",padx=3)

# ---------- START MESSAGE ----------
add_message("PROTON","Hello Pushpa 😊")
add_message("PROTON","I am Proton. How can I help you?")

root.mainloop()