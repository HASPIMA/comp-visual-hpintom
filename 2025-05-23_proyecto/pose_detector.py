# pose_detector.py
import time
from mediapipe.python.solutions.pose import PoseLandmark

class PoseDetector:
    def __init__(self):
        self.last_pose = None
        self.last_pose_time = 0
        self.menu_hold_start = None
        self.menu_hold_duration = 1.5

    def detect_action(self, landmarks):
        current_time = time.time()

        left_shoulder = landmarks[PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[PoseLandmark.RIGHT_SHOULDER.value]
        nose = landmarks[PoseLandmark.NOSE.value]
        left_wrist = landmarks[PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[PoseLandmark.RIGHT_WRIST.value]
        left_knee = landmarks[PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[PoseLandmark.RIGHT_KNEE.value]

        torso_x = (left_shoulder.x + right_shoulder.x) / 2
        torso_y = (left_shoulder.y + right_shoulder.y) / 2

        # LEFT/RIGHT tilt
        if right_shoulder.x - left_shoulder.x > 0.16:
            return "left"
        elif left_shoulder.x - right_shoulder.x > 0.16:
            return "right"

        # JUMP (both hands near knees)
        hands_near_knees = (
            abs(left_wrist.y - left_knee.y) < 0.1 and
            abs(right_wrist.y - right_knee.y) < 0.1
        )
        if hands_near_knees:
            return "x"

        # Z: arm lifted above head
        if left_wrist.y < nose.y or right_wrist.y < nose.y:
            return "z"

        # MENU: standing still, arms down
        arms_down = (
            left_wrist.y > left_shoulder.y + 0.15 and
            right_wrist.y > right_shoulder.y + 0.15
        )
        posture_straight = abs(left_shoulder.y - right_shoulder.y) < 0.05

        if arms_down and posture_straight:
            if self.menu_hold_start is None:
                self.menu_hold_start = current_time
            elif current_time - self.menu_hold_start > self.menu_hold_duration:
                return "menu"
        else:
            self.menu_hold_start = None

        return None
