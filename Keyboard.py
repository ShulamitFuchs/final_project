import cv2
import numpy as np
import dlib
from math import hypot
import mediapipe as mp
from Screen import *
import pyglet

# עבור צלילים
sound = pyglet.media.load("sound.wav", streaming=False)
left_sound = pyglet.media.load("left.wav", streaming=False)
right_sound = pyglet.media.load("right.wav", streaming=False)

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# התחברות למצלמה
cap = cv2.VideoCapture(0)

board = np.zeros((300, 1400), np.uint8)
board[:] = 255

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# הגדרת גודל מסך המקלדת
keyboard = np.zeros((600, 1200, 3), np.uint8)

# צד שמאלי של המקלדת
keys_set_1 = {
    0: "Q",
    1: "W",
    2: "E",
    3: "R",
    4: "T",
    5: "->",
    6: "A",
    7: "S",
    8: "D",
    9: "F",
    10: "G",
    11: "~",
    12: "Z",
    13: "X",
    14: "C",
    15: "V",
    16: "<",
    17: "^",
}
# צד ימני של המקלדת
keys_set_2 = {
    0: "Y",
    1: "U",
    2: "I",
    3: "O",
    4: "P",
    5: "->",
    6: "H",
    7: "J",
    8: "K",
    9: "L",
    10: "_",
    11: "~",
    12: "V",
    13: "B",
    14: "N",
    15: "M",
    16: "<",
    17: "^",
}

# מיקומי האותיות על גבי המסך והגדרת הגודל והגופן
def draw_letters(letter_index, text, letter_light):
    # Keys
    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 200
        y = 0
    elif letter_index == 2:
        x = 400
        y = 0
    elif letter_index == 3:
        x = 600
        y = 0
    elif letter_index == 4:
        x = 800
        y = 0
    elif letter_index == 5:
        x = 1000
        y = 0
    elif letter_index == 6:
        x = 0
        y = 200
    elif letter_index == 7:
        x = 200
        y = 200
    elif letter_index == 8:
        x = 400
        y = 200
    elif letter_index == 9:
        x = 600
        y = 200
    elif letter_index == 10:
        x = 800
        y = 200
    elif letter_index == 11:
        x = 1000
        y = 200
    elif letter_index == 12:
        x = 0
        y = 400
    elif letter_index == 13:
        x = 200
        y = 400
    elif letter_index == 14:
        x = 400
        y = 400
    elif letter_index == 15:
        x = 600
        y = 400
    elif letter_index == 16:
        x = 800
        y = 400
    elif letter_index == 17:
        x = 1000
        y = 400

    width = 200
    height = 200
    th = 3  # thickness

    # Text settings
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y

    if letter_light is True:
        cv2.rectangle(
            keyboard,
            (x + th, y + th),
            (x + width - th, y + height - th),
            (255, 255, 255),
            -1,
        )
        cv2.putText(
            keyboard,
            text,
            (text_x, text_y),
            font_letter,
            font_scale,
            (51, 51, 51),
            font_th,
        )
    else:
        cv2.rectangle(
            keyboard,
            (x + th, y + th),
            (x + width - th, y + height - th),
            (51, 51, 51),
            -1,
        )
        cv2.putText(
            keyboard,
            text,
            (text_x, text_y),
            font_letter,
            font_scale,
            (255, 255, 255),
            font_th,
        )


# מסך left and right
def draw_menu():
    rows, cols, _ = keyboard.shape
    th_lines = 4  # thickness lines
    cv2.line(
        keyboard,
        (int(cols / 2) - int(th_lines / 2), 0),
        (int(cols / 2) - int(th_lines / 2), rows),
        (51, 51, 51),
        th_lines,
    )
    cv2.putText(keyboard, "LEFT", (80, 300), font, 6, (255, 255, 255), 5)
    cv2.putText(
        keyboard, "RIGHT", (80 + int(cols / 2), 300), font, 6, (255, 255, 255), 5
    )


# חישוב ממוצע
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


font = cv2.FONT_HERSHEY_PLAIN


