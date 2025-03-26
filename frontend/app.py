import streamlit as st
import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000/chat"

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your Cal.com assistant. How can I help you today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to do with your calendar?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare request to backend
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    
    try:
        # Call backend API
        response = requests.post(
            BACKEND_URL,
            json={"messages": messages},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        # Get the response
        ai_response = response.json()
        
        # Add assistant response to chat history
        st.session_state.messages.append(ai_response)
        
        # Display assistant response
        with st.chat_message(ai_response["role"]):
            # Format function responses nicely
            if ai_response.get("role") == "function":
                try:
                    content = json.loads(ai_response["content"])
                    st.json(content)
                except:
                    st.markdown(ai_response["content"])
            else:
                st.markdown(ai_response["content"])
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def send_message_to_backend(message):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
    
    try:
        response = requests.post(
            BACKEND_URL,
            json={"messages": messages},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        ai_response = response.json()
        st.session_state.messages.append(ai_response)
        
        with st.chat_message(ai_response["role"]):
            if ai_response.get("role") == "function":
                try:
                    content = json.loads(ai_response["content"])
                    st.json(content)
                except:
                    st.markdown(ai_response["content"])
            else:
                st.markdown(ai_response["content"])
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add some example prompts
st.sidebar.title("Example Prompts")

if st.sidebar.button("Show schedule"):
    send_message_to_backend("Show me my scheduled events")

if st.sidebar.button("Book a meeting"):
    send_message_to_backend("Help me book a meeting")
    
if st.sidebar.button("Cancel an event"):
    send_message_to_backend("Help me to cancel an event")

if st.sidebar.button("Reschedule an event"):
    send_message_to_backend("Help me to reschedule an event")
    