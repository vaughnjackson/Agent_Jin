#!/usr/bin/env python3
"""
Digital Life Assistant - Main Interface
Simple command-line interface for quick interactions with your life management system.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from data_manager import DataManager
from task_manager import TaskManager
from habit_tracker import HabitTracker
from progress_tracker import ProgressTracker
from schedule_organizer import ScheduleOrganizer
from reminder_system import ReminderSystem


class DigitalLifeAssistant:
    """Main interface for the Digital Life Assistant."""

    def __init__(self):
        """Initialize all modules."""
        data_dir = os.path.join(script_dir, "data")
        self.data_manager = DataManager(data_dir=data_dir)
        self.task_manager = TaskManager(self.data_manager)
        self.habit_tracker = HabitTracker(self.data_manager)
        self.progress_tracker = ProgressTracker(self.data_manager)
        self.schedule_organizer = ScheduleOrganizer(self.data_manager)
        self.reminder_system = ReminderSystem(self.data_manager)

    def get_daily_overview(self, date_str=None):
        """Get complete overview for a specific date (defaults to today)."""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")

        overview = {
            "date": date_str,
            "tasks": self._get_tasks_for_date(date_str),
            "schedule": self._get_schedule_for_date(date_str),
            "habits": self._get_habits_to_track(),
            "reminders": self._get_active_reminders(),
            "goals": self._get_active_goals()
        }
        return overview

    def _get_tasks_for_date(self, date_str):
        """Get tasks for a specific date."""
        tasks = []
        date = datetime.strptime(date_str, "%Y-%m-%d")
        week_from_now = (date + timedelta(days=7)).strftime("%Y-%m-%d")

        for task in self.task_manager.tasks:
            if task["status"] in ["pending", "in-progress"]:
                # Include all pending tasks (overdue, due today, or due within next week)
                if task.get("due_date"):
                    if task["due_date"] <= week_from_now:
                        tasks.append(task)
                else:
                    # No due date - include it
                    tasks.append(task)

        return sorted(tasks, key=lambda t: (
            {"urgent": 0, "high": 1, "medium": 2, "low": 3}.get(t["priority"], 4),
            t.get("due_date", "9999-12-31")
        ))

    def _get_schedule_for_date(self, date_str):
        """Get schedule events for a specific date."""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = date.strftime("%A")

        events = []
        for event in self.schedule_organizer.events:
            event_date = datetime.fromisoformat(event["start_time"])

            if event["recurring"]:
                pattern = event.get("recurrence_pattern", "")
                if pattern == "daily":
                    events.append(event)
                elif pattern == "weekly_mwf" and day_name in ["Monday", "Wednesday", "Friday"]:
                    events.append(event)
            else:
                if event_date.date() == date.date():
                    events.append(event)

        return sorted(events, key=lambda e: e["start_time"])

    def _get_habits_to_track(self):
        """Get habits that should be tracked."""
        return [
            {
                "id": h["id"],
                "name": h["name"],
                "category": h["category"],
                "target_frequency": h["target_frequency"],
                "current_streak": h["current_streak"],
                "longest_streak": h["longest_streak"]
            }
            for h in self.habit_tracker.habits
        ]

    def _get_active_reminders(self):
        """Get active reminders."""
        now = datetime.now()
        active = []
        for reminder in self.reminder_system.reminders:
            if reminder["status"] == "active":
                due = datetime.fromisoformat(reminder["due_datetime"])
                if due >= now - timedelta(hours=24):  # Show reminders from last 24h
                    active.append(reminder)
        return sorted(active, key=lambda r: r["due_datetime"])

    def _get_active_goals(self):
        """Get active goals."""
        return [
            g for g in self.progress_tracker.goals
            if g.get("status") in ["active", "in-progress", None]
        ]

    def format_daily_overview(self, overview):
        """Format the daily overview as readable text."""
        output = []
        date = overview["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A, %B %d, %Y")

        output.append(f"# Daily Overview - {day_name}")
        output.append("")

        # Tasks
        tasks = overview["tasks"]
        if tasks:
            output.append(f"## 🎯 Priority Tasks ({len(tasks)} pending)")
            output.append("")
            for i, task in enumerate(tasks, 1):
                priority = task["priority"].upper()
                title = task["title"]
                due = task.get("due_date", "No due date")
                output.append(f"{i}. **{priority}**: {title}")
                output.append(f"   Due: {due} | Category: {task['category']}")
                if task.get("description"):
                    output.append(f"   {task['description']}")
                output.append("")

        # Schedule
        schedule = overview["schedule"]
        if schedule:
            output.append(f"## 📅 Calendar ({len(schedule)} events)")
            output.append("")
            for event in schedule:
                start = datetime.fromisoformat(event["start_time"])
                end = datetime.fromisoformat(event["end_time"])
                time_range = f"{start.strftime('%I:%M%p').lstrip('0').lower()} - {end.strftime('%I:%M%p').lstrip('0').lower()}"
                recurring = "🔄" if event["recurring"] else "📅"
                output.append(f"- {recurring} **{time_range}**: {event['title']}")
                if event.get("description"):
                    output.append(f"  {event['description']}")
            output.append("")

        # Habits
        habits = overview["habits"]
        if habits:
            output.append(f"## ✅ Habits to Track ({len(habits)} total)")
            output.append("")
            for habit in habits:
                streak_info = f"Streak: {habit['current_streak']} days (best: {habit['longest_streak']})"
                output.append(f"- ☐ **{habit['name']}** ({habit['target_frequency']}) - {streak_info}")
            output.append("")

        # Reminders
        reminders = overview["reminders"]
        if reminders:
            output.append(f"## 🔔 Active Reminders ({len(reminders)})")
            output.append("")
            for reminder in reminders:
                due = datetime.fromisoformat(reminder["due_datetime"])
                due_str = due.strftime("%I:%M%p on %b %d").lstrip('0')
                output.append(f"- **{reminder['title']}** - {due_str}")
                if reminder.get("description"):
                    output.append(f"  {reminder['description']}")
            output.append("")

        # Goals
        goals = overview["goals"]
        if goals:
            output.append(f"## 🎯 Active Goals ({len(goals)})")
            output.append("")
            for goal in goals:
                progress = goal.get("progress_percentage", 0)
                target = goal.get("target_date", "No target date")
                output.append(f"- **{goal['title']}** - {progress}% complete (target: {target})")
            output.append("")

        return "\n".join(output)


def main():
    """CLI interface."""
    assistant = DigitalLifeAssistant()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command in ["today", "overview"]:
            overview = assistant.get_daily_overview()
            print(assistant.format_daily_overview(overview))

        elif command == "tasks":
            tasks = assistant.task_manager.get_pending_tasks()
            print(f"Pending Tasks: {len(tasks)}")
            for task in tasks:
                print(f"- [{task['priority'].upper()}] {task['title']}")

        elif command == "habits":
            habits = assistant._get_habits_to_track()
            print(f"Habits to Track: {len(habits)}")
            for habit in habits:
                print(f"- {habit['name']} (streak: {habit['current_streak']} days)")

        elif command == "goals":
            goals = assistant._get_active_goals()
            print(f"Active Goals: {len(goals)}")
            for goal in goals:
                print(f"- {goal['title']} ({goal.get('progress_percentage', 0)}% complete)")

        else:
            print(f"Unknown command: {command}")
            print("Usage: python assistant.py [today|tasks|habits|goals]")
    else:
        # Default: show today's overview
        overview = assistant.get_daily_overview()
        print(assistant.format_daily_overview(overview))


if __name__ == "__main__":
    main()
