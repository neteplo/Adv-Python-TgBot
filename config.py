import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
FATSECRET_KEY = os.getenv('FATSECRET_KEY')
FATSECRET_SECRET = os.getenv('FATSECRET_SECRET')

