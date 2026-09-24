import google.generativeai as genai
from config import GEMINI_API_KEY


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_script(video, regenerate=False):
    mode = "Create a fresh alternative version." if regenerate else "Create the first version."

    prompt = f"""
You are an expert YouTube Shorts producer and viral content strategist.

Analyze this viral video:

Title: {video['title']}
URL: {video['url']}
Viral Score: {video.get('viral_score', 'unknown')}

{mode}

Do NOT copy the original video. Create an original idea using the same successful content principles.

Return exactly this structure:

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

SCENE 1
TIME: 0-3 seconds

VISUAL:
(Describe exactly what appears on screen)

VOICE:
(The exact words spoken)

EDIT:
(Camera movement, captions, sound effects, transitions)


SCENE 2
TIME: 3-15 seconds

VISUAL:

VOICE:

EDIT:


SCENE 3
TIME: 15-45 seconds

VISUAL:

VOICE:

EDIT:


SCENE 4
TIME: 45-60 seconds

VISUAL:

VOICE:

EDIT:


📌 FINAL RETENTION BOOST

Ending strategy:

Comment trigger:

Replay reason:

"""

    response = model.generate_content(prompt)
    return response.text
