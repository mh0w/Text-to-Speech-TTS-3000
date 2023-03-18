# -*- coding: utf-8 -*-
"""
Basic text-to-speech reader.

March 2023

@author: hawkem
"""
# pip install pyttsx3 pygame pyautogui keyboard glob errno
# from tkinter import *
# import errno
from tkinter import Tk, Button, Text, END, mainloop, Entry
import pyttsx3
import pygame
import pyautogui as pya
import time
import os
import glob
# import keyboard
#from bindglobal import BindGlobal


os.makedirs("temp_tts_3000_wav_files", exist_ok=True)

temp_path = f"{os.getcwd()}\\temp_tts_3000_wav_files"


def purge_temp_files():
    """Try to delete any files in the temp folder."""
    files = glob.glob(f"{temp_path}\\*.wav")
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            pass


purge_temp_files()

pygame.mixer.init()
engine = pyttsx3.init(driverName=None, debug=True)

root = Tk()
root.title("🦆 Text-to-speech 3000")

def test_function(x="blah"):
    print("hello")


def speak_highlighted(x="blah"):
    """Copy, save to .wav, and read aloud whatever is highlighted."""
    purge_temp_files()
    # pya.hotkey("ctrl", "c")  # copy the text (simulating key strokes)
    root.withdraw()  # hide the tkinter window
    time.sleep(0.2)
    pya.hotkey("ctrl", "c")  # copy the text (simulating key strokes)
    root.deiconify()
    clipboard = root.clipboard_get()  # get the text from the clipboard
    outfile = (
        f"{temp_path}/"
        f"{time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())}.wav"
    )
    engine.save_to_file(clipboard, outfile)
    engine.runAndWait()
    pygame.mixer.music.load(outfile)
    pygame.mixer.music.play()


def stop():
    """Stop the audio player."""
    pygame.mixer.music.stop()


def pause():
    """Pause the audio player."""
    pygame.mixer.music.pause()


def unpause():
    """Unpause the audio player."""
    pygame.mixer.music.unpause()


read_highlighted = Button(
    root, text="Read highlighted", command=speak_highlighted
)
read_highlighted.pack(side="left")

pause_button = Button(root, text="Pause", command=pause)
pause_button.pack(side="left")

unpause_button = Button(root, text="Unpause", command=unpause)
unpause_button.pack(side="left")

#bg = BindGlobal(widget=root)
#bg.gbind("<Control_L-b>", speak_highlighted)

purge_temp_files()

root.mainloop()
