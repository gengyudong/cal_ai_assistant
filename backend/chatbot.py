from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any
from cal_api import CalClient
from schemas import GetBookingsInput, CreateBookingInput, CancelBookingInput, RescheduleBookingInput
from util import to_slug, append_event_type_id_to_dict
from config import CAL_EMAIL, CAL_EVENT_TYPE_ID, CAL_EVENT_TYPE_ID_FILEPATH
import json
import logging

cal_client = CalClient()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the functions for the LLM to call
def get_schedule() -> str:
    """Get all bookings for a user"""
    bookings = cal_client.get_all_bookings()
    return json.dumps(bookings)

def create_booking(title: str, duration: int,
                   start_time: str, attendee_name: str, attendee_timezone: str) -> str:
    """Create a new booking"""
    global CAL_EVENT_TYPE_ID
    
    event_type_id = CAL_EVENT_TYPE_ID.get(str(duration) + "min", None)
    
    if not event_type_id:
        title = f"{duration} Min Meeting"
        slug = to_slug(title)
        event_type = cal_client.create_event_type(title, slug, duration)
        if "data" in event_type:
            # Save updated CAL_EVENT_TYPE_ID to event_type_id.json
            key = str(duration) + "min"
            event_type_id = event_type["data"]["id"]
            append_event_type_id_to_dict(CAL_EVENT_TYPE_ID_FILEPATH, key, event_type_id)
        else:
            error_message = "Failed to create event type"
            return json.dumps({"error": error_message})
        
    result = cal_client.create_booking(event_type_id, start_time, attendee_name, attendee_timezone, email=CAL_EMAIL)
    return json.dumps(result)

def cancel_booking(booking_datetime: str) -> str:
    """Cancel a booking"""
    bookings = json.loads(get_schedule())
    
    booking_uid = None

    for booking in bookings["data"]:
        if booking["start"] == booking_datetime:
            booking_uid = booking["uid"]
            break
    
    if not booking_uid:
        return json.dumps({"error": "Booking not found"})
    
    result = cal_client.cancel_booking(booking_uid)
    return json.dumps(result)

def reschedule_booking(booking_datetime: str, new_datetime: str) -> str:
    """Reschedule a booking"""
    bookings = json.loads(get_schedule())
    
    booking_uid = None

    for booking in bookings["data"]:
        if booking["start"] == booking_datetime:
            booking_uid = booking["uid"]
            break
    
    if not booking_uid:
        return json.dumps({"error": "Booking not found"})
    
    result = cal_client.reschedule_booking(booking_uid, new_datetime)
    return json.dumps(result)

# Convert functions to OpenAI format
function_schemas = [GetBookingsInput, CreateBookingInput, CancelBookingInput, RescheduleBookingInput]
functions = [convert_to_openai_function(f) for f in function_schemas]

# Set up the chat model with function calling
model = ChatOpenAI(model="gpt-4-0125-preview").bind(functions=functions)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that helps users manage their Cal.com bookings."
     "You can help users get their schedule, create a new booking, cancel a booking, or reschedule a booking."
     "Be polite and ask for any missing information you need to complete requests."
     "All timing that you respond to the user should be in the user's timezone."),
    MessagesPlaceholder(variable_name="messages"),
])

# Create the chain
chain = prompt | model

def process_chat_message(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Process a chat message and return the AI response"""
    # Convert messages to LangChain format
    lc_messages = []
    for msg in messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    
    # Invoke the chain
    response = chain.invoke({"messages": lc_messages})
    
    # Check for function calls
    if hasattr(response, "additional_kwargs") and "function_call" in response.additional_kwargs:
        function_call = response.additional_kwargs["function_call"]
        function_name = function_call["name"]
        args = json.loads(function_call["arguments"])
        
        try:
            # Call the appropriate function
            if function_name == "GetBookingsInput":
                logger.info("Calling get_schedule function")
                result = get_schedule()
                logger.info("Finished getting bookings")
            elif function_name == "CreateBookingInput":
                logger.info(f"Calling create_booking function")
                result = create_booking(**args)
                logger.info(f"Result: {result}")
            elif function_name == "CancelBookingInput":
                logger.info(f"Calling cancel_booking function")
                result = cancel_booking(**args)
                logger.info(f"Result: {result}")
            elif function_name == "RescheduleBookingInput":
                logger.info(f"Calling reschedule_booking function")
                result = reschedule_booking(**args)
                logger.info(f"Result: {result}")
            else:
                result = "Unknown function called"
                logger.warning("Unknown function called")
        except ValueError as ve:
            result = f"ValueError occurred: {str(ve)}"
            logger.error(result)
        except KeyError as ke:
            result = f"KeyError occurred: {str(ke)}"
            logger.error(result)
        except TypeError as te:
            result = f"TypeError occurred: {str(te)}"
            logger.error(result)
        except Exception as e:
            result = f"An unexpected error occurred: {str(e)}"
            logger.error(result)
        
        # Return the function result
        if result == "Successfully created booking":
            return {"role": "assistant", "content": "Successfully created a booking!"}
        
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except:
                pass
        
        function_result_message = AIMessage(content=json.dumps(result))
        lc_messages.append(function_result_message)
        final_response = chain.invoke({"messages": lc_messages})
        
        return {"role": "assistant", "content": final_response.content}
    
    else:
        return {"role": "assistant", "content": response.content}
