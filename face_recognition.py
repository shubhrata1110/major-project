import csv
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np
# from lottie import LottieAnimation
from tkinterweb import HtmlFrame
import tkinter as tk



class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("face Recogniton System")


        title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="Black",fg="White")
        title_lbl.place(x=0,y=0,width=1530,height=55)

        # # Load the GIF image
        # self.gif_image = Image.open(r"college_images\project11.gif")
        #
        # # Initialize a label to display the GIF
        # self.gif_label = Label(self.root)
        # self.gif_label.pack(pady=(55, 10))
        #
        # # Add the text label below the GIF
        # text_label = tk.Label(self.root, text="This is some text below the GIF",
        #                            font=("times new roman", 18, "bold"))
        # text_label.pack(pady=(10, 10))
        #
        # # Start the animation
        # self.animate_gif(0)

        # 1st - Background Image
        bg_image = Image.open(r"college_images\img.png").resize((1600, 900), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image =self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        gif_image = Image.open(r"college_images\project11.gif")
        gif_photo = ImageTk.PhotoImage(gif_image)
        gif_label = Label(self.root, image=gif_photo)
        gif_label.image = gif_photo  # Keep a reference to avoid garbage collection
        gif_label.pack(pady=(200,20))

        # 3rd - Text below the Lottie animation
        text_label = Label(self.root, text="Click below to register yourself!", font=("Arial", 18), bg="white", fg="black")
        text_label.pack()

        # Button below the text
        b1_1 = Button(self.root, text="Face Recognition", command=self.face_recog, cursor="hand2",
                      font=("times new roman", 18, "bold"), bg="white", fg="black")
        b1_1.pack(pady=(10, 0))

    # def animate_gif(self, frame):
    #     # Get the next frame of the GIF
    #     self.gif_image.seek(frame)
    #
    #     # Convert the current frame to PhotoImage
    #     gif_photo = ImageTk.PhotoImage(self.gif_image)
    #
    #     # Update the label with the new frame
    #     self.gif_label.config(image=gif_photo)
    #     self.gif_label.image = gif_photo  # Keep a reference
    #
    #     # Update to the next frame, looping back to 0 if the end is reached
    #     next_frame = (frame + 1) % self.gif_image.n_frames
    #     self.root.after(100, self.animate_gif, next_frame)



    # =========================attendance==============================

    def mark_attendance(self,i,r,n,d):
        with open("abhishek.csv", "r+", newline="") as f:
            reader = csv.reader(f)
            existing_entries = list(reader)

            # Check if an entry with (i, r, n, d) already exists
            if not any(row[:4] == [i, r, n, d] for row in existing_entries):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")

                # Write the new attendance entry
                writer = csv.writer(f)
                writer.writerow([i, r, n, d, dtString, d1, "Present"])

    # ======================face recognition ===================

    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

            coord=[]

            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])
                confidence=int((100*(1-predict/300)))

                conn=mysql.connector.connect(host="localhost",user="root",password="@Abhiveer18",database="major", auth_plugin='mysql_native_password')
                my_cursor=conn.cursor()
                
                my_cursor.execute("select Name from student where Student_id="+str(id))
                n=my_cursor.fetchone()
                n = str(n)

                my_cursor.execute("select Roll from student where Student_id="+str(id))
                r=my_cursor.fetchone()
                r = str(r)

                my_cursor.execute("select Dep from student where Student_id="+str(id))
                d=my_cursor.fetchone() 
                d = str(d)

                my_cursor.execute("select Student_id from student where Student_id="+str(id))
                i=my_cursor.fetchone()
                i = str(i)

                if confidence>77:
                    cv2.putText(img,f"ID:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Department:{d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(i,r,n,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                
                coord=[x,y,w,y]

            return coord

        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img

        faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap=cv2.VideoCapture(0)

        while True:
            ret,img=video_cap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Welcome To face Recognition",img)

            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()           
















if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()