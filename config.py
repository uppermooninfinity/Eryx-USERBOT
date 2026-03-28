import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")


API_ID = int(getenv("API_ID", "32228932")) #optional
API_HASH = getenv("API_HASH", "152e4c828fbc897e927f42894ae9c9f4") #optional

SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
OWNER_ID = 7396578515
MONGO_URL = getenv("mongodb+srv://mailnewtest1234_db_user:urps1q1RuW4ebVHQ@newclusteruserbot.fob21b9.mongodb.net/")
BOT_TOKEN = getenv("BOT_TOKEN", "8429717262:AAHBQ7nqzSc0LibQrOaxM337UFXxtQclhVY")
ALIVE_PIC = getenv("ALIVE_PIC", 'https://i.ibb.co/RkB0mshb/photo-2026-03-28-18-26-18-7622374658888695856.jpg')
ALIVE_TEXT = getenv("ALIVE_TEXT")
PM_LOGGER = getenv("PM_LOGGER")
LOG_GROUP = getenv("LOG_GROUP")
GIT_TOKEN = getenv("GIT_TOKEN") #personal access token
REPO_URL = getenv("REPO_URL", "https://github.com/Hellobot-cmd/Eryx-USERBOT.git")
BRANCH = getenv("BRANCH", "master") #don't change
 
STRING_SESSION1 = getenv("STRING_SESSION1", "")
STRING_SESSION2 = getenv("STRING_SESSION2", "")
STRING_SESSION3 = getenv("STRING_SESSION3", "")
STRING_SESSION4 = getenv("STRING_SESSION4", "")
STRING_SESSION5 = getenv("STRING_SESSION5", "")
STRING_SESSION6 = getenv("STRING_SESSION6", "")
STRING_SESSION7 = getenv("STRING_SESSION7", "")
STRING_SESSION8 = getenv("STRING_SESSION8", "")
STRING_SESSION9 = getenv("STRING_SESSION9", "")
STRING_SESSION10 = getenv("STRING_SESSION10", "")
