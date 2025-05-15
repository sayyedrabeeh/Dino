import cv2
import mediapipe as mp
import pyautogui
import time
import pygetwindow as gw
import win32gui
import win32con
import numpy as np 

cv2.namedWindow("Hand Gesture Control")
dummy_frame = 255 * np.ones((100, 100, 3), dtype=np.uint8)
cv2.imshow("Hand Gesture Control", dummy_frame)
cv2.waitKey(1)
try:
    hwnd = gw.getWindowsWithTitle("Hand Gesture Control")[0]._hWnd
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 640, 480, 0)
except Exception as e:
    print("⚠️ Could not set window always on top:", e)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
last_press_time = 0
cooldown = 0.5  
while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1) 
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            tip_y = hand_landmarks.landmark[8].y
            base_y = hand_landmarks.landmark[6].y
            if tip_y > base_y and (time.time() - last_press_time > cooldown):
                pyautogui.click(x=600, y=300)  
                pyautogui.press('space') 
                print("🕹️ Jump triggered!")
                last_press_time = time.time()
    cv2.imshow("Hand Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
