import google.generativeai as genai
from config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_script(video):
    prompt = f"""
Analyze this viral YouTube video and create an original remake idea.

Title: {video['title']}
URL: {video['url']}

Return:
- Why it went viral
- New original concept
- Shorts title
- 0-60 second script
- Editing ideas
"""

    response = model.generate_content(prompt)
    return response.text
