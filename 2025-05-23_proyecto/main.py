import time

import cv2
import keyboard
from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions.hands import (HAND_CONNECTIONS, HandLandmark,
                                              Hands)

CAMERA_INDEX = 0

# Create a video capture object.
# We can then use cap to read frames from the camera.
cap = cv2.VideoCapture(CAMERA_INDEX)

# Use the imported Hands class directly
hands = Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

while True:
    ret, frame = cap.read()  # capture the image from the webcam
    if not ret:
        break

    # media pipe works with RGB images, so we convert the BGR image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image_rgb)  # process the image to detect the hand

    if results.multi_hand_landmarks:  # type: ignore
        for hand_landmarks in results.multi_hand_landmarks:  # type: ignore

            # Draw hand landmarks on the image
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                list(HAND_CONNECTIONS)
            )

            thumb_tip = hand_landmarks.landmark[HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[HandLandmark.RING_FINGER_TIP]
            pinky_finger_tip = hand_landmarks.landmark[HandLandmark.PINKY_TIP]
            cv2.putText(
                frame,
                f"Thumb tip y: {round(thumb_tip.y, 2)}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                1,
            )
            cv2.putText(
                frame,
                f"Index finger tip y: {round(index_finger_tip.y, 2)}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                1,
            )
            cv2.putText(
                frame,
                f"Middle finger tip y: {round(middle_finger_tip.y, 2)}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                1
            )
            cv2.putText(
                frame,
                f"Ring finger tip y: {round(ring_finger_tip.y, 2)}",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                1
            )
            cv2.putText(
                frame,
                f"Pinky finger tip y: {round(pinky_finger_tip.y, 2)}",
                (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                1
            )
            is_hand_closed = (
                (index_finger_tip.y > thumb_tip.y) and
                (middle_finger_tip.y > thumb_tip.y) and
                (ring_finger_tip.y > thumb_tip.y) and
                (pinky_finger_tip.y > thumb_tip.y)
            )

            if is_hand_closed:
                print("Hand Closed")
                cv2.putText(
                    frame,
                    "Hand Closed",
                    (10, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    1
                )
            else:
                keyboard.press('space')
                print("Hand Open")
                cv2.putText(
                    frame,
                    "Hand Open",
                    (10, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    1
                )
                time.sleep(0.1)

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
