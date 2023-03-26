# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 13:06:17 2023

@author: Matthew
"""

import vlc

player = vlc.MediaPlayer("C:/Users/Matthew/Downloads/file_example_MP3_1MG.mp3")

player.play()

player.pause()

player.get_time()

player = vlc.MediaPlayer("C:/Users/Matthew/Downloads/file_example_MP3_1MG.mp3")
player.set_time(player.get_time() - 1_000)  # back, works fine
player.set_time(player.get_time() + 1_000)  # forward, works fine

player.play()


