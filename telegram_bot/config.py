import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', 'some_token')
PG_LINK = os.getenv('PG_LINK', 'some')


