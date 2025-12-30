"""
Schedule Organizer Module for Digital Life Assistant.

Handles calendar event management, conflict detection, time blocking,
and optional Google Calendar integration.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class ScheduleOrganizer:
    """Manage calendar events with conflict detection."""

    EVENT_TYPES = ["meeting", "appointment", "block", "reminder", "personal", "work", "other"]

    def __init__(self, data_manager):
        """
        Initialize ScheduleOrganizer with data persistence layer.

        Args:
            data_manager: DataManager instance for persistence
        """
        self.data_manager = data_manager
        self.events = self.data_manager.load_data("schedule")
        self.config = self.data_manager.load_config()

    def create_event(
        self,
        title: str,
        start_time: str,
        end_time: str,
        event_type: str = "other",
        location: str = "",
        description: str = "",
        attendees: Optional[List[str]] = None,
        recurring: bool = False,
        recurrence_pattern: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new calendar event.

        Args:
            title: Event title
            start_time: Start time in ISO format (YYYY-MM-DDTHH:MM:SS)
            end_time: End time in ISO format
            event_type: Type of event
            location: Event location
            description: Event description
            attendees: List of attendee emails/names
            recurring: Whether event recurs
            recurrence_pattern: Recurrence pattern (e.g., "daily", "weekly", "monthly")

        Returns:
            Created event object
        """
        if event_type not in self.EVENT_TYPES:
            event_type = "other"

        event = {
            "id": str(uuid.uuid4()),
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "event_type": event_type,
            "location": location,
            "description": description,
            "attendees": attendees or [],
            "recurring": recurring,
            "recurrence_pattern": recurrence_pattern,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.events.append(event)
        self.data_manager.save_data("schedule", self.events)

        # Sync to Google Calendar if enabled
        if self._is_google_calendar_enabled():
            self._sync_to_google_calendar(event, action="create")

        return event

    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get an event by ID."""
        for event in self.events:
            if event["id"] == event_id:
                return event
        return None

    def update_event(self, event_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an event.

        Args:
            event_id: Event ID
            updates: Dictionary of fields to update

        Returns:
            Updated event or None if not found
        """
        event = self.get_event_by_id(event_id)
        if not event:
            return None

        allowed_fields = ["title", "start_time", "end_time", "event_type", "location",
                         "description", "attendees", "recurring", "recurrence_pattern"]

        for field in allowed_fields:
            if field in updates:
                event[field] = updates[field]

        event["updated_at"] = datetime.now().isoformat()
        self.data_manager.save_data("schedule", self.events)

        # Sync to Google Calendar if enabled
        if self._is_google_calendar_enabled():
            self._sync_to_google_calendar(event, action="update")

        return event

    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event.

        Args:
            event_id: Event ID

        Returns:
            True if deleted, False if not found
        """
        for i, event in enumerate(self.events):
            if event["id"] == event_id:
                # Sync deletion to Google Calendar if enabled
                if self._is_google_calendar_enabled():
                    self._sync_to_google_calendar(event, action="delete")

                del self.events[i]
                self.data_manager.save_data("schedule", self.events)
                return True
        return False

    def get_events_by_date_range(
        self,
        start_date: str,
        end_date: str,
        event_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get events within a date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            event_type: Optional filter by event type

        Returns:
            List of events in range
        """
        filtered_events = []

        for event in self.events:
            event_date = event["start_time"][:10]  # Extract YYYY-MM-DD

            if start_date <= event_date <= end_date:
                if event_type is None or event["event_type"] == event_type:
                    filtered_events.append(event)

        # Sort by start time
        filtered_events.sort(key=lambda x: x["start_time"])
        return filtered_events

    def get_today_events(self) -> List[Dict[str, Any]]:
        """Get all events for today."""
        today = datetime.now().date().isoformat()
        return self.get_events_by_date_range(today, today)

    def get_week_events(self, offset_weeks: int = 0) -> List[Dict[str, Any]]:
        """
        Get events for a week.

        Args:
            offset_weeks: Number of weeks from now (0 = this week, 1 = next week, -1 = last week)

        Returns:
            List of events for the week
        """
        today = datetime.now().date()
        week_start = today + timedelta(days=-today.weekday(), weeks=offset_weeks)
        week_end = week_start + timedelta(days=6)

        return self.get_events_by_date_range(
            week_start.isoformat(),
            week_end.isoformat()
        )

    def detect_conflicts(
        self,
        new_start: str,
        new_end: str,
        exclude_event_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Detect scheduling conflicts.

        Args:
            new_start: New event start time (ISO format)
            new_end: New event end time (ISO format)
            exclude_event_id: Event ID to exclude from conflict check (for updates)

        Returns:
            List of conflicting events
        """
        new_start_dt = datetime.fromisoformat(new_start)
        new_end_dt = datetime.fromisoformat(new_end)

        conflicts = []

        for event in self.events:
            if exclude_event_id and event["id"] == exclude_event_id:
                continue

            event_start = datetime.fromisoformat(event["start_time"])
            event_end = datetime.fromisoformat(event["end_time"])

            # Check for overlap
            if (new_start_dt < event_end and new_end_dt > event_start):
                conflicts.append(event)

        return conflicts

    def create_time_block(
        self,
        title: str,
        date: str,
        duration_hours: float,
        preferred_start: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a time block, automatically finding available time.

        Args:
            title: Block title
            date: Date for the block (YYYY-MM-DD)
            duration_hours: Duration in hours
            preferred_start: Preferred start time (HH:MM), will find next available if conflicts

        Returns:
            Created time block event or None if no time available
        """
        if preferred_start is None:
            preferred_start = "09:00"

        # Parse duration
        duration_minutes = int(duration_hours * 60)

        # Try to find available slot
        start_hour, start_minute = map(int, preferred_start.split(":"))
        current_time = datetime.fromisoformat(f"{date}T{preferred_start}:00")

        # Search for available slot (max 12 hours of searching)
        for _ in range(48):  # 30-minute increments
            end_time = current_time + timedelta(minutes=duration_minutes)

            # Check if within working hours (9 AM - 6 PM)
            if current_time.hour >= 9 and end_time.hour <= 18:
                conflicts = self.detect_conflicts(
                    current_time.isoformat(),
                    end_time.isoformat()
                )

                if not conflicts:
                    # Found available slot!
                    return self.create_event(
                        title=title,
                        start_time=current_time.isoformat(),
                        end_time=end_time.isoformat(),
                        event_type="block",
                    )

            # Try next 30-minute slot
            current_time += timedelta(minutes=30)

        return None  # No available time found

    def get_daily_schedule(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get formatted daily schedule.

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            Daily schedule summary
        """
        if date is None:
            date = datetime.now().date().isoformat()

        events = self.get_events_by_date_range(date, date)

        # Calculate free time
        total_scheduled_minutes = 0
        for event in events:
            start = datetime.fromisoformat(event["start_time"])
            end = datetime.fromisoformat(event["end_time"])
            total_scheduled_minutes += (end - start).total_seconds() / 60

        return {
            "date": date,
            "total_events": len(events),
            "events": events,
            "total_scheduled_hours": round(total_scheduled_minutes / 60, 1),
            "has_conflicts": len(self._find_all_conflicts_for_date(date)) > 0,
        }

    def _find_all_conflicts_for_date(self, date: str) -> List[Dict[str, Any]]:
        """Find all conflicts for a given date."""
        events = self.get_events_by_date_range(date, date)
        conflicts = []

        for i, event1 in enumerate(events):
            for event2 in events[i+1:]:
                start1 = datetime.fromisoformat(event1["start_time"])
                end1 = datetime.fromisoformat(event1["end_time"])
                start2 = datetime.fromisoformat(event2["start_time"])
                end2 = datetime.fromisoformat(event2["end_time"])

                if start1 < end2 and end1 > start2:
                    conflicts.append({
                        "event1": event1,
                        "event2": event2,
                    })

        return conflicts

    def _is_google_calendar_enabled(self) -> bool:
        """Check if Google Calendar integration is enabled."""
        return self.config.get("google_calendar", {}).get("enabled", False)

    def _sync_to_google_calendar(self, event: Dict[str, Any], action: str) -> None:
        """
        Sync event to Google Calendar (placeholder for actual implementation).

        Args:
            event: Event to sync
            action: Action to perform (create, update, delete)

        Note:
            This is a placeholder. Actual implementation would use Google Calendar API.
            Users need to set up OAuth credentials and enable the API.
        """
        # TODO: Implement actual Google Calendar API integration
        # This requires:
        # 1. OAuth 2.0 credentials
        # 2. google-api-python-client library
        # 3. Proper token management

        # Example structure (not implemented):
        # from googleapiclient.discovery import build
        # from google.oauth2.credentials import Credentials
        #
        # creds = Credentials.from_authorized_user_file('token.json')
        # service = build('calendar', 'v3', credentials=creds)
        #
        # if action == "create":
        #     service.events().insert(calendarId='primary', body=event).execute()
        # elif action == "update":
        #     service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        # elif action == "delete":
        #     service.events().delete(calendarId='primary', eventId=event['id']).execute()

        pass

    def import_from_google_calendar(self, days_back: int = 7, days_forward: int = 30) -> int:
        """
        Import events from Google Calendar (placeholder for actual implementation).

        Args:
            days_back: Number of days in the past to import
            days_forward: Number of days in the future to import

        Returns:
            Number of events imported

        Note:
            This is a placeholder. Actual implementation would use Google Calendar API.
        """
        # TODO: Implement actual Google Calendar API import
        pass
