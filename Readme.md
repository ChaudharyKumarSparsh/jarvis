# Jarvis: a Python voice assistant

A voice assistant inspired by Jarvis from Iron Man, built as my 4th-year college project.
Say "Jarvis" and give it a command.

## Features
- Wake word: only responds when you say "Jarvis"
- Tells the time and date
- Opens websites ("Jarvis, open YouTube")
- Finds files on your laptop by name and opens them
- Answers questions using Wikipedia and web search
- Typing mode for testing without a microphone

## Setup
1. Install Python 3.12
2. In this folder:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Open `config.py` and set your microphone number (`MIC_INDEX`), your name and the folders to search.
4. Run `python jarvis.py`

## How it works
| File | Job |
|---|---|
| `jarvis.py` | Main loop: listens, checks for the wake word, sends commands to the brain |
| `brain.py` | The `Brain` class: matches keywords to skills |
| `listen.py` | Speech to text (Google's free recogniser) |
| `speak.py` | Text to speech (pyttsx3, works offline) |
| `files.py` | Searches folders and ranks files by name |
| `websearch.py` | Wikipedia + DuckDuckGo search, picks the best sentences |
| `config.py` | All settings in one place |

## Limitations
- Needs internet for speech recognition and web search
- Web answers are picked sentences, so they can miss the point