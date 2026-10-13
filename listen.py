import speech_recognition as sr

import config



recognizer = sr.Recognizer()
mic = sr.Microphone(device_index = config.MIC_INDEX)




with mic as source:
    print("Calibrating... stay quiet for a second")
    recognizer.adjust_for_ambient_noise(source, duration = 1)


def listen():
    with mic as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout = config.LISTEN_TIMEOUT, 
                                      phrase_time_limit = config.PHRASE_TIME_LIMIT)
        except sr.WaitTimeoutError:
            return None

    try:
        text = recognizer.recognize_google(audio, language = config.LANGUAGE)
    except sr.UnknownValueError:
        # print('Heard sound but could not understand it.')
        return None
    except sr.RequestError as e:
        print(f"Speech service error: {e}")
        return None

    text = text.lower()
    print(f'You: {text}')
    return text

if __name__ == '__main__':
    while True:
        heard = listen()
        if heard:
            print('Got it:', heard)

    