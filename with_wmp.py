# -*- coding: utf-8 -*-
"""
Basic text-to-speech reader.

March 2023

@author: hawkem
"""
# pip install pyttsx3 pygame pyautogui keyboard glob errno soundfile
import os
import errno
import pyttsx3
import pyautogui as pya
import time
import glob
import keyboard
from tkinter import Tk
import soundfile as sf
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from win32com.client import Dispatch
from time import sleep


#################
# USER SETTINGS #
#######################################################################################
# Choose from available voices by changing chosen_voice number
# Choose voice speed by changing speed_multiplier (0.5 = half speed, 2.0 = double, etc)
# Choose voice volume by setting chosen_volume from 0 to 1 (e.g., 0.45 = 45% of normal)
# Choose how far back the ALT+V command will rewind (e.g., 5 seconds)
chosen_voice = 1  # default is 1 (starts at 0)
speed_multiplier = 1.0  # default is 1.0
chosen_volume = 1.0  # default is 1.0 (from 0.0 to 1.0)
rewind_seconds = 5  # default is 5
#######################################################################################


print(
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "~~ TTS 3000 is now running ~~\n"
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "\nCTRL + b == play/pause highlighted text (not in this terminal/console window)"
    "\nCTRL + i == stop"
    "\nALT  + v == rewind"
    "\n\nMinimise this prompt/console/terminal window to use TTS 3000"
    "\n\nClose this prompt/console/terminal window to quit TTS 3000"
)

os.makedirs("temp_audio_files", exist_ok=True)

temp_path = f"{os.getcwd()}\\temp_audio_files"

clipboard = "Empty, has not been used yet"
old_clipboard = "Empty, not yet used"
state = "Empty, not yet used"


def purge_temp_files():
    """Try to delete any files in the temp folder."""
    files = glob.glob(f"{temp_path}\\*")
    for f in files:
        os.remove(f)
        try:
            os.remove(f)
        except OSError:
            pass


purge_temp_files()

pygame.init()
engine = pyttsx3.init()

try:
    engine.setProperty("voice", engine.getProperty("voices")[chosen_voice].id)
except IndexError:
    print("Could not set custom selected voice")

try:
    engine.setProperty("rate", 200 * speed_multiplier)
except IndexError:
    print("Could not set custom selected speed")

try:
    engine.setProperty("volume", chosen_volume)
except IndexError:
    print("Could not set custom selected volume")


def check_status():
    """Report status to console."""
    global clipboard, old_clipboard, state
    print("\nUnchanged text") if clipboard == old_clipboard else print("\nChanged text")
    print(f"State: {state}")
    print(f"Busy: {pygame.mixer.music.get_busy()}")


def speak_highlighted():
    """
    Copy, save to .mp3, and read aloud whatever is highlighted.

    If the selection (copied text) is unchanged, then just unpause.
    """
    global clipboard, old_clipboard, state, duration, mp, tune

    # Capture clipboard
    pya.hotkey("ctrl", "c")  # copy the text (simulating key strokes)
    clipboard = Tk().clipboard_get()
    if clipboard == " ":
        clipboard = "No text selected"

    # Check if busy
    is_busy = pygame.mixer.music.get_busy()

    # If paused, then start playing
    if (clipboard == old_clipboard) & (state == "Paused") & (is_busy is False):
        mp.controls.play()
        state = "Playing"
        return state

    # If playing, then pause
    if (clipboard == old_clipboard) & (state == "Playing") & (is_busy is True):
        mp.controls.pause()
        state = "Paused"
        return state

    # If stopped or new text highlighted, then play the new text audio
    if (clipboard != old_clipboard) or (state == "Stopped") or (is_busy is False):
        old_clipboard = clipboard
        outfile_wav = (
            f"{temp_path}/"
            f"{time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())}.wav"
        )
        engine.save_to_file(clipboard, outfile_wav)
        engine.runAndWait()
        duration = pygame.mixer.Sound(outfile_wav).get_length()
        data, fs = sf.read(outfile_wav)
        output_mp3 = f"{outfile_wav[0:-3]}mp3"
        sf.write(output_mp3, data, fs)

        mp = Dispatch("WMPlayer.OCX")
        tune = mp.newMedia(output_mp3)
        mp.currentPlaylist.appendItem(tune)
        mp.controls.play()
        sleep(1)
        # mp.controls.playItem(tune)

        state = "Playing"
        return state, duration, mp, tune


def rewind_n_seconds():
    """Rewind n seconds or to 00:00 (0 seconds)."""
    global state
    state = "Playing"

    # If not beyond n seconds in the audio file, start from beginning (00:00 / 0s)
    mp.controls.currentPosition = (mp.controls.currentPosition) - 2

    # If more than n seconds into the audio file, rewind n seconds

    return state


def forward_5s():
    """Fast forward 5s."""
    global duration, state
    mp.controls.currentPosition = (mp.controls.currentPosition) + 2

    return state


keyboard.add_hotkey("ctrl + b", speak_highlighted)
keyboard.add_hotkey("alt + v", rewind_n_seconds)
keyboard.add_hotkey("alt + shift + v", forward_5s)
keyboard.add_hotkey("ctrl + #", check_status)
keyboard.wait("ctrl + 1 + 2")
