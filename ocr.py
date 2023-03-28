"""OCR read the text from a area screenshot using the dimensions drawn by the user."""

import easyocr
import tkinter as tk
from PIL import ImageTk, ImageGrab, ImageEnhance
import time
import os

reader = easyocr.Reader(["en"])

root = tk.Tk()
T = tk.Text(root, wrap="word")
T.pack(expand="yes", fill="both")
root.withdraw()  # hide the root window

temp_path = f"{os.path.dirname(__file__)}/temp_audio_files"


def ocr_read_image():
    """Extract text from an image and place it in a tkinter Text box."""
    T.delete("1.0", "end")

    T.insert("end", "Loading, please wait...")

    filename = f"{temp_path}/1_screenshot.png"

    result = reader.readtext(filename, detail=0, paragraph=True)

    result_string = "\n\n".join([x for x in result])

    T.delete("1.0", "end")

    T.insert("end", result_string)


def area_sel():
    """Capture an area screenshot of the area selected by the user."""
    x1 = y1 = x2 = y2 = 0
    roi_image = None

    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline="red", tag="roi")

    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete("roi-image")  # remove old overlay image
        roi_image = image.crop((x1, y1, x2, y2))  # get the image of selected region
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=("roi-image"), anchor="nw")
        canvas.coords("roi", x1, y1, x2, y2)
        # make sure the select rectangle is on top of the overlay image
        canvas.lift("roi")

    root.withdraw()  # hide the root window
    image = ImageGrab.grab()  # grab the fullscreen as select region background
    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken the capture image
    # create a fullscreen window to perform the select region action
    win = tk.Toplevel()
    win.attributes("-fullscreen", 1)
    win.attributes("-topmost", 1)
    canvas = tk.Canvas(win, highlightthickness=0)
    canvas.pack(fill="both", expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor="nw", tag="images")
    # bind the mouse events for selecting region
    win.bind("<ButtonPress-1>", on_mouse_down)
    win.bind("<B1-Motion>", on_mouse_move)
    win.bind("<ButtonRelease-1>", lambda e: win.destroy())
    # use Esc key to abort the capture
    win.bind("<Escape>", lambda e: win.destroy())
    # make the capture window modal
    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify()  # restore root window
    # show the capture image
    if roi_image:
        roi_image.save(f"{temp_path}/1_screenshot.png")
        time.sleep(0.5)
        ocr_read_image()


area_sel()

root.mainloop()
