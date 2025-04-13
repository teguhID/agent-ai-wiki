import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(os.getenv("GOOLE_MODEL"))

def generate_text(prompt: str) -> str:
    return model.generate_content(prompt).text
