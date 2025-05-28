# Hand Gesture Controlled Air Drawing

A real-time hand gesture recognition system using MediaPipe and OpenCV, allowing users to draw in the air with simple gestures detected by a webcam.

## Project Overview

This project turns your hand into a virtual pen. By recognizing specific hand gestures, the system allows you to:

- Start or stop drawing  
- Change brush colour  
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

```

## Run the Application
```bash 
python air_draw.py

```
Press q to quit the application.

## Output Example
When you show 4 fingers, the current canvas will be saved as an image (e.g., drawing_1716922123.png) in the same directory.

## Future Enhancements
- Add support for undo and redo functionality

- Implement multi-hand support

- Introduce gesture sequences for advanced actions

- Integrate with voice controls or speech feedback

## About

This is a personal project by Aakash Kathirvel, built to explore gesture-based human-machine interaction systems using computer vision and artificial intelligence.

Feel free to connect or contribute.  
LinkedIn: [https://www.linkedin.com/in/aakash-k-382a14208/)


