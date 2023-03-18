cd /d C:\Users\Matthew\Documents\TTS 3000

echo CTRL+b to read highlighted text, play, or pause
echo CTRL+i to stop

set root=%USERPROFILE%/Anaconda3

call %root%/Scripts/activate.bat %root%

python -m pip install --no-input --user pyttsx3 pyautogui keyboard pygame

python main.py

cmd /k