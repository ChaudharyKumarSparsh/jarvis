import pyttsx3

import config

def speak(text):
    print(f"{config.ASSISTANT_NAME}: {text}")
    engine = pyttsx3.init()
    engine.setProperty('rate', config.VOICE_RATE)
    voices = engine.getProperty("voices")
    if voices and config.VOICE_INDEX < len(voices):
        engine.setProperty("voice", voices[config.VOICE_INDEX].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

if __name__ == '__main__':
    speak(f"Hello {config.USER_NAME}. I am {config.ASSISTANT_NAME}, your assistant")
    speak('All systems online.')

