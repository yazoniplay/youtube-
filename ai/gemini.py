import google.generativeai as genai
from config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_script(video):
    prompt = f"""
You are a YouTube Shorts growth strategist.

Analyze this currently viral video:

Title: {video['title']}
URL: {video['url']}
Viral Score: {video.get('viral_score', 'unknown')}

Create an ORIGINAL video concept. Do not copy the original.

Return:

🔥 VIRAL ANALYSIS
- Why viewers clicked
- Hook strength
- Retention strategy
- What made it shareable

💡 ORIGINAL REMAKE IDEA
- New title
- New concept
- Target audience

🎬 FULL SHORTS SCRIPT
0-3 seconds:
Hook

3-15 seconds:
Setup

15-45 seconds:
Main content

45-60 seconds:
Payoff

🎥 EDITING PLAN
- Cuts
- Captions
- Effects

"""

    response = model.generate_content(prompt)
    return response.text
