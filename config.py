from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = getenv('TOKEN')
MANAGER_CHAT_ID = int(os.getenv("MANAGER_CHAT_ID", 0))
