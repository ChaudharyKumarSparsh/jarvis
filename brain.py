from pathlib import Path

import files
import websearch
from speak import speak

import config

import datetime
import webbrowser
from urllib.parse import quote_plus


def text_after(command, phrases):
    for phrase in phrases:
        if phrase in command:
            return command.split(phrase, 1 )[1].strip()
    return command

NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
               "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,}


class Brain:
    def __init__(self):
        self.last_found = []
        self.skills = [
            (["goodbye", "bye", "stop", "exit", "sleep", "go to sleep"], self.goodbye),
            (["help", "what can you do"], self.show_help),
            (["find file", "search file", "locate file", "find my file", "where is the file"], self.find_file),
            (["open number", "open file number", "open the file number"], self.open_number),
            (["open"], self.open_website),
            (["time"], self.tell_time),
            (["date", "day is it"], self.tell_date),
            (["your name", "who are you"], self.say_name),
            (["who is", "who was", "what are", "what is"], self.who_or_what_is),
            (["search for", "search", "google", "look up"], self.web_search),           
        ]

    def handle(self, command):
        for keywords, skill in self.skills:
            for keyword in keywords:
                if keyword in command:
                    result = skill(command)
                    return result is not False
        self.search_and_answer(command)
        return True


    def tell_time(self, command):
        speak(datetime.datetime.now().strftime("It's %I:%M %p"))

    def tell_date(self, command):
        speak(datetime.datetime.now().strftime("Today is %A %d %B %Y"))

    def say_name(self, command):
        speak(f"I am {config.ASSISTANT_NAME}, your personal assistant.")

    def show_help(self, command):
        speak("I can tell the time and date, open websites, find files on your laptop, "
              "and answer questions from the internet. Say goodbye to stop me.")

    def goodbye(self, command):
        speak(f"Goodbye {config.USER_NAME}.")
        return False



    def open_website(self, command):
        site = command.split("open", 1)[1].strip()
        key = site.replace(" ", "")
        if key in config.SITES:
            speak(f"Opening {site}.")
            webbrowser.open(config.SITES[key])
        else:
            speak(f"I don't know {site}, so I'll google it for you!")
            webbrowser.open("https://google.com/search?q=" + quote_plus(site))


    def find_file(self, command):
        name = command.split("file", 1)[1].strip()
        for filler in ("named ", "called "):
            if name.startswith(filler):
                name = name[len(filler):]
        if not name:
            speak("Which file should I look for?")
            return 
        speak(f"Searching for {name}")
        self.last_found = files.find_files(name)

        if not self.last_found:
            speak("Sorry, I couldn't find any file with that name:((")
        elif len(self.last_found) == 1:
            speak(f"Found it! Opening {Path(self.last_found[0]).name}.")
            files.open_file(self.last_found[0])
        else:
            speak(f"I found {len(self.last_found)} files.")
            for number, path in enumerate(self.last_found, start = 1):
                print(f"  {number}. {path}")
            speak("Say open number one, two, and so on")


    def open_number(self, command):
        number = None
        for word in command.split():
            if word.isdigit():
                number = int(word)
            elif word in NUMBER_WORDS:
                number = NUMBER_WORDS[word]

        if number is None or not 1 <= number <= len(self.last_found):
            speak("There is no file with that number")
            return 
        path = self.last_found[number - 1]
        speak(f"Opening {Path(path).name}.")
        files.open_file(path)


    def search_and_answer(self, query):
        speak("Let me look that up.")
        results = websearch.search_web(query)
        if not results:
            speak("Sorry, I couldn't search the internet the right now")
            return

        for result in results[:3]:
            page = websearch.read_page(result["href"])
            answer = websearch.best_sentences(page, query)
            if answer:
                speak(answer)
                break
        else:
            speak(results[0]["body"])

        print("     Sources: ")
        for number, result in enumerate(results, start = 1):
            print(f" {number}. {result['title']} - {result['href']}")


    def web_search(self, command):
        query = text_after(command, ["search for", "search", "google", "look up"])
        self.search_and_answer(query)


    def who_or_what_is(self, command):
        topic = text_after(command, ["who is", "who was", "what is", "what are"])
        for article in ("a ", "an ", "the "):
            if topic.startswith(article):
                topic = topic[len(article):]

        summary = websearch.wikipedia(topic)
        if summary:
            first_two = websearch.split_sentences(summary)[:2]
            speak(" ".join(first_two))
        else:
            self.search_and_answer(command)
    


