import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from backend.calendar_utils import check_availability, book_slot

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")


def extract_intent_entities(user_input):
    prompt = f"""
You are a smart assistant that handles scheduling queries and casual chat.

Extract the user's intent as one of the following:
- "book" (if user wants to book a time)
- "check" (if user wants to check availability)
- "chitchat" (for greetings, small talk, general questions)
- "unknown" (if the intent is unclear)

If intent is "book" or "check", also extract "date" and "time".
If it's "chitchat" or "unknown", set "date" and "time" to null.

Respond ONLY in JSON:
{{
  "intent": "book" | "check" | "chitchat" | "unknown",
  "date": "YYYY-MM-DD" | null,
  "time": "HH:MM" | null
}}

User input: "{user_input}"
"""
    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        match = re.search(r'\{[\s\S]*?\}', raw_text)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        return None
    except Exception as e:
        print(" Error extracting intent:", e)
        return None


def gemini_chitchat_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        print(" Error generating chitchat:", e)
        return "Sorry, I couldn't think of a reply just now."


def parse_and_respond(user_input):
    result = extract_intent_entities(user_input)
    if not result:
        return "Sorry, I couldn't understand your request."

    intent = result.get("intent")
    date = result.get("date")
    time = result.get("time")

    if intent == "check":
        if not date:
            return "Please specify a date to check availability."
        slots = check_availability(date)
        return f"Available slots on {date}: {', '.join(slots)}" if slots else f"No slots available on {date}."

    elif intent == "book":
        if not date or not time:
            return "Please specify both date and time to book."
        success = book_slot(date, time)
        return f"Booking confirmed for {date} at {time}!" if success else f"{time} on {date} is already booked."

    elif intent == "chitchat":
        return gemini_chitchat_response(user_input)

    else:
        return "I'm here to help with bookings and availability — feel free to ask anything!"


def chat_with_agent(message):
    return parse_and_respond(message)
