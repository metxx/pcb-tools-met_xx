from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen',True)
canvas = Canvas(root, width = 1920, height = 1080)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("to_display.png"))  
canvas.create_image(0, 0, anchor=NW, image=img) 
root.mainloop() 

