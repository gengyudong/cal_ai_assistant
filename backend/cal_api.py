import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
from config import CAL_API_KEY, CAL_BASE_URL

class CalClient:
    def __init__(self):
        pass
    
    # Function to get all scheduled events
    def get_all_bookings(self) -> Dict:
        """Get all bookings for a user"""
        url = f"{CAL_BASE_URL}/bookings"
        
        headers = {
            "cal-api-version": "2024-08-13",
            "Authorization": f"Bearer {CAL_API_KEY}"
        }
        
        querystring = {"status":"upcoming"}
        
        try:
            response = requests.get(url, headers=headers, params=querystring)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Get all booking error: {e}")
            return []
    
    # Function to create an event type
    def create_event_type(self, title: str, slug: str, duration: int) -> Dict:
        """Create a new event type"""
        url = f"{CAL_BASE_URL}/event-types"
        
        headers = {
            "cal-api-version": "2024-06-14",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CAL_API_KEY}"
        }
        
        payload = {
            "lengthInMinutes": duration,
            "title": title,
            "slug": slug
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Create event type error: {e}")
            return {}
    
    # Function to book an event
    def create_booking(self, event_type_id: int, start_time: str, attendee_name: str, attendee_timezone, email) -> Dict:
        """Create a new booking"""
        url = f"{CAL_BASE_URL}/bookings"
        
        headers = {
            "cal-api-version": "2024-08-13",
            "Content-Type": "application/json"
        }
        
        payload = {
            "start": start_time,
            "eventTypeId": event_type_id,
            "attendee": {
                "name": attendee_name,
                "timeZone": attendee_timezone,
                "email": email
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Create booking error: {e}")
            return {}
    
    # Function to cancel an event
    def cancel_booking(self, booking_id: int) -> Dict:
        """Cancel a booking"""
        url = f"{CAL_BASE_URL}/bookings/{booking_id}/cancel"
        
        headers = {
            "cal-api-version": "2024-08-13",
            "Content-Type": "application/json"
        }
        
        payload = {
            "cancellationReason": "User requested cancellation"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Cancel booking error: {e}")
            return {}
    
    # Function to reschedule an event
    def reschedule_booking(self, booking_id: int, new_start_time: str) -> Dict:
        """Reschedule a booking"""
        url = f"{CAL_BASE_URL}/bookings/{booking_id}/reschedule"
        
        headers = {
            "cal-api-version": "2024-08-13",
            "Content-Type": "application/json"
        }
        
        payload = {
            "start": new_start_time,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Reschedule booking error: {e}")
            return {}
