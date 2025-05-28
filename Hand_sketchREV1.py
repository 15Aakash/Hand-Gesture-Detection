import cv2
import numpy as np
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

consecutiveCheck = 0
count_fingers_value = 0
color_change = 0
thickness_change = 0
save_state = 0

#confidence kwarg changed to 0.9 to prevent accidental board clears.
hands = mp_hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9)
cap = cv2.VideoCapture(0)

tip_ids = [4, 8, 12, 16, 20]

canvas = None
draw_mode = False
prev_x, prev_y = None, None

# Color + Thickness Setup
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]  # Blue, Red, Green
color_index = 0
color = colors[color_index]
thickness = 4
is_thick = False

def check_gesture(finger_count):
    global consecutiveCheck, count_fingers_value, color_change, thickness_change, save_state
    if finger_count == count_fingers_value:
        consecutiveCheck += 1
        #special code to slow down the rate of change with the color changer
        if(finger_count == 3):
            if(color_change > 20):
                color_change=0
                return 1
            else:
                color_change +=1
                return 0
        #special code to down the rate of change with the thickness changer
        if(finger_count == 2):
            if(thickness_change > 20):
                thickness_change=0
                return 1
            else:
                thickness_change +=1
                return 0
        #special code to limit just 1 save everytime 4 fingers is detected
        if(finger_count == 4):
            if save_state !=1:
                save_state = 1
                return 1
            else:
                return 0
    else:
        save_state=0
        consecutiveCheck = 0
        count_fingers_value = finger_count
    return consecutiveCheck >= 3

def count_fingers(hand_landmarks, hand_label):
    fingers = []
    # Thumb
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[idx].classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = count_fingers(hand_landmarks, hand_label)

            h, w, _ = frame.shape
            cx = int(hand_landmarks.landmark[8].x * w)
            cy = int(hand_landmarks.landmark[8].y * h)

            if finger_count == 1:
                if check_gesture(1):
                    cv2.putText(frame, "DRAWING", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                    if prev_x is None or prev_y is None:
                        prev_x, prev_y = cx, cy  # Initialize
                    else:
                        distance = np.hypot(cx - prev_x, cy - prev_y)
                        if distance < 50:  # Avoid large jumps
                            cv2.line(canvas, (prev_x, prev_y), (cx, cy), color, thickness)
                        prev_x, prev_y = cx, cy
                    draw_mode = True

            elif finger_count == 2:
                if check_gesture(2):
                    is_thick = not is_thick
                    thickness = 8 if is_thick else 4
                    
                    cv2.putText(frame, f"THICKNESS {'HIGH' if is_thick else 'LOW'}", (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 200, 200), 3)
                    prev_x, prev_y = None, None

            elif finger_count == 0:
                if check_gesture(0):
                    cv2.putText(frame, "STOPPED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    draw_mode = False
                    prev_x, prev_y = None, None

            elif finger_count == 3:
                if check_gesture(3):
                    cv2.putText(frame, "COLOR CHANGED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 255), 3)
                    color_index = (color_index + 1) % len(colors)
                    color = colors[color_index]
                    prev_x, prev_y = None, None

            elif finger_count == 4:
                if check_gesture(4):
                    cv2.putText(frame, "SAVED", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    timestamp = int(time.time())
                    cv2.imwrite(f'drawing_{timestamp}.png', canvas)
                    prev_x, prev_y = None, None

            elif finger_count == 5:
                if check_gesture(5):
                    cv2.putText(frame, "CLEAR", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
                    canvas = np.zeros_like(frame)
                    draw_mode = False
                    prev_x, prev_y = None, None

    # Combine canvas with live feed
    combined = cv2.addWeighted(frame, 1, canvas, 1, 0)

    # Draw current color in top-right corner
    cv2.rectangle(combined, (560, 10), (630, 60), color, -1)

    cv2.imshow("Air Drawing", combined)

    #q is exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
