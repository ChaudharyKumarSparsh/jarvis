from listen import listen
from speak import speak

speak('Say something and I will repeat it.')

while True:
    heard = listen()
    if heard is None:
        continue
    # if 'your name' in heard:
    #     speak('My name is JARVIS, I am your voice assistant ;)')
    if heard == 'stop':
        speak('Okay, stopping :((')
        break
    speak(f'You said {heard}')
