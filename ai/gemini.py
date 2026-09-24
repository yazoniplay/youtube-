import google.generativeai as genai
from config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_script(video, regenerate=False):
    if not video:
        return "❌ No viral video was found. Try again later."

    mode = "Create a fresh alternative version." if regenerate else "Create the first version."

    prompt = f"""
You are an expert YouTube Shorts producer and viral content strategist.

Analyze this viral video:

Title: {video.get('title', 'Unknown')}
URL: {video.get('url', '')}
Viral Score: {video.get('viral_score', 'unknown')}

{mode}

Do NOT copy the original video. Create an original idea using the same successful principles.

Return:

🔥 VIRAL ANALYSIS

Why people clicked:
Hook analysis:
Retention strategy:
Why viewers shared it:

💡 ORIGINAL VIDEO IDEA

Title:
Concept:
Target audience:
Why this could work:

🎬 FULL SHORTS PRODUCTION SCRIPT

For every scene include:
TIME:
VISUAL:
VOICE:
EDIT:

📌 FINAL RETENTION BOOST

Ending strategy:
Comment trigger:
Replay reason:
"""

    try:
        response = model.generate_content(prompt)
        if not response.text:
            return "❌ Gemini returned an empty response."
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return f"❌ Gemini error: {e}"
