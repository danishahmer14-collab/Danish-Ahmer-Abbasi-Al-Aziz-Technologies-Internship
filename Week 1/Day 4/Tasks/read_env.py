from dotenv import load_dotenv
import os

load_dotenv()   # reads the .env file and loads its values into memory

name = os.getenv("MY_NAME")
key = os.getenv("API_KEY")

print(name)
print(key)