# פןנקציה לחישוב המצמוץ
def get_blinking_ratio(rgb_frame):
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    ratio = None
    if landmark_points:
        landmarks_med = landmark_points[0].landmark
        left = [landmarks_med[145], landmarks_med[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        ratio = left[0].y - left[1].y
    return ratio



# מחזיר שתי מערכים אחד עם מיקומוי נקודת עין ימין והשני עם מיקומי נקודות עבור עין שמאל
def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye


# פונקציה לחישוב יחס המבט
def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array(
        [
            (
                facial_landmarks.part(eye_points[0]).x,
                facial_landmarks.part(eye_points[0]).y,
            ),
            (
                facial_landmarks.part(eye_points[1]).x,
                facial_landmarks.part(eye_points[1]).y,
            ),
            (
                facial_landmarks.part(eye_points[2]).x,
                facial_landmarks.part(eye_points[2]).y,
            ),
            (
                facial_landmarks.part(eye_points[3]).x,
                facial_landmarks.part(eye_points[3]).y,
            ),
            (
                facial_landmarks.part(eye_points[4]).x,
                facial_landmarks.part(eye_points[4]).y,
            ),
            (
                facial_landmarks.part(eye_points[5]).x,
                facial_landmarks.part(eye_points[5]).y,
            ),
        ],
        np.int32,
    )
    # cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y:max_y, min_x:max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0:height, 0 : int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0:height, int(width / 2) : width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio


# Counters
frames = 0
#מספר מיקום האות
letter_index = 0
# בודק כמה פעמים מצמץ ברצף
blinking_frames = 0
# עד כמה אמור למצמץ
frames_to_blink = 6
#למשך כמה זמן יהיה דלוק האור על גבי המסך
frames_active_letter = 12
# מסמן האם לצאת מהלולאה
flag_exit = False

# הגדרות טקסט ומקלדת
text = ""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0

# לולאה אישית
while flag_exit is False:
    # לוקח פריים מהמצלמה
    _, frame = cap.read()
    # הופך שיהיה כמו מרה
    frame = cv2.flip(frame, 1)
    rows, cols, _ = frame.shape
    keyboard[:] = (26, 26, 26)

    frames += 1
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # מה יחס המצמוץ
    blinking_ratio = get_blinking_ratio(rgb_frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # מצייר את הסרגלים שבין האותיות (הרווחים)
    frame[rows - 50 : rows, 0:cols] = (255, 255, 255)


    # בודק האם צריך לצייר את מסך הימין והשמאל ,אם כן מצייר
    if select_keyboard_menu is True:
        draw_menu()

    # בודק אם זה שמאל לוקח את אותיות צד ימין
    if keyboard_selected == "left":
        keys_set = keys_set_1
    # אם זה שמאל לוקח של צד שמאל
    else:
        keys_set = keys_set_2
    active_letter = keys_set[letter_index]

    # Face detection
    faces = detector(gray)
    for face in faces:
        # if flag_exit is False:
        landmarks = predictor(gray, face)
        cv2.rectangle(
            frame,
            (landmarks.part(36).x, landmarks.part(38).y),
            (landmarks.part(39).x, landmarks.part(41).y),
            (0, 0, 255),
            2,
        )
        left_eye, right_eye = eyes_contour_points(landmarks)

        if select_keyboard_menu is True:

            # מחשב את יחס המבט אם מסתכל ימין או שמאל
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
            landmarks.part(36).x

            if gaze_ratio >= 1.5:
                keyboard_selected = "right"
                keyboard_selection_frames += 1
                # אם שמירת מבט בצד אחד יותר מ-15 פריימים, עבור למקלדת
                if keyboard_selection_frames == 18:
                    select_keyboard_menu = False
                    right_sound.play()
                    # הגדר את ספירת המסגרות ל-0 כאשר המקלדת נבחרה
                    frames = 0
                    keyboard_selection_frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0
            else:
                keyboard_selected = "left"
                keyboard_selection_frames += 1
                # אם שמירת מבט בצד אחד יותר מ-15 פריימים, עבור למקלדת
                if keyboard_selection_frames == 18:
                    select_keyboard_menu = False
                    left_sound.play()
                    # Set frames count to 0 when keyboard selected
                    frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0

        else:
            # מזהה האם ממצמץ מצמוץ משמעותי לבחירת האות הדלוקה
            if blinking_ratio < 0.006:
                # cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                blinking_frames += 1
                frames -= 1

                # Show green eyes when closed
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                # Typing letter
                if blinking_frames == frames_to_blink:
                    board_h, board_w = board.shape

                    if (
                        active_letter != "<"
                        and active_letter != "_"
                        and active_letter != "->"
                        and active_letter != "~"
                        and active_letter!="^"
                    ):
                        text += active_letter
                    if active_letter == "_":
                        text += " "
                    if active_letter == "~":
                        cv2.rectangle(
                            board, (0, 0), (board_w, board_h), (255, 255, 255), -1
                        )
                        text = text[:-1]
                    if active_letter=="^":
                        text=""
                        cv2.rectangle(
                            board, (0, 0), (board_w, board_h), (255, 255, 255), -1
                        )
                    if active_letter == "->":
                        flag_exit = True
  
                    sound.play()
                    select_keyboard_menu = True
                    # time.sleep(1)

            else:
                blinking_frames = 0

    # הצגת אותיות המקלדת
    if select_keyboard_menu is False:
        
        if frames == frames_active_letter:
            letter_index += 1
            frames = 0
        if letter_index == 18:
            letter_index = 0
        for i in range(18):
            if i == letter_index:
                light = True
            else:
                light = False
            draw_letters(i, keys_set[i], light)

    # כתיבת הטקסט על המסך
    cv2.putText(board, text, (80, 100), font, 4, 0, 2)

    # Blinking loading bar
    percentage_blinking = blinking_frames / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)

    # cv2.imshow("Frame", frame)
    cv2.imshow("Virtual keyboard", keyboard)
    cv2.imshow("Board", board)

    # if flag_exit is True:
    #     running = True
    #     break
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()

cv2.destroyAllWindows()
screen=EyeControl(start_program=True)
# screen.close_window()
# screen=EyeControl(start_program=True)

# screen.running=True
# screen.run_script()
# screen.close_window()
# screen.running=True
# screen.run_script()
