from tkinter import *

from tkinter import ttk

win = Tk()


win.title("Arpan085 WEATHER")
win.iconbitmap("project\image\weather image.png")


win.config(background= "blue")

win.geometry("500x500")

Name_label = Label(win, text="Weather App",
                   font=("Time New Roman",40,"bold"))
Name_label.place(x=25,y=50,height=50,width=450)


list_name = [
    "Koshi",
    "Madhesh",
    "Bagmati",
    "Gandaki",
    "Lumbini",
    "Karnali",
    "Sudurpashchim"
]
 




com = ttk.Combobox(win, text="Weather App",values= list_name,
                   font=("Time New Roman",20,"bold"))

com.place(x=25,y=120,height=50,width=450)


done_button = Button(win, text="DONE",
                   font=("Time New Roman",20,"bold"))

done_button.place(x=200,y=190,height=50,width=50)



















win.mainloop()