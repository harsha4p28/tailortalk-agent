import json
import os

CALENDAR_FILE = os.path.join(os.path.dirname(__file__), '../data/mock_calendar.json')

def load_calendar():
    with open(CALENDAR_FILE, "r") as f:
        return json.load(f)

def save_calendar(data):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_availability(date):
    calendar = load_calendar()
    return calendar.get(date, [])

def book_slot(date, time):
    calendar = load_calendar()
    slots = calendar.get(date, [])
    if time in slots:
        return False  
    slots.append(time)
    calendar[date] = slots
    save_calendar(calendar)
    return True
