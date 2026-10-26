import cv2
import mediapipe as mp
import math

# ---------------- Mediapipe Setup ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# ---------------- Keyboard Layout ----------------
keys = [["1","2","3","4","5","6","7","8","9","0"],
        ["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L"],
        ["Z","X","C","V","B","N","M","SPACE","<--"]]

# Special keys positioned separately
special_keys = [["ENTER"]]  # ENTER key spans middle and bottom rows

key_w, key_h = 80, 80
gap = 15
start_x, start_y = 50, 150

typed_text = ""
clicking = False

# ---------------- Draw Keyboard ----------------
def draw_keyboard(img, fingertip):
    pressed_key = None
    
    # Draw main keyboard keys
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = start_x + j*(key_w + gap)
            y = start_y + i*(key_h + gap)
            
            # Determine key color based on position
            if key == "H":
                # H key is pink/magenta like other keys, only green when pressed
                key_color = (147, 20, 255)  # Pink/Magenta
                text_color = (255, 255, 255)  # White text
            else:
                # All other keys are pink/magenta
                key_color = (147, 20, 255)  # Pink/Magenta
                text_color = (255, 255, 255)  # White text
            
            # Highlight if fingertip inside
            if fingertip and x < fingertip[0] < x+key_w and y < fingertip[1] < y+key_h:
                cv2.rectangle(img, (x,y), (x+key_w, y+key_h), (0,255,0), -1)
                cv2.putText(img, key, (x+15,y+50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                pressed_key = key
            else:
                cv2.rectangle(img, (x,y), (x+key_w, y+key_h), key_color, -1)
                cv2.putText(img, key, (x+15,y+50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
    
    # Draw ENTER key (spans middle and bottom rows, positioned to the right of L)
    enter_x = start_x + 9*(key_w + gap)  # Position after the L key
    enter_y = start_y + 1*(key_h + gap)  # Start from middle row
    enter_w = key_w
    enter_h = 2*key_h + gap  # Height of two rows
    
    # ENTER key is green
    if fingertip and enter_x < fingertip[0] < enter_x+enter_w and enter_y < fingertip[1] < enter_y+enter_h:
        cv2.rectangle(img, (enter_x,enter_y), (enter_x+enter_w, enter_y+enter_h), (0,255,0), -1)
        cv2.putText(img, "ENTER", (enter_x+5,enter_y+enter_h//2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        pressed_key = "ENTER"
    else:
        cv2.rectangle(img, (enter_x,enter_y), (enter_x+enter_w, enter_y+enter_h), (0,255,0), -1)
        cv2.putText(img, "ENTER", (enter_x+5,enter_y+enter_h//2+10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    
    return img, pressed_key

# ---------------- Camera Setup ----------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img,1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    fingertip, middle_tip = None, None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = img.shape
            # Index finger tip
            x1 = int(hand_landmarks.landmark[8].x * w)
            y1 = int(hand_landmarks.landmark[8].y * h)
            fingertip = (x1,y1)

            # Middle finger tip
            x2 = int(hand_landmarks.landmark[12].x * w)
            y2 = int(hand_landmarks.landmark[12].y * h)
            middle_tip = (x2,y2)

            # Draw skeleton 
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw solid green circle on index finger
            cv2.circle(img, fingertip, 15, (0,255,0), -1)   # Solid green

            # Draw solid blue circle on middle finger
            cv2.circle(img, middle_tip, 15, (255,0,0), -1)  # Solid blue

    # Draw keyboard
    img, pressed_key = draw_keyboard(img, fingertip)
    
    # Detect key press (pinch = click)
    if fingertip and middle_tip and pressed_key:
        dist = math.hypot(fingertip[0]-middle_tip[0], fingertip[1]-middle_tip[1])

        if dist < 35 and not clicking:
            if pressed_key == "<--":
                typed_text = typed_text[:-1]
            elif pressed_key == "SPACE":
                typed_text += " "
            elif pressed_key == "ENTER":
                # ENTER key does nothing for now, just for display
                pass
            else:
                typed_text += pressed_key
            clicking = True

        elif dist > 50:
            clicking = False

    # Display typed text area
    cv2.rectangle(img, (50,50), (900,120), (255,255,255), -1)
    y_offset = 100
    for line in typed_text.split("\n"):
        cv2.putText(img, line, (60,y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,0), 3)
        y_offset += 50
    
    # Add keyboard cursor (blinking underscore) to show current typing position
    import time
    cursor_blink = int(time.time() * 2) % 2  # Blink every 0.5 seconds
    if cursor_blink:
        # Find the last line and add cursor after the last character
        if typed_text:
            last_line = typed_text.split("\n")[-1]
            # Get exact text width using OpenCV's getTextSize for precise cursor positioning
            (text_width, text_height), baseline = cv2.getTextSize(last_line, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
            cursor_x = 60 + text_width  # Exact position after the text
            cursor_y = y_offset - 50
        else:
            cursor_x = 60
            cursor_y = 100
        
        cv2.putText(img, "|", (cursor_x, cursor_y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,0), 3)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
