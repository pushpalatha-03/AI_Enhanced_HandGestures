# 🖱️ AI Virtual Mouse using Hand Gestures

## 📌 Project Description

This project implements an **AI-based Virtual Mouse System** that allows users to control the computer using **hand gestures captured through a webcam**. The system detects hand landmarks using MediaPipe and translates finger gestures into various computer control actions such as cursor movement, clicking, scrolling, brightness control, volume adjustment, and screenshots.

## ✨ Features

* 🖱️ Cursor movement using index finger
* 👆 Left click gesture
* 👉 Right click gesture
* ✌️ Double click gesture
* 🖐️ Drag and drop functionality
* 📑 Multi-select with gesture
* 📜 Scroll up and scroll down
* 🔆 Brightness increase and decrease
* 🔊 Volume up and volume down
* 🔇 Mute and unmute system sound
* 📸 Screenshot capture with preview
* 🖥️ Real-time gesture action display on screen

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* Screen Brightness Control
* Keyboard Library

## ⚙️ How the System Works

1. The webcam captures the user's hand movements in real time.
2. MediaPipe detects **hand landmarks and finger positions**.
3. The program identifies which fingers are raised.
4. Different finger combinations trigger specific system actions.
5. PyAutoGUI and system libraries execute mouse, keyboard, brightness, and volume controls.

## 🎯 Project Goal

The goal of this project is to develop a **touchless human-computer interaction system** that enables users to control computer operations using natural hand gestures.
# ⌨️ AI Virtual Keyboard using Hand Gestures

## 📌 Project Description

This project implements an **AI-based Virtual Keyboard** that allows users to type on a computer using **hand gestures detected through a webcam**. The system uses MediaPipe to track hand landmarks and identifies finger gestures to interact with a virtual keyboard displayed on the screen.

## ✨ Features

* ⌨️ On-screen virtual keyboard layout
* 🖐️ Hand gesture detection using webcam
* 👆 Finger pinch gesture to press keys
* 🔠 Support for uppercase and lowercase typing using Shift
* ⬅️ Backspace key functionality
* ↩️ Enter key support
* ␣ Space key support
* ⎋ Escape key support
* 🖥️ Real-time display of the last pressed key

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI

## ⚙️ How the System Works

1. The webcam captures the user's hand movement in real time.
2. MediaPipe detects hand landmarks and tracks finger positions.
3. A virtual keyboard is drawn on the screen using OpenCV.
4. When the user performs a **pinch gesture (thumb + index finger)** over a key, the system detects the key area.
5. The selected key is triggered and typed using PyAutoGUI.

## 🎯 Project Goal

The goal of this project is to develop a **touchless virtual typing system** that enables users to type using hand gestures without using a physical keyboard.
# 🎮 AI Gaming Control using Hand Gestures

## 📌 Project Description

This project implements an **AI-based Gaming Gesture Control System** that allows users to control computer games using **hand movements detected through a webcam**. The system uses MediaPipe to track hand landmarks and converts the position of the index finger into keyboard inputs for controlling game actions such as movement, jumping, and sliding.

## ✨ Features

* 🎮 Control games using hand gestures
* 👆 Index finger tracking for movement detection
* ⬅️ Move left gesture
* ➡️ Move right gesture
* ⬆️ Jump gesture
* ⬇️ Slide gesture
* 🚗 Continuous acceleration and braking control
* 🖥️ Real-time gesture detection and action display
* 📷 Webcam-based gesture recognition

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

## ⚙️ How the System Works

1. The webcam captures the user's hand movements in real time.
2. MediaPipe detects hand landmarks and tracks the **index finger position**.
3. The screen is divided into control zones.
4. Moving the finger to different zones triggers specific keyboard inputs such as **left, right, jump, or slide**.
5. These inputs control gameplay actions in compatible keyboard-based games.

## 🎯 Project Goal

The goal of this project is to create a **gesture-based gaming control system** that allows users to interact with games without using a physical keyboard.
# 🤖 PROTON – AI Virtual Assistant

## 📌 Project Overview

**PROTON** is a Python-based AI Virtual Assistant that allows users to interact with their computer using **voice commands, text input, and hand gestures**. The assistant provides real-time responses, performs system tasks, opens applications, searches the internet, and supports gesture-based controls using computer vision.

The project integrates **speech recognition, text-to-speech, GUI interaction, and hand gesture detection** to create an interactive assistant similar to modern smart assistants.

## ✨ Key Features

🎤 **Voice Command Recognition** – Control the assistant using spoken commands
⌨️ **Text Command Interface** – Send commands through a chat-style GUI
🖐 **Gesture Control** – Use hand gestures to launch applications
🌐 **Internet Search** – Fetch information from Wikipedia or Google
📍 **Location Finder** – Search locations using Google Maps
📂 **Application Launcher** – Open apps like Chrome, Word, Excel, PowerPoint, and Calculator
📋 **Clipboard Actions** – Perform copy and paste operations
🕒 **Date & Time Query** – Get current system time and date
💬 **Chat Interface** – Modern scrollable chat UI built using Tkinter
🔊 **Speech Response** – Assistant replies using text-to-speech

## 🛠️ Technologies Used

* **Python**
* **Tkinter** – GUI interface
* **OpenCV** – Webcam processing
* **MediaPipe** – Hand gesture detection
* **SpeechRecognition** – Voice command recognition
* **pyttsx3** – Text-to-speech engine
* **PyAutoGUI** – Keyboard automation
* **Wikipedia API** – Knowledge retrieval
* **Geopy** – Location services

## ⚙️ System Workflow

1. The user provides commands through **voice, text, or gestures**.
2. The system processes the input using **speech recognition or gesture detection**.
3. The assistant interprets the command and performs the requested action.
4. Responses are displayed in the **chat interface** and spoken through **text-to-speech**.

## 🎯 Project Objective

The goal of this project is to build a **multi-modal AI assistant** that enhances human-computer interaction by combining **voice, vision, and automation technologies**.

## 🚀 Future Enhancements

* Add **AI chatbot using LLMs (LLaMA / GPT)**
* Implement **smart home automation commands**
* Add **file management and system monitoring features**
* Deploy the assistant as a **desktop application**


