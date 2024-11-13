from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np


class Train:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("face Recogniton System")

        title_lbl=Label(self.root,text="Train Data Set" , font=("Baskerville Old Face", 30, "bold"), bg="white", fg="#4682B4")
        title_lbl.place(x=0,y=0,width=1530,height=60)

        bg_image = Image.open(r"college_images\img.png").resize((1600, 900), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        gif_image = Image.open(r"college_images\project11.gif")
        gif_photo = ImageTk.PhotoImage(gif_image)
        gif_label = Label(self.root, image=gif_photo)
        gif_label.image = gif_photo  # Keep a reference to avoid garbage collection
        gif_label.pack(pady=(200, 20))

        # 3rd - Text below the Lottie animation
        text_label = Label(self.root, text="Click below to register yourself!", font=("Arial", 18), bg="white",
                           fg="black")
        text_label.pack()

        #============== button==========================
        b1_1=Button(self.root,text="TRAIN DATA",command=self.train_classifier,cursor="hand2",font=("times new roman",18,"bold"),bg="white",fg="black")
        b1_1.place(x=630, y=430,width =250,height=60)






    def train_classifier(self):
        data_dir= "data"
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]

        faces=[]
        ids=[]

        for image in path:
            img=Image.open(image).convert('L')   #Grey scale image
            imageNp=np.array(img,'uint8')
            id=int(os.path.split(image)[1].split('.')[1])

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids=np.array(ids)



        #===================== Train the classifier And save =============
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training datasets completed!!!")








if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()



  