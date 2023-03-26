# -*- coding: utf-8 -*-
"""Playlist experimentation.

Created on Sat Mar 25 11:08:28 2023

@author: Matthew
"""

import pyttsx3
import pygame
import time
import keyboard

pygame.init()
engine = pyttsx3.init()

clipboard = (
"""We know it's been a difficult time for many, with costs increasing across every part of our day-to-day lives. Sadly the cost of supplying your services has increased, so we've needed to review our prices and discounts.
Details of how your energy prices are changing can be found below.
We continue to work hard to keep your household bills as low as possible, still offering the cheapest energy in the UK when you bundle with us.*
We've also updated our Privacy Policy and Terms and Conditions. You can find the latest Terms and Conditions alongside the summary of changes here.
Everything you need to know is in this email, and more detail about your energy information is in the attachment. We've also included a link below to find out even more ways we can help you save."""
).split(".")

temp_path = "C:/Users/Matthew/Documents/TTS 3000/temp_audio_files"

time_stamp = (f"{time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())}")

file_list = []

for i, item in enumerate(clipboard):
    print(i, item)
    outfile_wav = (
        f"{temp_path}/"
        f"part-{i}---{time_stamp}.wav"
    )
    engine.save_to_file(clipboard[i], outfile_wav)

    file_list.append(outfile_wav)

engine.runAndWait()

# Load in file 0 (1st)
pygame.mixer.music.load(file_list[0])

playlist_item = 0

playlist_length = len(file_list)

# Setup the end track event
pygame.mixer.music.set_endevent(pygame.USEREVENT)

pygame.mixer.music.play()

keyboard.add_hotkey("ctrl + b", pygame.mixer.music.pause)
keyboard.add_hotkey("ctrl + h", pygame.mixer.music.unpause)


running = True
while pygame.mixer.music.get_busy() is True:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if playlist_item < playlist_length-1:
                playlist_item = playlist_item + 1
                pygame.mixer.music.load(file_list[playlist_item])
                pygame.mixer.music.play()

