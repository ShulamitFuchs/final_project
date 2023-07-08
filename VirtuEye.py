import cv2
import dlib
import numpy as np
import mediapipe as mp
from pynput.mouse import Button,Controller,Listener


class EyeTracker:
    def __init__(self):
        # עבטר המקלדת
        self.mouse =Controller()

        # משתנה בשביל החלקת העכבר
        self.smoothing_factor = 0.9
        # מיקום המיקומים הקודמים של העכבר בשביל ההחלקה
        self.prev_mouse_x = None
        self.prev_mouse_y = None


        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # התחברות למצלמה (אינדקס 0 ברירת מחדל)
        self.cap = cv2.VideoCapture(0)

        # גודל המסך
        self.screen_w, self.screen_h = 1920, 1080

        #נקודת אמצע של מסך המכשיר
        self.screen_center_x, self.screen_center_y = self._calculate_screen_center(
            self.screen_w, self.screen_h
        )

        # עבור כמה פריימים מצמץ
        self.blinking_frames = 0
        # כמות הפריימים שאמור למצמץ
        self.frames_to_blink = 6



        # self._get_blinking()

    # פונקציה לחישוב נקודת אמצע
    def _calculate_screen_center(self, width, height):
        center_x = width // 2
        center_y = height // 2
        return center_x, center_y

    # פונקציה לחישוב ממוצע בין שתי נקודות
    def _midpoint(self, p1, p2):
        return int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)

    # פונקציה לחישוב המלבן העוטף את העין
    def _calculate_eye_width_height(self, points,frame):
        #  נקודות המרכז העליון והתחתון
        center_top = self._midpoint(points[1], points[2])
        center_bottom = self._midpoint(points[4], points[5])
        cv2.rectangle(frame,(points[0][0]+10,center_top[1]-5),(points[3][0]-1,center_bottom[1]),(255,0,0),2)
        # גובהה ורוחב מלבן העוטף את העין
        height = center_bottom[1] - center_top[1]+5
        width = points[3][0]-1 - points[0][0]-10
        #נקודת מרכז המלבן העוטף את העין
        center_x = (points[0][0]+7 + points[3][0]-1) // 2
        center_y = (center_top[1]-2 + center_bottom[1]+1) // 2
        cv2.circle(frame,(center_x,center_y),2,(255,0,0))
        # cv2.imshow("Frame", frame)

        return width, height, center_x, center_y

    # פונקציה המקבלת אתת מספרי הפנים ומחזירה מערך עם 6 נקודות בשביל חישוב המלבן
    def _eyes_contour_points(self, facial_landmarks):
        # An array to save the eye points
        right_eye = []
        for n in range(42, 48):
            x = facial_landmarks.part(n).x
            y = facial_landmarks.part(n).y
            right_eye.append({"x": x, "y": y})
        right_eye = np.array(
            [[point["x"], point["y"]] for point in right_eye], np.int32
        )
        return right_eye

    # פונקציה המחשבת לפי אחוזים את המיקום החדש של העכבר
    def _new_point_screen(self, width_rec, height_rec, how_pix_move_x, how_pix_move_y):
        if how_pix_move_x < 0:
            Percent_x_rec = int(
                (((how_pix_move_x * -1) * 100) // (width_rec // 2)) *2
            )
            new_point_screen_x = self.screen_center_x - (
                (Percent_x_rec * (self.screen_w // 2)) // 100
            )
        else:
            Percent_x_rec = int(((how_pix_move_x * 100) // (width_rec // 2)) *1.5)
            new_point_screen_x = self.screen_center_x + (
                ((self.screen_w // 2 * Percent_x_rec) // 100)
            )
        if how_pix_move_y < 0:
            Percent_y_rec = int(
                (((how_pix_move_y * -1) * 100) // (height_rec // 2))
            )
            new_point_screen_y = self.screen_center_y - (
                (Percent_y_rec * (self.screen_h // 2)) // 100
            )
        else:
            Percent_y_rec = int(((how_pix_move_y * 100) // (height_rec // 2)) )
            new_point_screen_y = self.screen_center_y + (
                (Percent_y_rec * (self.screen_h // 2)) // 100
            )
        return new_point_screen_x, new_point_screen_y


    def run(self):

        print("true")
        # קורא פריים מהמצלמה
        _, frame = self.cap.read()
        # הופך שיהיה כמו מראה
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = self.face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        faces = self.detector(gray)
        landmarks_68 = -1

        for face in faces:
            landmarks_68 = self.predictor(gray, face)
            # אם מצא פנים...
            if landmarks_68 != -1:
                # שליחה לקבלת מערך של מיקומי נקודות עין ימין
                right_eye = self._eyes_contour_points(landmarks_68)
                # cv2.rectangle(
                #     frame,
                #     (landmarks_68.part(42).x, landmarks_68.part(43).y - 4),
                #     (landmarks_68.part(45).x, landmarks_68.part(46).y + 3),
                #     (0, 0, 255),
                #     2,
                # )
                # cv2.imshow("Frame", frame)
                # שליחה לקבלת גובה רוחב ונקודת אמצע של המלבן העוטף את העין
                (
                    width_rec,
                    height_rec,
                    pic_center_rec_x,
                    pic_center_rec_y,
                ) = self._calculate_eye_width_height(right_eye,frame)

        if landmark_points:
            # הפנים הראשונות שמוצא
            landmarks_468 = landmark_points[0].landmark
            # מיקום האישון על ידי 4 נקודות (המרכז שלהם)
            center_iris_x, center_iris_y = int(landmarks_468[475].x * frame_w), int(
                landmarks_468[474].y * frame_h
            )
            # cv2.circle(frame, (pic_center_rec_x, pic_center_rec_y), 2, (0, 0, 255))

            cv2.circle(frame, (center_iris_x, center_iris_y), 2, (255, 255, 255))
            # cv2.imshow("Frame", frame)

            # בודק בכמה פיקסלים זז האישון מנקודת מרכז המלבן העוטף את העין
            how_pix_move_x = center_iris_x - pic_center_rec_x
            how_pix_move_y = center_iris_y - pic_center_rec_y

            # שליחה לחישוב מה המיקום של העכבר על המסך ביחס למלבן העוטף את העין
            new_point_mouse_pos = self._new_point_screen(
                width_rec, height_rec, how_pix_move_x, how_pix_move_y
            )

            # החלקת העכבר על המסך שלא יזוז בצורה אגרסיבית
            if self.prev_mouse_x is not None and self.prev_mouse_y is not None:
                smoothed_mouse_x = self.smoothing_factor * self.prev_mouse_x + (1 - self.smoothing_factor) * new_point_mouse_pos[0]
                smoothed_mouse_y = self.smoothing_factor * self.prev_mouse_y + (1 - self.smoothing_factor) * new_point_mouse_pos[1]
                new_point_mouse_pos = (smoothed_mouse_x, smoothed_mouse_y)
            self.mouse.position = (round(new_point_mouse_pos[0]), round(new_point_mouse_pos[1]))
            # מעדכן את מיקום המסך הקודם
            self.prev_mouse_x, self.prev_mouse_y = new_point_mouse_pos

            # בדיקב האם ממצמץ באופן משמעותי
            left = [landmarks_468[145], landmarks_468[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if left[0].y - left[1].y < 0.006:
                self.blinking_frames += 1
                if self.blinking_frames == self.frames_to_blink:
                    self.blinking_frames = 0
                    print("enter")
                    self.mouse.press(Button.left)
                    self.mouse.release(Button.left)


        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1)
        # if key == 27:
        #     break
        # self.cap.release()
        # cv2.destroyAllWindows()

    def stop(self):
        self.cap.release()


# tracker = EyeTracker()
# while True:
#     tracker.run()