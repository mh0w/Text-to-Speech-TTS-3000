# -*- coding: utf-8 -*-
"""
Basic text-to-speech reader.

March 2023

@author: hawkem
"""
# pip install pyttsx3 pygame pyautogui keyboard glob errno
import errno
import pyttsx3
import pygame
import pyautogui as pya
import time
import os
import glob
import keyboard
from tkinter import Tk

print("CTRL+b == play/pause highlighted text, CTRL+i == stop")

os.makedirs("temp_tts_3000_wav_files", exist_ok=True)

temp_path = f"{os.getcwd()}\\temp_tts_3000_wav_files"

clipboard = "Empty, has not been used yet"
old_clipboard = "Empty, not yet used"
state = "Empty, not yet used"


def purge_temp_files():
    """Try to delete any files in the temp folder."""
    files = glob.glob(f"{temp_path}\\*.wav")
    for f in files:
        os.remove(f)
        try:
            os.remove(f)
        except OSError as e:
            pass


purge_temp_files()

pygame.mixer.init()
engine = pyttsx3.init()


def check_status():
    """Little test function."""
    global clipboard, old_clipboard, state
    print("\nUnchanged") if clipboard == old_clipboard else print("\nChanged")
    print(f"Testing: {state}")


def speak_highlighted():
    """
    Copy, save to .wav, and read aloud whatever is highlighted.

    If the selection (copied text) is unchanged, then just unpause.
    """
    global clipboard, old_clipboard, state
    pya.hotkey("ctrl", "c")  # copy the text (simulating key strokes)
    clipboard = Tk().clipboard_get()
    if clipboard == " ":
        clipboard = "No text selected"
    print("\nUnchanged") if clipboard == old_clipboard else print("\nChanged")
    if (clipboard == old_clipboard) & (state == "Paused"):
        pygame.mixer.music.unpause()
        state = "Playing"
        print(f"1: {state}")
        return state
    if (clipboard == old_clipboard) & (state == "Playing"):
        pygame.mixer.music.pause()
        state = "Paused"
        print(f"2: {state}")
        return state
    if (clipboard != old_clipboard) or (state == "Stopped"):
        old_clipboard = clipboard
        outfile = (
            f"{temp_path}/"
            f"{time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())}.wav"
        )
        engine.save_to_file(clipboard, outfile)
        engine.runAndWait()
        pygame.mixer.music.load(outfile)
        pygame.mixer.music.play()
        state = "Playing"
        print(f"3: {state}, new")
        return state


def stop():
    """Stop the audio player."""
    global state
    pygame.mixer.music.stop()
    state = "Stopped"
    print(state)
    return state


keyboard.add_hotkey("ctrl + b", speak_highlighted)
keyboard.add_hotkey("ctrl + i", stop)
keyboard.add_hotkey("ctrl + #", check_status)
keyboard.wait("ctrl + 1 + 2")
