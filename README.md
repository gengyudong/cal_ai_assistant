# LiveX.AI Problem Statement

## Introduction

This project is an interactive chatbot using OpenAI's function calling capabilities. The chatbot allows users to interact with their cal.com account directly through a chat interface. Users can book new events, list upcoming events, and cancel or reschedule events using the cal.com API.

## Features

- **Book a Meeting**: The chatbot can help users book a new meeting by asking for the meeting details such as date, time, and reason.
- **Cancel an Event**: The chatbot can find and cancel an event based on the user's request.
- **Reschedule an Event**: Users can reschedule an existing event to a new time.
- **Show Scheduled Events**: Users can retrieve a list of their scheduled events.

## Installation

### Using Docker

1. **Clone the repository**:

   ```sh
   git clone cal_ai_assistant
   cd <repository-directory>
   ```

2. **Create a `.env` file** in the root directory with the following content:

   ```env
   OPENAI_API_KEY=<your-openai-api-key>
   CAL_API_KEY=<your-cal-api-key>
   CAL_BASE_URL='https://api.cal.com/v2/'
   CAL_EMAIL=<your-cal-email>
   ```

3. **Build and start the services** using Docker Compose:
   ```sh
   docker-compose up --build
   ```

## Running the Application

### Starting the Frontend

1. **Access the frontend**:
   Open your web browser and navigate to `http://localhost:8501`.

2. **Interact with the chatbot**:
   - Use the chat input to ask the chatbot to book a meeting, show your schedule, cancel an event, or reschedule an event.
   - Example prompts:
     - "Help me book a meeting"
     - "Show me my upcoming schedule"
     - "Help me to cancel an event"
     - "Help me to reschedule an event"

The chatbot will guide you through the process and interact with the cal.com API to fulfill your requests.
