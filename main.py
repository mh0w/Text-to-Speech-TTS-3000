# -*- coding: utf-8 -*-
"""
Basic text-to-speech reader.

Currently:
    ctrl + b == play/pause
    alt + v == back 10s
    ctrl + i == stop

    ctrl + # == report status to console (for debugging)
    ctr + 1 + 2 == stop/exit/escape

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
import soundfile as sf


print("CTRL+b == play/pause highlighted text, CTRL+i == stop")

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
        except OSError as e:
            pass


purge_temp_files()

pygame.init()
engine = pyttsx3.init()


def check_status():
    """Report status to console."""
    global clipboard, old_clipboard, state
    print("\nUnchanged") if clipboard == old_clipboard else print("\nChanged")
    print(f"Testing: {state}")
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
    print("\nUnchanged") if clipboard == old_clipboard else print("\nChanged")

    # Check if busy
    is_busy = pygame.mixer.music.get_busy()

    # If paused, then start playing
    if (clipboard == old_clipboard) & (state == "Paused") & (is_busy is False):
        pygame.mixer.music.unpause()
        state = "Playing"
        print(f"1: {state}")
        return state

    # If playing, then pause
    if (clipboard == old_clipboard) & (state == "Playing") & (is_busy is True):
        pygame.mixer.music.pause()
        state = "Paused"
        print(f"2: {state}")
        return state

    # If stopped or new text highlighted, then play the new text audio
    if (
        (clipboard != old_clipboard)
        or (state == "Stopped")
        or (is_busy is False)
    ):
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
        print(f"3: {state}, new")
        return state, duration


def stop():
    """Stop the audio player."""
    global state
    pygame.mixer.music.stop()
    state = "Stopped"
    print(state)
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
