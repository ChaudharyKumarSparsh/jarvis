from pathlib import Path

#    Who's who
ASSISTANT_NAME = "Jarvis"
USER_NAME = "Sparsh"
WAKE_WORDS = ['jarvis', 'harry']


#    Ears
MIC_INDEX = 2
LANGUAGE = "en-IN"
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 8


#    Mouth
VOICE_RATE = 180
VOICE_INDEX = 0


#    Test
TYPE_MODE = False


#    File Search
HOME = Path.home()
SEARCH_FOLDERS = [HOME / "Desktop",
                  HOME / "Documents", 
                  HOME / "Downloads", 
                  HOME / "Pictures", 
                  HOME / "Music", 
                  HOME / "Videos", 
                  HOME / "OneDrive", 
                  Path("D:/"), Path("E:/")]
SKIP_FOLDERS = {"node_modules", ".git", "__pycache__", ".venv", "venv", "AppData"}


#    Websites
SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "github": "https://www.github.com",
    "spotify": "https://open.spotify.com",
}


#    Web Search
CONTACT_MAIL = "sparshkumr3@gmail.com"



