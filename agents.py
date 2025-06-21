import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY


def call_gemini(prompt):
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, headers={
                             "Content-Type": "application/json"}, data=json.dumps(data))
    if response.status_code != 200:
        return None
    result = response.json()
    if 'candidates' in result and result['candidates']:
        return result['candidates'][0]['content']['parts'][0]['text']
    return None


def writer_agent(text):
    prompt = f"""
You are a skilled fiction editor and storyteller. Take the following raw chapter and rewrite it with:

1. A more modern, emotionally rich narrative voice
2. Stronger imagery and sensory details
3. Engaging pacing and character-driven descriptions
4. Clear structure, broken into logical paragraphs or scenes

Avoid old-fashioned or passive language. Make the prose feel vivid and immersive, like something from a bestselling novel.

--- Raw Chapter Start ---
{text}
--- Raw Chapter End ---

Begin your rewritten version below:
"""
    return call_gemini(prompt)


def reviewer_agent(spun_text):
    prompt = f"""
You're a senior editor. Review the rewritten chapter below and make improvements to:

- Tone: ensure it matches a modern, immersive storytelling style
- Clarity: remove awkward phrasing or confusing parts
- Flow: improve paragraph transitions, scene breaks, or narrative rhythm

Polish the prose like it's going to be published professionally.

--- Rewritten Chapter Start ---
{spun_text}
--- Rewritten Chapter End ---

Begin your reviewed version below:
"""
    return call_gemini(prompt)



def orchestrator(text):
    spun = writer_agent(text)
    reviewed = reviewer_agent(spun) if spun else None
    return spun, reviewed
