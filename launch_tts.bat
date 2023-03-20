echo off
cd /d C:\Users\Matthew\Documents\TTS 3000
cd /d C:\Users\hawkem\OneDrive - Office for National Statistics\Tools\Text-to-Speech-TTS-3000

cls

set root=%USERPROFILE%/Anaconda3

call %root%/Scripts/activate.bat %root%

python -m pip install --quiet --no-input --user pyttsx3 pyautogui keyboard pygame soundfile

python main.py

cmd /k