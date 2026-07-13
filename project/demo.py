from tkinter import *

win = Tk()


win.title("Arpan085 WEATHER")
win.iconbitmap("project\image\weather image.png")


win.config(background= "blue")

win.geometry("500x500")

Name_label = Label(win, text="Weather App",
                   font=("Time New Roman",40,"bold"))
Name_label.place(x=25,y=50,height=50,width=450)

win.mainloop()