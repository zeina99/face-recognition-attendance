import tkinter as tk
from PIL import ImageTk, Image
import pickle
import os
import cv2 as cv
import os.path
import time
import sys
from train import *
from recogizer import *
import record_attendance
from record_attendance import attendance_record

class OurGui(tk.Tk):  # main class that has the main window

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="icon.ico")  # makes new icon
        self.resizable(width=False, height=False)  # makes it so that window size cant be changed
        self.geometry('800x600')  # sets size of window to 800x600
        self.title('camera gui')  # makes title camera gui
        window = tk.Frame(self)  # sets a new frame with the name window

        window.pack(side="top", fill="both", expand=True)  # this is to but window in the self frame

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        self.frames = {}  # to store the all the different pages we have

        for F in (MainMenu, AddStudent, ErrorMessage, Instruction, CameraAdd,
                  WaitPage):  # puts the different pages in the frames tuple if a page is added put its name here
            frame = F(window, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)  # starts the main page

    def show_frame(self, cont):  # is called upon when there is change from one page to another
        frame = self.frames[cont]
        frame.tkraise()


class MainMenu(tk.Frame):  # class that has the main page and all of it content

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def clicked_bt():  # this button will go to face recognition system so call it from here
            recog = Recognize()
            recog.read_training_data()
            recognized_names = recog.recognize()
            print(recognized_names)

            #mark attendance on excel sheet
            record = attendance_record()
            record.take_attendance(recognized_names_list=recognized_names)

        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(side="top", fill="both")  # define top frame and pack it

        mid_frame = tk.Frame(self, bg="white", padx=50, pady=120)
        mid_frame.pack(fill="both")  # define middle frame and pack it

        toolbar = tk.Frame(self, bg="white")
        toolbar.pack(side="bottom", fill="both")  # toolbar and pack it

        buid = "buid.png"  # load img directory into var
        img = ImageTk.PhotoImage(file=buid)  # load img into new var
        panel = tk.Label(top_frame, image=img, bg="white")
        panel.image = img
        panel.pack(side="top")  # make new label loads img into it and pack it

        welcome = tk.Label(top_frame, text="welcome to our face attendance system", bg="white", fg="blue", height=4,
                           width=20,
                           font=("Helvetica", 20))
        welcome.pack(side="bottom", fill="both", expand="yes")  # makes new label and pack it

        bt = tk.Button(mid_frame, text="Add student", bg="white", fg="blue", height=4, width=20, font="bold",
                       command=lambda: controller.show_frame(AddStudent))
        bt.pack(side="left", padx=40)  # makes button that goes to add_student page and pack it

        bt1 = tk.Button(mid_frame, text="take attendance", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: clicked_bt())
        bt1.pack(side="right", padx=40)  # makes button that goes to face recognition page and pack it

        bt4 = tk.Button(toolbar, text="exit", bg="white", fg="blue", height=3, width=15, font="bold",
                        command=lambda: sys.exit())
        bt4.pack(padx=10, pady=10)


class AddStudent(tk.Frame):  # class that has the Add_student page and all of it content

    def bt2_action(self, controller, name, field_name):  # a button that when pressed will show error if the name exists and if
        # it does not it will create a new dir with that name an go to instruction page
        pickle.dump(name, open("name.pkl", "wb"))
        path = f"Faces/{name}"
        if os.path.exists(path):
            controller.show_frame(ErrorMessage)
        else:
            os.makedirs(path)
            pickle.dump(path, open("path.pkl", "wb"))
            field_name.delete(0, "end")
            controller.show_frame(Instruction)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(side="top", fill="both")  # define top frame and pack it

        mid_frame = tk.Frame(self, bg="white", padx=270, pady=150)
        mid_frame.pack(fill="both")  # define middle frame and pack it

        toolbar = tk.Frame(self, bg="white")
        toolbar.pack(side="bottom", fill="both")  # toolbar and pack it

        buid = "buid.png"
        img = ImageTk.PhotoImage(file=buid)
        panel = tk.Label(top_frame, image=img, bg="white")
        panel.image = img
        panel.pack(side="top")

        todo = tk.Label(top_frame, text="Please enter the name of the new student", bg="white", fg="blue", height=4,
                        width=20,
                        font=("Helvetica", 20))
        todo.pack(side="bottom", fill="both", expand="yes")
        name = tk.StringVar()  # var to store entry field_name

        def limitname(*args):  # function to limit the size of field_name to 20 characters
            value = name.get()
            if len(value) > 20: name.set(value[:20])

        name.trace('w', limitname)  # calls limitname
        name_label = tk.Label(mid_frame, text="Name: ", bg="white", fg="blue", font="bold")
        name_label.grid(row=0, column=0)  # define label and put it in grid format row 0 col 0
        field_name = tk.Entry(mid_frame, bg="gray90", font="bold", textvariable=name)
        field_name.grid(row=0, column=1, sticky="w")  # define name entry and put it in grid format row 0 col 1

        bt3 = tk.Button(toolbar, text="<- back", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: controller.show_frame(MainMenu))
        bt3.pack(side="left", padx=10, pady=10)  # define button that goes back to main menu page
        bt4 = tk.Button(toolbar, text="next ->", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: self.bt2_action(controller, name.get(), field_name))
        bt4.pack(side="right", padx=10, pady=10)  # define button that goes does bt2_action


