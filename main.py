# -*- coding: utf-8 -*-
"""
Basic highlighted-text-to-speech reader.

Created March 2023

@author: hawkem / mh0w
"""
# pip install pyttsx3 pygame pyautogui keyboard glob errno soundfile jupyter ipywidgets
import os
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
import subprocess


#######################################################################################
# USER SETTINGS #######################################################################
#######################################################################################
# Choose from available voices by changing chosen_voice number
# Choose voice speed by changing speed_multiplier (0.5 = half speed, 2.0 = double, etc)
# Choose voice volume by setting chosen_volume from 0 to 1 (e.g., 0.45 = 45% of normal)
# Choose how many seconds to rewind and fast forward in seconds
# Choose what hotkeys to use for play/pause, rewind, and fast forward
chosen_voice = 1  # default is 1 (starts at 0)
speed_multiplier = 1.0  # default is 1.0
chosen_volume = 1.0  # default is 1.0 (from 0.0 to 1.0)
rewind_seconds = 3  # default is 3 (seconds)
forward_seconds = 3  # default is 3 (seconds)
play_pause_hotkey = "ctrl + b"  # default is "ctrl + b"
rewind_hotkey = "alt + v"  # default is "alt + v"
forward_hotkey = "alt + n"  # default is "alt + n"
ocr_hotkey = "alt + o"  # default is "alt + o"
#######################################################################################
#######################################################################################
#######################################################################################


print(
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "~~ TTS 3000 is now running ~~\n"
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "\nCTRL + b == play/pause highlighted text (minimise this terminal/console first!)"
    "\nALT  + v == rewind"
    "\nALT  + n == fast-forward"
    "\n\nMinimise this prompt/console/terminal window to use TTS 3000"
    "\n\nClose this prompt/console/terminal window to quit TTS 3000"
)

temp_path = f"{os.path.dirname(__file__)}/temp_audio_files"

os.makedirs(temp_path, exist_ok=True)

# Initialise some variables
clipboard = "clipboard not yet set"
old_clipboard = "old_clipboard not yet set"
state = "state not yet set"


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

pygame.init()  # idk why I cannot remove this!
engine = pyttsx3.init()
#mp = Dispatch("WMPlayer.OCX")


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


def speak_highlighted():
    """
    Copy, save to .wav, and read aloud whatever is highlighted.

    If the selection (copied text) is unchanged, then just unpause.
    """
    global clipboard, old_clipboard, state, output_mp3, mp, tune

    # Capture clipboard
    pya.hotkey("ctrl", "c")  # copy the text (simulating key strokes)
    clipboard = Tk().clipboard_get()
    if clipboard.strip() == "":
        clipboard = "No text selected"

    # If paused, then start playing
    if (clipboard == old_clipboard) & (state == "Paused"):
        mp.controls.play()
        state = "Playing"
        return state

    # If playing, then pause
    if (clipboard == old_clipboard) & (state == "Playing"):
        mp.controls.pause()
        state = "Paused"
        return state

    # If new text highlighted or not busy, then play the new text audio
    if (clipboard != old_clipboard):
        old_clipboard = clipboard
        outfile_wav = (
            f"{temp_path}/"
            f"{time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())}.wav"
        )
        engine.save_to_file(clipboard, outfile_wav)
        engine.runAndWait()
        data, fs = sf.read(outfile_wav)
        output_mp3 = f"{outfile_wav[0:-3]}mp3"
        sf.write(output_mp3, data, fs)

        mp = Dispatch("WMPlayer.OCX")
        tune = mp.newMedia(output_mp3)
        mp.currentPlaylist.appendItem(tune)
        mp.controls.play()
        sleep(1)
        #mp.controls.playItem(tune)

        state = "Playing"
        return state, mp, tune, output_mp3


def rewind_n_seconds():
    """Rewind n seconds, or rewind to 00:00 (0 seconds) if near start already."""
    mp.controls.currentPosition = (mp.controls.currentPosition) - rewind_seconds


def forward_n_seconds():
    """Go forward n seconds if sufficiently far from end of audio track."""
    if mp.currentMedia.duration > (mp.controls.currentPosition + forward_seconds + 2):
        mp.controls.currentPosition = (mp.controls.currentPosition) + forward_seconds


def run_ocr_script():
    """Run the OCR image to text script."""
    subprocess.Popen(['python', 'ocr.py'])


keyboard.add_hotkey(play_pause_hotkey, speak_highlighted)
keyboard.add_hotkey(rewind_hotkey, rewind_n_seconds)
keyboard.add_hotkey(forward_hotkey, forward_n_seconds)
keyboard.add_hotkey(ocr_hotkey, run_ocr_script)

keyboard.add_hotkey("ctrl + #", check_status)

keyboard.wait("ctrl + 1 + 2")
