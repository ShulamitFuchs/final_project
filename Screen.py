import tkinter as tk
import subprocess
from PIL import ImageTk, Image
from VirtuEye import *


tracker = EyeTracker()

class EyeControl:
    def __init__(self,start_program=True):
        self.root = tk.Tk()
        self.root.title("Eye Control")
        self.root.configure(bg="white")

        # משתנה לבדיקה האם צריך להריץ מצב עיניים
        self.running=True


        # קביעת גודל החלון לפי גודל המסך
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        print(screen_width,screen_height)
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")


        if start_program:
            # תמונת לוגו
            your_image = Image.open("Logo\mmm.png")
            # גודל התמונה
            your_image = your_image.resize((400, 200))
            your_image = ImageTk.PhotoImage(your_image)
            # בחלק הימני של המסך
            your_image_label_left = tk.Label(self.root, image=your_image, bg=self.root["bg"])
            your_image_label_left.place(x=0, y=0)
            # בחלק שמאלי של המסך
            your_image_label_right = tk.Label(self.root, image=your_image, bg=self.root["bg"])
            your_image_label_right.place(x=1100, y=0)
            # כותרת המסך
            title_label = tk.Label(self.root, text="Eye Control", font=("Arial", 40), bg="white")
            title_label.pack(padx=30, pady=(80, 0)) 

            # יצירת כפתור לכניסה למקלדת
            left_button = tk.Button(
                self.root,
                text="Keyboard",
                bg="#333333",
                fg="white",
                font=("Arial", 50),
                relief="raised",
                borderwidth=8,
                padx=55,
                pady=55,
                command=self.run_keyboard,
            )
            left_button.pack(side="left", padx=150, pady=(0, 20))

            # יצירת כפתור ליציאה ממצב עיניים
            right_button = tk.Button(
                self.root,
                text="Close Eye Control",
                bg="dark green",
                fg="white",
                font=("Arial", 35),
                borderwidth=8,
                padx=35,
                pady=75,
                command=self.close_control_eye,
            )
            right_button.pack(side="right", padx=150, pady=(0, 20))

            self.root.after(200, self.run_script)

            # הפעלת לולאת התגובה
            self.root.mainloop()

    # סגירת המסך
    def close_window(self):
        # עצירת הלולאה של הפעלת המסך
        self.root.quit()  
        self.root.destroy()


    # הרצת מצב עיניים
    def run_script(self):
        if self.running is True:
            # מריצה את מצב העיניים מהמופע שיצרתי מהמחלקה של מצב העיניים
            tracker.run()
            print("hhhhh")
            # מריצה שוב כמו לולאה את מצב העיניים
            self.root.after(200, self.run_script)
        else:
            # יציאה ממצב עיניים
            tracker.stop()
            # פתיחת המקלדת
            subprocess.Popen(['python', 'Keyboard.py'])


    # כשלוחצים על מקלדת מגיע לכאן
    def run_keyboard(self):
        # מסמן לעצור מצב עיניים
        self.running=False
        print("false")


    # כשלוחץ ליציאה ממצב עיניים מגיע לכאן ויוצא
    def close_control_eye(self):
        exit()



if __name__ == "__main__":
    eye=EyeControl()



































##### לא במחלקה עובד טוב ברוך ד'
# import tkinter as tk
# import subprocess
# from PIL import ImageTk, Image
# # from pynput.mouse import Button,Controller,Listener
# # mouse=Controller()
# from VirtuEye import *
# # import n

# # process=None
# running= True

# tracker = EyeTracker()

# def run_script():
#     global running
#     if running is True:
#     # while True:
#         # mouse.position=(1140,600)
#         tracker.run()
#         # root.update()
#         # if running is False:
#         print("hhhhh") 
#         root.after(200, run_script)
#     else:
#         tracker.stop()
#         subprocess.Popen(['python', 'Keyboard.py'])

#         # key = cv2.waitKey(1)
#         # if key == 27:
#         #     pass



# # פונקציה שתופעל כאשר הכפתור הימני ילחץs


# def run_keyboard():
#     global running
#     running=False
#     print("false")
#     # tracker.stop()


#     # tracker.finalize()
#     # tracker.thread.join()
#     # tracker.stop()
#     # os.system('python keyboard5.py')
#     # subprocess.Popen(['python', 'keyboard5.py'])
# def on_click(x, y, button, pressed):
#         if pressed:
#             print(f"Mouse clicked at ({x}, {y})")

# # פונקציה שתופעל כאשר הכפתור השמאלי ילחץ
# def close_control_eye():
#     with Listener(on_click=on_click) as listener:
#         pass
#     exit()

# def handle_click(event):
#     # get the mouse position
#     mouse_pos = f"({event.x}, {event.y})"

#     # update the label with the mouse position

#     # print the mouse position to the console
#     print(f"Mouse clicked at {mouse_pos}")


# # יצירת חלון ראשי
# root = tk.Tk()
# root.title("Eye Control")
# root.configure(bg="white")
# # הגדרת כותרת החלון

# # קביעת גודל החלון לפי גודל המסך
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# print(screen_width,screen_height)
# root.geometry(f"{screen_width}x{screen_height}+0+0")



# # יצירת כותרת גדולה בחלק העליון של המסך
# your_image = Image.open("Logo\mmm.png")  # Replace with your own image path
# your_image = your_image.resize((400, 200))
# your_image = ImageTk.PhotoImage(your_image)
# # root.update()
# # Create a label to display your image in the upper left part of the screen
# your_image_label_left = tk.Label(root, image=your_image, bg=root["bg"])
# your_image_label_left.place(x=0, y=0)
# # Create a label to display your image in the upper right part of the screen
# your_image_label_right = tk.Label(root, image=your_image, bg=root["bg"])
# your_image_label_right.place(x=1100, y=0)
# # Creating a label with the header and design
# title_label = tk.Label(root, text="Eye Control", font=("Arial", 40), bg="white")
# title_label.pack(padx=30, pady=(80, 0))  # lower margin height larger

# # יצירת כפתור גדול בצד השמאלי של המסך
# left_button = tk.Button(
#     root,
#     text="Keyboard",
#     bg="dark gray",
#     fg="white",
#     font=("Arial", 50),
#     relief="raised",
#     borderwidth=8,
#     padx=55,
#     pady=55,
#     command=run_keyboard,
# )
# left_button.pack(side="left", padx=150, pady=(0, 20))

# # יצירת כפתור גדול בצד הימני של המסך
# right_button = tk.Button(
#     root,
#     text="Close Eye Control",
#     bg="dark green",
#     fg="white",
#     font=("Arial", 35),
#     borderwidth=8,
#     padx=35,
#     pady=75,
#     command=close_control_eye,
# )
# right_button.pack(side="right", padx=150, pady=(0, 20))
# # root.bind("<Button-1>", handle_click)

# root.after(200, run_script)

# # הרצת לולאת התצוגה
# root.mainloop()