class ErrorMessage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        root = tk.Frame(self, bg="white")
        root.pack(side="top", fill="both")  # define a frame and pack it

        buid = "buid.png"
        img = ImageTk.PhotoImage(file=buid)
        panel = tk.Label(root, image=img, bg="white")
        panel.image = img
        panel.pack(side="top")

        error_label = tk.Label(root, text="this name already exist please enter a new name", bg="white",
                               fg="blue",
                               font=("Helvetica", 20), pady=220)
        error_label.pack()  # label that tells the user they encountered error
        bt4 = tk.Button(root, text="<- back", bg="white", fg="blue", height=3, width=15, font="bold",
                        command=lambda: controller.show_frame(AddStudent))
        bt4.pack(padx=10, pady=10)  # a button that if pressed will take you back to Addstudent page


class Instruction(tk.Frame):

    def bt3_action(self, controller):
        path = pickle.load(open("path.pkl", "rb"))
        os.rmdir(path)
        controller.show_frame(AddStudent)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(side="top", fill="both")  # define top frame and pack it

        toolbar = tk.Frame(self, bg="white")
        toolbar.pack(side="bottom", fill="both")  # toolbar and pack it

        buid = "buid.png"
        img = ImageTk.PhotoImage(file=buid)
        panel = tk.Label(top_frame, image=img, bg="white")
        panel.image = img
        panel.pack(side="top")

        instruction_label = tk.Label(top_frame,
                                     text="in the next page you will have to take 4 pictures\n of yourself for face "
                                          "identification you will\n be doing this by pressing the button 4 times",
                                     bg="white",
                                     fg="blue",
                                     font=("Helvetica", 20), pady=180)
        instruction_label.pack()  # label that will tell user how to take picture and pack it

        bt3 = tk.Button(toolbar, text="<- back", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: self.bt3_action(controller))
        bt3.pack(side="left", padx=10, pady=10)  # define button that goes back to main menu page
        bt4 = tk.Button(toolbar, text="next ->", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: controller.show_frame(CameraAdd))
        bt4.pack(side="right", padx=10, pady=10)  # define button that goes does CameraAdd


class CameraAdd(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        root = tk.Frame(self, bg="white")
        root.pack(side="top", fill="both")  # define a frame and pack it

        toolbar = tk.Frame(self, bg="white")
        toolbar.pack(side="bottom", fill="both")  # toolbar and pack it

        bt6 = tk.Button(toolbar, text="open camera", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: self.bt6_action(root, toolbar, controller, bt6))
        bt6.pack(side="left", padx=10, pady=10)  # define button that takes picture

    def bt6_action(self, root, toolbar, controller, bt6):
        bt6.destroy()
        lmain = tk.Label(root)
        lmain.pack()  # label that has the video stream inside it
        bt3 = tk.Button(toolbar, text="take picture", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: self.bt4_action(root, toolbar, controller, lmain, bt3))
        bt3.pack(side="right", padx=10, pady=10)  # define button that takes picture

        # Capture from camera
        cap = cv.VideoCapture(0)

        # function for video streaming
        def video_stream():  # I had to use this workaround to make opencv2 work with tkinter
            _, self.frame = cap.read()
            cv2image = cv.cvtColor(self.frame, cv.COLOR_RGB2BGR)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream)

        video_stream()  # calls video streaming


    def bt4_action(self,root, toolbar, controller, lmain, bt3):  # a button that will take a picture of the frame then name it the same time it
        # was taken and checks if there is more the 4 pictures in the file if there is go back to MainMenu
        name = pickle.load(open("name.pkl", "rb"))
        timestr = time.strftime("%Y%m%d-%H%M%S")
        img_name = f"Faces/{name}/{timestr}.png"
        cv.imwrite(img_name, self.frame)
        path = pickle.load(open("path.pkl", "rb"))
        num_files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        if num_files > 3:
            wait_var = 1
            pickle.dump(wait_var, open("wait.pkl", "wb"))
            lmain.destroy()
            bt3.destroy()
            bt6 = tk.Button(toolbar, text="open camera", bg="white", fg="blue", height=4, width=20, font="bold",
                            command=lambda: self.bt6_action(root, toolbar, controller, bt6))
            bt6.pack(side="left", padx=10, pady=10)  # define button that takes picture
            controller.show_frame(WaitPage)


class WaitPage(tk.Frame):

    def bt5_action(self, controller):
        tray = Train()
        tray.train_latest_student()
        controller.show_frame(MainMenu)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        root = tk.Frame(self, bg="white")
        root.pack(side="top", fill="both")  # define top frame and pack it

        toolbar = tk.Frame(self, bg="white")
        toolbar.pack(side="bottom", fill="both")  # toolbar and pack it

        buid = "buid.png"
        img = ImageTk.PhotoImage(file=buid)
        panel = tk.Label(root, image=img, bg="white")
        panel.image = img
        panel.pack(side="top")

        error_label = tk.Label(root, text="press the button and wait a few moments\n for the data training to finish",
                               bg="white",
                               fg="blue",
                               font=("Helvetica", 20), pady=200)
        error_label.pack()  # label that tells the user they encountered error
        # faisal put your face training code here

        bt5 = tk.Button(toolbar, text="train", bg="white", fg="blue", height=4, width=20, font="bold",
                        command=lambda: self.bt5_action(controller))
        bt5.pack(padx=10, pady=10)  # define button that goes back to main menu page



app = OurGui()  # calls main application
app.mainloop()  # keeps window open
