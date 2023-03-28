echo off
cd /d C:\Users\Matthew\Documents\TTS 3000
cd /d C:\Users\hawkem\OneDrive - Office for National Statistics\Tools\Text-to-Speech-TTS-3000

cls
echo Loading, please wait...

set root=%USERPROFILE%/Anaconda3

call %root%/Scripts/activate.bat %root%

python -m pip install --no-input --user -r requirements.txt

cls

python main.py

cmd /k