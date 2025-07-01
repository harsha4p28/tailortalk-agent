import os
import google.generativeai as genai
from dotenv import load_dotenv
from backend.calendar_utils import check_availability, book_slot
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def extract_intent_entities(user_input):
    prompt = f"""
You are an assistant for a scheduling app.

Extract the user's intent (check or book), the date, and time (if provided).

Respond ONLY with valid JSON. Do NOT include markdown (no ```), no explanation, no preamble.

Format:
{{
  "intent": "check" or "book",
  "date": "YYYY-MM-DD",
  "time": "HH:MM" or null
}}

User input: "{user_input}"
"""
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        import re
        match = re.search(r'\{[\s\S]*?\}', raw_text)
        if match:
            json_str = match.group()
            print(" Cleaned JSON:\n", json_str)
            return json.loads(json_str)

        print(" No JSON found in response.")
        return None

    except Exception as e:
        print(" Error extracting intent:", e)
        return None


def parse_and_respond(user_input):
    result = extract_intent_entities(user_input)
    if not result:
        return "Sorry, I couldn't understand your request."

    intent = result.get("intent")
    date = result.get("date")
    time = result.get("time")

    if intent == "check":
        slots = check_availability(date)
        return f"Available slots on {date}: {', '.join(slots)}" if slots else f"No slots available on {date}."

    elif intent == "book":
        if not time:
            return "Please specify a time to book."
        success = book_slot(date, time)
        return f"Booking confirmed for {date} at {time}!" if success else f"{time} on {date} is already booked."

    return "I couldn't understand what you wanted to do."

def chat_with_agent(message):
    return parse_and_respond(message)
