# TailorTalk Booking Assistant

TailorTalk is a conversational AI-powered assistant for scheduling appointments. It uses Google's Gemini model to interpret user input and manage booking slots through a user-friendly interface.

# Deployment 

- **Frontend (Streamlit):** [Streamlit Cloud Deployment](https://tailortalk-agent-harsha4p28.streamlit.app/)
- **Backend (FastAPI):** [Railway Deployment](https://tailortalk-agent-production.up.railway.app/) 

## Project Structure

- **Frontend:** Streamlit app that interacts with the assistant and displays the chat history.
- **Backend:** FastAPI server with endpoints for processing user input and generating responses using Gemini.
- **Agent:** Gemini-powered intent extractor and responder.
- **Calendar Utils:** Reads and writes to a mock calendar (JSON file).
- **Data:** Mock calendar data stored in `mock_calendar.json`.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **LLM:** Google Gemini (via `google.generativeai`)
- **Data Storage:** JSON (mock calendar)
- **API Communication:** REST (via `requests`)

## Features

- Chat-based booking and availability checking
- Intent recognition using Google Gemini 1.5 Flash
- Date and time extraction from natural language
- Real-time slot booking and calendar updates


## Example Queries

- "Book a slot on July 2 at 11 AM"
- "Check availability on July 1"
- "Can I schedule something at 2 PM tomorrow?"
