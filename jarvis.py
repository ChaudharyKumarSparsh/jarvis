import datetime

import config
from speak import speak

from brain import Brain



def type_instead():
    try:
        return input("You: ").strip().lower() or None
    except EOFError:
        return "goodbye"
    

def get_command(text):
    for word in config.WAKE_WORDS:
        if word in text:
            position = text.find(word)
            command = text[position + len(word):]
            return command.strip(' ,.')
    return None


def greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good AfterNoon"
    return "Good Evening"


def main():
    if config.TYPE_MODE:
        get_input = type_instead
    else:
        from listen import listen
        get_input = listen

    brain = Brain()
    speak(f"{greeting()}, {config.USER_NAME}. {config.ASSISTANT_NAME} is online.")

    running = True
    while running:
        heard = get_input()
        if heard is None:
            continue

        command = get_command(heard)
        if command is None:
            continue

        if command == "":
            speak(f"Yes {config.USER_NAME}??")
            command = get_input()
            if command is None:
                continue

        try:
            running = brain.handle(command)
        except Exception as error:
            print(f"Error: {error}")
            speak("Sorry, something went wrong with that.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting Down.")




