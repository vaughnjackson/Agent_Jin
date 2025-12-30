"""
Reminder System Module for Digital Life Assistant.

Handles reminder creation, recurring patterns, context-based alerts,
and notification management.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class ReminderSystem:
    """Manage reminders with recurring patterns and context awareness."""

    PRIORITIES = ["low", "medium", "high"]
    RECURRENCE_PATTERNS = ["once", "daily", "weekly", "monthly", "yearly", "custom"]
    STATUSES = ["active", "snoozed", "completed", "cancelled"]

    def __init__(self, data_manager):
        """
        Initialize ReminderSystem with data persistence layer.

        Args:
            data_manager: DataManager instance for persistence
        """
        self.data_manager = data_manager
        self.reminders = self.data_manager.load_data("reminders")

    def create_reminder(
        self,
        title: str,
        due_datetime: str,
        description: str = "",
        priority: str = "medium",
        recurrence: str = "once",
        recurrence_end_date: Optional[str] = None,
        context: Optional[str] = None,
        linked_task_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new reminder.

        Args:
            title: Reminder title
            due_datetime: Due date and time (ISO format: YYYY-MM-DDTHH:MM:SS)
            description: Reminder description
            priority: Priority level
            recurrence: Recurrence pattern
            recurrence_end_date: When to stop recurring (optional)
            context: Context for the reminder (e.g., "home", "work", "call mom")
            linked_task_id: Optional task ID this reminder is associated with

        Returns:
            Created reminder object
        """
        if priority not in self.PRIORITIES:
            priority = "medium"

        if recurrence not in self.RECURRENCE_PATTERNS:
            recurrence = "once"

        reminder = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "due_datetime": due_datetime,
            "priority": priority,
            "recurrence": recurrence,
            "recurrence_end_date": recurrence_end_date,
            "context": context,
            "linked_task_id": linked_task_id,
            "status": "active",
            "snooze_until": None,
            "completed_at": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.reminders.append(reminder)
        self.data_manager.save_data("reminders", self.reminders)
        return reminder

    def get_reminder_by_id(self, reminder_id: str) -> Optional[Dict[str, Any]]:
        """Get a reminder by ID."""
        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                return reminder
        return None

    def update_reminder(self, reminder_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a reminder.

        Args:
            reminder_id: Reminder ID
            updates: Dictionary of fields to update

        Returns:
            Updated reminder or None if not found
        """
        reminder = self.get_reminder_by_id(reminder_id)
        if not reminder:
            return None

        allowed_fields = ["title", "description", "due_datetime", "priority",
                         "recurrence", "recurrence_end_date", "context", "status"]

        for field in allowed_fields:
            if field in updates:
                reminder[field] = updates[field]

        reminder["updated_at"] = datetime.now().isoformat()
        self.data_manager.save_data("reminders", self.reminders)
        return reminder

    def snooze_reminder(self, reminder_id: str, snooze_minutes: int = 60) -> Optional[Dict[str, Any]]:
        """
        Snooze a reminder.

        Args:
            reminder_id: Reminder ID
            snooze_minutes: Minutes to snooze (default 1 hour)

        Returns:
            Updated reminder or None if not found
        """
        reminder = self.get_reminder_by_id(reminder_id)
        if not reminder:
            return None

        snooze_until = datetime.now() + timedelta(minutes=snooze_minutes)
        reminder["snooze_until"] = snooze_until.isoformat()
        reminder["status"] = "snoozed"
        reminder["updated_at"] = datetime.now().isoformat()

        self.data_manager.save_data("reminders", self.reminders)
        return reminder

    def complete_reminder(self, reminder_id: str) -> Optional[Dict[str, Any]]:
        """
        Mark a reminder as completed.

        Args:
            reminder_id: Reminder ID

        Returns:
            Updated reminder or None if not found
        """
        reminder = self.get_reminder_by_id(reminder_id)
        if not reminder:
            return None

        reminder["status"] = "completed"
        reminder["completed_at"] = datetime.now().isoformat()
        reminder["updated_at"] = datetime.now().isoformat()

        # If recurring, create next occurrence
        if reminder["recurrence"] != "once":
            self._create_next_recurrence(reminder)

        self.data_manager.save_data("reminders", self.reminders)
        return reminder

    def _create_next_recurrence(self, reminder: Dict[str, Any]) -> None:
        """
        Create next occurrence of a recurring reminder.

        Args:
            reminder: Original reminder object
        """
        # Check if we should stop recurring
        if reminder.get("recurrence_end_date"):
            end_date = datetime.fromisoformat(reminder["recurrence_end_date"])
            if datetime.now() >= end_date:
                return

        current_due = datetime.fromisoformat(reminder["due_datetime"])

        # Calculate next occurrence based on pattern
        if reminder["recurrence"] == "daily":
            next_due = current_due + timedelta(days=1)
        elif reminder["recurrence"] == "weekly":
            next_due = current_due + timedelta(weeks=1)
        elif reminder["recurrence"] == "monthly":
            # Add one month (approximate)
            next_due = current_due + timedelta(days=30)
        elif reminder["recurrence"] == "yearly":
            next_due = current_due + timedelta(days=365)
        else:
            return  # Don't create next for "once" or "custom"

        # Create new reminder instance
        self.create_reminder(
            title=reminder["title"],
            due_datetime=next_due.isoformat(),
            description=reminder["description"],
            priority=reminder["priority"],
            recurrence=reminder["recurrence"],
            recurrence_end_date=reminder.get("recurrence_end_date"),
            context=reminder.get("context"),
            linked_task_id=reminder.get("linked_task_id"),
        )

    def get_active_reminders(self, include_snoozed: bool = False) -> List[Dict[str, Any]]:
        """
        Get all active reminders.

        Args:
            include_snoozed: Whether to include snoozed reminders

        Returns:
            List of active reminders
        """
        now = datetime.now()
        active = []

        for reminder in self.reminders:
            if reminder["status"] == "active":
                active.append(reminder)
            elif reminder["status"] == "snoozed" and include_snoozed:
                # Check if snooze period has ended
                if reminder["snooze_until"]:
                    snooze_until = datetime.fromisoformat(reminder["snooze_until"])
                    if now >= snooze_until:
                        # Reactivate
                        reminder["status"] = "active"
                        reminder["snooze_until"] = None
                        active.append(reminder)
                    elif include_snoozed:
                        active.append(reminder)

        return active

    def get_due_reminders(self, hours_ahead: int = 24) -> List[Dict[str, Any]]:
        """
        Get reminders due within the next N hours.

        Args:
            hours_ahead: How many hours to look ahead

        Returns:
            List of due reminders
        """
        now = datetime.now()
        future = now + timedelta(hours=hours_ahead)

        active = self.get_active_reminders(include_snoozed=False)
        due = []

        for reminder in active:
            due_datetime = datetime.fromisoformat(reminder["due_datetime"])
            if now <= due_datetime <= future:
                due.append(reminder)

        # Sort by due datetime
        due.sort(key=lambda x: x["due_datetime"])
        return due

    def get_overdue_reminders(self) -> List[Dict[str, Any]]:
        """Get all overdue reminders."""
        now = datetime.now()
        active = self.get_active_reminders(include_snoozed=False)

        overdue = []
        for reminder in active:
            due_datetime = datetime.fromisoformat(reminder["due_datetime"])
            if due_datetime < now:
                overdue.append(reminder)

        return overdue

    def get_reminders_by_context(self, context: str) -> List[Dict[str, Any]]:
        """
        Get reminders by context.

        Args:
            context: Context to filter by

        Returns:
            List of reminders matching context
        """
        return [r for r in self.reminders if r.get("context") == context]

    def get_reminders_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get reminders by priority level."""
        active = self.get_active_reminders()
        return [r for r in active if r["priority"] == priority]

    def get_daily_reminder_summary(self) -> Dict[str, Any]:
        """
        Get daily reminder summary.

        Returns:
            Summary of reminders for the day
        """
        due_today = self.get_due_reminders(hours_ahead=24)
        overdue = self.get_overdue_reminders()

        # Group by priority
        high_priority = [r for r in due_today if r["priority"] == "high"]
        medium_priority = [r for r in due_today if r["priority"] == "medium"]
        low_priority = [r for r in due_today if r["priority"] == "low"]

        return {
            "date": datetime.now().date().isoformat(),
            "total_due_today": len(due_today),
            "total_overdue": len(overdue),
            "high_priority": len(high_priority),
            "medium_priority": len(medium_priority),
            "low_priority": len(low_priority),
            "top_reminders": sorted(
                due_today + overdue,
                key=lambda x: (
                    {"high": 0, "medium": 1, "low": 2}[x["priority"]],
                    x["due_datetime"]
                )
            )[:5],
        }

    def delete_reminder(self, reminder_id: str) -> bool:
        """
        Delete a reminder.

        Args:
            reminder_id: Reminder ID

        Returns:
            True if deleted, False if not found
        """
        for i, reminder in enumerate(self.reminders):
            if reminder["id"] == reminder_id:
                del self.reminders[i]
                self.data_manager.save_data("reminders", self.reminders)
                return True
        return False

    def cleanup_completed_reminders(self, days_old: int = 30) -> int:
        """
        Clean up old completed reminders.

        Args:
            days_old: Remove completed reminders older than this many days

        Returns:
            Number of reminders removed
        """
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()

        initial_count = len(self.reminders)

        self.reminders = [
            r for r in self.reminders
            if not (r["status"] == "completed" and r["completed_at"] and r["completed_at"] < cutoff_date)
        ]

        removed_count = initial_count - len(self.reminders)

        if removed_count > 0:
            self.data_manager.save_data("reminders", self.reminders)

        return removed_count
