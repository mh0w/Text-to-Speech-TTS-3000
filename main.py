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


print(
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "~~ TTS 3000 is now running ~~\n"
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "\nCTRL + b == play/pause highlighted text (not in this terminal/console window)"
    "\nCTRL + i == stop"
    "\nALT  + v == back 10s"
    "\n\nMinimise this prompt/console/terminal window to use TTS 3000"
    "\n\nClose this prompt/console/terminal window to quit TTS 3000"
)

os.makedirs("temp_tts_3000_wav_files", exist_ok=True)

temp_path = f"{os.getcwd()}\\temp_tts_3000_wav_files"

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

# Choose from available voices by changing chosen_voice number
# Choose voice speed by changing speed_multiplier (0.5 = half speed, 2.0 = double, etc)
# Choose voice volume by setting chosen_volume from 0 to 1 (e.g., 0.45 = 45% of normal)
chosen_voice = 1  # default is 1 (starts at 0)
speed_multiplier = 1.0  # default is 1.0
chosen_volume = 1.0  # default is 1.0 (from 0.0 to 1.0)

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
    Copy, save to .wav, and read aloud whatever is highlighted.

    If the selection (copied text) is unchanged, then just unpause.
    """
    global clipboard, old_clipboard, state, duration

    # Capture clipboard
    pya.hotkey("ctrl", "c")  # copy the text (simulating key strokes)
    clipboard = Tk().clipboard_get()
    if clipboard == " ":
        clipboard = "No text selected"

    # Check if busy
    is_busy = pygame.mixer.music.get_busy()

    # If paused, then start playing
    if (clipboard == old_clipboard) & (state == "Paused") & (is_busy is False):
        pygame.mixer.music.unpause()
        state = "Playing"
        return state

    # If playing, then pause
    if (clipboard == old_clipboard) & (state == "Playing") & (is_busy is True):
        pygame.mixer.music.pause()
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
        pygame.mixer.music.load(output_mp3)
        pygame.mixer.music.play()
        state = "Playing"
        return state, duration


def stop():
    """Stop the audio player."""
    global state
    pygame.mixer.music.stop()
    state = "Stopped"
    return state


def back_10s():
    """Rewind 10s or to 0s."""
    global state
    current_pos = pygame.mixer.music.get_pos() / 1000
    state = "Playing"

    # If less than 11 seconds into the audio file, start from beginning (0s)
    if current_pos < 11:
        pygame.mixer.music.play()

    # If 11 seconds or more into the audio file, rewind 10s
    if current_pos >= 11:
        pygame.mixer.music.play(start=current_pos - 10)

    return state


def forward_5s():
    """Fast forward 5s."""
    global duration, state
    if state != "Stopped":
        current_pos = pygame.mixer.music.get_pos() / 1000
        if duration - current_pos > 6:
            pygame.mixer.music.set_pos(current_pos + 5)


keyboard.add_hotkey("ctrl + b", speak_highlighted)
keyboard.add_hotkey("alt + v", back_10s)
# keyboard.add_hotkey("alt + shift + v", forward_5s)
keyboard.add_hotkey("ctrl + i", stop)
keyboard.add_hotkey("ctrl + #", check_status)
keyboard.wait("ctrl + 1 + 2")
