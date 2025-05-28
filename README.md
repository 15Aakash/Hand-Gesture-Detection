# Hand Gesture Controlled Air Drawing

A real-time hand gesture recognition system using MediaPipe and OpenCV, allowing users to draw in the air with simple gestures detected by a webcam.

## Project Overview

This project turns your hand into a virtual pen. By recognizing specific hand gestures, the system allows you to:

- Start or stop drawing  
- Change brush color  
- Change brush thickness  
- Clear the screen  
- Save your drawing as an image  

All of this is achieved with a standard webcam and no physical input device.

## How It Works

- MediaPipe detects hand landmarks and identifies finger positions.
- A gesture recognition function determines the number of fingers raised.
- Each gesture (based on the number of fingers) is mapped to a specific action.
- A canvas overlays the live webcam feed to display the drawing in real time.

## Gesture Controls

| Fingers Shown | Action           |
|---------------|------------------|
| 1             | Start Drawing    |
| 0             | Stop Drawing     |
| 2             | Toggle Thickness |
| 3             | Change Color     |
| 4             | Save Drawing     |
| 5             | Clear Canvas     |

Consecutive frame validation is used to avoid accidental triggers of commands.

## Technologies Used

- Python  
- OpenCV  
- MediaPipe  
- NumPy  

## Getting Started

### Prerequisites

Install the required libraries:

```bash
pip install opencv-python mediapipe numpy
