from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkFont
from playsound import playsound

#------------------------------------------------------------------------------
#     
# Note: 
#   It's important that this code *not* interact directly with tkinter 
#   stuff in the main process since it doesn't support multi-threading.
import itertools
import os
import shutil
import threading
import time


number = 0

filepaths = []
for subdir, dirs, files in os.walk('./images'):
    for file in files:
        filepath = subdir + os.sep + file
        filepaths.append(filepath)

num_images = len(filepaths)

def sound(pitido):
    if pitido:
        playsound("./sound.mp3", False)

def update_image_file(dst):
    """ Overwrite (or create) destination file by copying successive image 
        files to the destination path. Runs indefinitely. 
    """
    TEST_IMAGES = filepaths

    for src in itertools.cycle(TEST_IMAGES):
        shutil.copy(src, dst)
        time.sleep(.5)  # pause between updates
            
    
        
#------------------------------------------------------------------------------

def refresh_image(canvas, img, image_path, image_id):
    try:
        pil_img = Image.open(image_path).resize((700,700), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(image_id, image=img)
    except IOError:  # missing or corrupt image file
        img = None
    # repeat every half sec
    canvas.after(5000, refresh_image, canvas, img, image_path, image_id)  

root = tk.Tk()
root.attributes('-fullscreen', True)
image_path = './1.jpg'

#------------------------------------------------------------------------------
# More code to simulate background process periodically updating the image file.

th = threading.Thread(target=update_image_file, args=(image_path,))
th.daemon = True  # terminates whenever main thread does
th.start()
while not os.path.exists(image_path):  # let it run until image file exists
    time.sleep(.1)


#------------------------------------------------------------------------------

def key(event):
    global number
    kp = repr(event.num)
    print ("pressed", kp) #repr(event.char))
    if (kp == "1"):
        print("number: ", number)
        number += 1
        if number > 99:
            number = 0
        numero.config(text=number, fg="yellow")
        numero.config(text=number, fg="white")
        #sound(True)
    if (kp == "3"):
        print("number: ", number)
        number -= 1
        if number < 0:
            number = 99
        numero.config(text=number, fg="yellow")
        numero.config(text=number, fg="white")
        #sound(True)

#------------------------------------------------------------------------------

canvas_width = 1920
canvas_height = 1080
w = canvas_width // 2
h = canvas_height // 2
colorBG = "black"
colorFG = "white"

canvas = tk.Canvas(root, bg=colorBG, height = canvas_height, width=canvas_width, highlightthickness=0)
#canvas.pack(fill=tk.BOTH, expand=False)


#-----------------------------------FONTS-------------------------------------
fontStyle = tkFont.Font(family= 'Arial', size=60 )
fontStyle2 = tkFont.Font(family= 'Arial', size=400 )
#-----------------------------------------------------------------------------

#---------------------------------INORMATION---------------------------------
fm1 = tk.Frame(root, bg=colorBG)
text1 = tk.Label(fm1, text="Carniceria Luján", font=fontStyle,fg=colorFG, bg = colorBG).pack()
fm1.pack(side='top', padx=0, pady=0, fill="both")
#-----------------------------------------------------------------------------
#text.config(font=('Helvetica bold',4000))
#line = canvas.create_line(10, 10, 100, 35, fill="red")

#----------------------------------NUMBER-------------------------------------
fm1 = tk.Frame(root, bg=colorBG)

text3 = tk.Label(fm1, text=u"🠗 Su turno 🠗", font=fontStyle,fg=colorFG, bg = colorBG).pack(pady=(300,0), padx=(0,50))
numero = tk.Label(fm1, text=number, font=fontStyle2,fg=colorFG, bg = colorBG)
numero.pack(anchor="center", padx=(0,30))
fm1.pack(side='right', padx=0, pady=0, fill="both")

frame = canvas.bind_all("<Button>", key)
#-----------------------------------------------------------------------------


# IMAGEN
canvas.pack(fill=tk.BOTH, expand=True)
img = None  # initially only need a canvas image place-holder
image_id = canvas.create_image(400, h-100, image=img)

refresh_image(canvas, img, image_path, image_id)
#-----------------------------------------------------------------------------

root.mainloop()
