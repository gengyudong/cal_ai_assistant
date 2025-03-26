# Define Pydantic models for function calling
from pydantic import BaseModel, Field

class GetBookingsInput(BaseModel):
    pass

class CreateEventTypeInput(BaseModel):
    title: str = Field(..., description="Title of the event type")
    slug: str = Field(..., description="Slug of the event type")
    duration: int = Field(..., description="Duration of the event type in minutes")

class CreateBookingInput(BaseModel):
    title: str = Field(..., description="Title of the event type")
    duration: int = Field(..., description="Duration of the event type in minutes")
    start_time: str = Field(..., description="Start time in ISO format)")
    attendee_name: str = Field(..., description="Name of the attendee")
    attendee_timezone: str = Field(default="America/San_Francisco", description="Time zone of the attendee, in IANA Time zone format")

class CancelBookingInput(BaseModel):
    booking_datetime: str = Field(..., description="Datetime of the booking in ISO format (e.g. 2025-03-27T06:00:00.000Z)")

class RescheduleBookingInput(BaseModel):
    booking_datetime: str = Field(..., description="Datetime of the booking in ISO format (e.g. 2025-03-27T06:00:00.000Z)")
    new_datetime: str = Field(..., description="New start time in ISO format")
    