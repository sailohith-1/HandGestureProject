# Virtual Keyboard – Hand Gesture Typing System

A real-time computer vision project that enables users to interact with a virtual keyboard using hand gestures captured through a webcam. Built with Python, OpenCV, and MediaPipe, the system uses hand landmark detection and fingertip tracking to recognize user interactions.

## Overview

Traditional keyboards require physical contact. This project explores a touch-free alternative by tracking hand movements in real time and translating recognized gestures into keyboard interactions.

The webcam captures hand movements, MediaPipe detects hand landmarks, and OpenCV processes the video stream to support gesture-based interaction with a virtual keyboard.

## Key Features

- **Real-Time Hand Tracking:** Detects and tracks hand landmarks using MediaPipe.
- **Fingertip Detection:** Identifies fingertip positions for interaction with virtual keys.
- **Gesture Recognition:** Uses hand movements and recognized gestures to trigger keyboard interactions.
- **Virtual Keyboard Interface:** Provides a visual keyboard for selecting keys through hand gestures.
- **Live Webcam Processing:** Processes video frames to support interactive, real-time input.

## Architecture

```text
         Webcam Video Feed
                 |
                 v
       OpenCV Frame Processing
                 |
                 v
      MediaPipe Hand Detection
                 |
                 v
       Hand Landmark Extraction
                 |
                 v
       Fingertip / Gesture Logic
                 |
                 v
       Virtual Keyboard Interaction
                 |
                 v
          Text Input Output
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| OpenCV | Webcam capture and video-frame processing |
| MediaPipe | Hand landmark detection and tracking |
| NumPy | Numerical operations, if used in the implementation |

## How It Works

1. **Capture:** The webcam captures live video frames.
2. **Process:** OpenCV reads and processes the frames.
3. **Detect:** MediaPipe identifies the hand and estimates its landmarks.
4. **Track:** The application tracks fingertip positions and evaluates gestures.
5. **Interact:** The recognized interaction selects a virtual key and produces text input, according to the implemented gesture logic.

## Getting Started

### Prerequisites

- Python 3.x
- A working webcam
- pip

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the placeholders with your actual repository URL and folder name.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

Install the libraries used by your project:

```bash
pip install opencv-python mediapipe numpy
```

If your project has a `requirements.txt` file, use:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Run the main Python script from the project root. For example:

```bash
python main.py
```

Replace `main.py` with the actual entry-point filename in your project.

Allow webcam access if prompted. Follow the gestures supported by your implementation to interact with the virtual keyboard.

## Potential Applications

- Touch-free computer interaction
- Human-computer interaction research
- Assistive input interfaces
- Gesture-controlled interfaces

## Future Improvements

- Add customizable keyboard layouts and shortcuts.
- Improve gesture recognition accuracy and reduce accidental key presses.
- Add support for additional hand gestures.
- Optimize frame processing for lower latency.
- Improve accessibility and support for different input requirements.

## Learning Outcomes

This project demonstrates practical experience with computer vision, real-time video processing, hand landmark detection, gesture-based interaction, and human-computer interaction.
