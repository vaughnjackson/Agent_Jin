"""
Habit Tracking Module for Digital Life Assistant.

Handles habit creation, logging, streak counting, pattern analysis,
and motivation insights.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class HabitTracker:
    """Track habits with streak counting and pattern analysis."""

    FREQUENCIES = ["daily", "weekly", "custom"]
    CATEGORIES = ["wellness", "fitness", "productivity", "learning", "social", "other"]

    def __init__(self, data_manager):
        """
        Initialize HabitTracker with data persistence layer.

        Args:
            data_manager: DataManager instance for persistence
        """
        self.data_manager = data_manager
        self.habits = self.data_manager.load_data("habits")

    def create_habit(
        self,
        name: str,
        category: str = "other",
        target_frequency: str = "daily",
        target_count: int = 1,
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        Create a new habit to track.

        Args:
            name: Habit name
            category: Habit category
            target_frequency: How often (daily, weekly, custom)
            target_count: Number of times per frequency period
            notes: Optional notes about the habit

        Returns:
            Created habit object
        """
        if category not in self.CATEGORIES:
            category = "other"

        if target_frequency not in self.FREQUENCIES:
            target_frequency = "daily"

        habit = {
            "id": str(uuid.uuid4()),
            "name": name,
            "category": category,
            "target_frequency": target_frequency,
            "target_count": target_count,
            "notes": notes,
            "logs": [],
            "current_streak": 0,
            "longest_streak": 0,
            "created_at": datetime.now().isoformat(),
        }

        self.habits.append(habit)
        self.data_manager.save_data("habits", self.habits)
        return habit

    def get_habit_by_id(self, habit_id: str) -> Optional[Dict[str, Any]]:
        """Get a habit by ID."""
        for habit in self.habits:
            if habit["id"] == habit_id:
                return habit
        return None

    def get_habit_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a habit by name (case-insensitive)."""
        name_lower = name.lower()
        for habit in self.habits:
            if habit["name"].lower() == name_lower:
                return habit
        return None

    def log_habit(
        self,
        habit_id: str,
        date: Optional[str] = None,
        completed: bool = True,
        notes: str = "",
        value: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Log a habit completion.

        Args:
            habit_id: Habit ID
            date: Date in YYYY-MM-DD format (defaults to today)
            completed: Whether habit was completed
            notes: Optional notes about this log
            value: Optional numerical value (e.g., minutes exercised)

        Returns:
            Updated habit object
        """
        habit = self.get_habit_by_id(habit_id)
        if not habit:
            raise ValueError(f"Habit {habit_id} not found")

        if date is None:
            date = datetime.now().date().isoformat()

        # Check if already logged for this date
        existing_log = None
        for log in habit["logs"]:
            if log["date"] == date:
                existing_log = log
                break

        if existing_log:
            # Update existing log
            existing_log["completed"] = completed
            existing_log["notes"] = notes
            if value is not None:
                existing_log["value"] = value
        else:
            # Create new log
            log_entry = {
                "date": date,
                "completed": completed,
                "notes": notes,
                "logged_at": datetime.now().isoformat(),
            }
            if value is not None:
                log_entry["value"] = value

            habit["logs"].append(log_entry)

        # Sort logs by date
        habit["logs"].sort(key=lambda x: x["date"])

        # Recalculate streaks
        self._update_streaks(habit)

        self.data_manager.save_data("habits", self.habits)
        return habit

    def _update_streaks(self, habit: Dict[str, Any]) -> None:
        """
        Update current and longest streak for a habit.

        Args:
            habit: Habit object to update
        """
        if not habit["logs"]:
            habit["current_streak"] = 0
            habit["longest_streak"] = 0
            return

        # Sort logs by date (most recent first)
        completed_dates = sorted(
            [log["date"] for log in habit["logs"] if log["completed"]],
            reverse=True,
        )

        if not completed_dates:
            habit["current_streak"] = 0
            return

        # Calculate current streak
        today = datetime.now().date()
        current_streak = 0

        for i, date_str in enumerate(completed_dates):
            log_date = datetime.fromisoformat(date_str).date()

            if i == 0:
                # Most recent log
                days_since = (today - log_date).days
                if days_since > 1:
                    # Streak is broken
                    current_streak = 0
                    break
                else:
                    current_streak = 1
            else:
                # Check if consecutive
                prev_date = datetime.fromisoformat(completed_dates[i - 1]).date()
                if (prev_date - log_date).days == 1:
                    current_streak += 1
                else:
                    # Streak broken
                    break

        habit["current_streak"] = current_streak

        # Calculate longest streak
        longest = 0
        current = 0

        # Sort dates in chronological order for longest streak calculation
        sorted_dates = sorted([datetime.fromisoformat(d).date() for d in completed_dates])

        for i, log_date in enumerate(sorted_dates):
            if i == 0:
                current = 1
            else:
                prev_date = sorted_dates[i - 1]
                if (log_date - prev_date).days == 1:
                    current += 1
                else:
                    longest = max(longest, current)
                    current = 1

        longest = max(longest, current)
        habit["longest_streak"] = max(habit["longest_streak"], longest)

    def get_habit_stats(self, habit_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get statistics for a habit over a period.

        Args:
            habit_id: Habit ID
            days: Number of days to analyze

        Returns:
            Statistics dictionary
        """
        habit = self.get_habit_by_id(habit_id)
        if not habit:
            return {}

        cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()

        recent_logs = [
            log for log in habit["logs"]
            if log["date"] >= cutoff_date
        ]

        completed_logs = [log for log in recent_logs if log["completed"]]
        completion_count = len(completed_logs)

        # Calculate completion rate
        completion_rate = (completion_count / days * 100) if days > 0 else 0

        # Calculate average value if tracked
        avg_value = None
        if completed_logs and "value" in completed_logs[0]:
            values = [log.get("value", 0) for log in completed_logs if "value" in log]
            avg_value = sum(values) / len(values) if values else None

        return {
            "habit_name": habit["name"],
            "period_days": days,
            "total_completions": completion_count,
            "completion_rate": round(completion_rate, 1),
            "current_streak": habit["current_streak"],
            "longest_streak": habit["longest_streak"],
            "average_value": round(avg_value, 2) if avg_value else None,
        }

    def get_all_habits_summary(self) -> List[Dict[str, Any]]:
        """
        Get summary of all habits with current streaks.

        Returns:
            List of habit summaries
        """
        summaries = []
        for habit in self.habits:
            summaries.append({
                "id": habit["id"],
                "name": habit["name"],
                "category": habit["category"],
                "current_streak": habit["current_streak"],
                "longest_streak": habit["longest_streak"],
                "total_logs": len(habit["logs"]),
            })
        return summaries

    def get_habits_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all habits in a specific category."""
        return [h for h in self.habits if h["category"] == category]

    def get_daily_habit_checklist(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get checklist of daily habits and their completion status.

        Args:
            date: Date in YYYY-MM-DD format (defaults to today)

        Returns:
            Checklist with completion status
        """
        if date is None:
            date = datetime.now().date().isoformat()

        checklist = []
        for habit in self.habits:
            if habit["target_frequency"] == "daily":
                # Check if logged for this date
                completed = False
                log_entry = None

                for log in habit["logs"]:
                    if log["date"] == date:
                        completed = log["completed"]
                        log_entry = log
                        break

                checklist.append({
                    "habit_id": habit["id"],
                    "name": habit["name"],
                    "category": habit["category"],
                    "completed": completed,
                    "current_streak": habit["current_streak"],
                    "log": log_entry,
                })

        return {
            "date": date,
            "total_habits": len(checklist),
            "completed": len([h for h in checklist if h["completed"]]),
            "habits": checklist,
        }

    def get_streak_milestones(self, habit_id: str) -> Dict[str, Any]:
        """
        Get streak milestone information and motivation.

        Args:
            habit_id: Habit ID

        Returns:
            Milestone information
        """
        habit = self.get_habit_by_id(habit_id)
        if not habit:
            return {}

        current_streak = habit["current_streak"]
        longest_streak = habit["longest_streak"]

        # Define milestone levels
        milestones = [7, 14, 21, 30, 60, 90, 100, 180, 365]

        # Find next milestone
        next_milestone = None
        for milestone in milestones:
            if current_streak < milestone:
                next_milestone = milestone
                break

        # Find last achieved milestone
        last_milestone = None
        for milestone in reversed(milestones):
            if current_streak >= milestone:
                last_milestone = milestone
                break

        days_to_next = next_milestone - current_streak if next_milestone else None

        # Generate motivation message
        motivation = self._generate_motivation_message(current_streak, days_to_next, longest_streak)

        return {
            "habit_name": habit["name"],
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "last_milestone": last_milestone,
            "next_milestone": next_milestone,
            "days_to_next_milestone": days_to_next,
            "motivation_message": motivation,
        }

    def _generate_motivation_message(
        self,
        current_streak: int,
        days_to_next: Optional[int],
        longest_streak: int,
    ) -> str:
        """Generate motivational message based on streak."""
        if current_streak == 0:
            return "Start your streak today! Every journey begins with a single step."
        elif current_streak == 1:
            return "Great start! Keep it going tomorrow."
        elif current_streak < 7:
            return f"Building momentum! {days_to_next} more days to your 1-week milestone."
        elif current_streak < 14:
            return f"Solid first week! {days_to_next} more days to 2 weeks."
        elif current_streak < 21:
            return f"You're forming a habit! {days_to_next} more days to 3 weeks (habit formation zone)."
        elif current_streak < 30:
            return f"Amazing consistency! {days_to_next} more days to 1 month."
        elif current_streak == longest_streak and current_streak >= 30:
            return f"Personal record! You're at {current_streak} days - your longest streak ever!"
        elif days_to_next and days_to_next <= 7:
            return f"So close! Just {days_to_next} more days to your next milestone."
        else:
            return f"Incredible dedication! Keep up your {current_streak}-day streak!"

    def delete_habit(self, habit_id: str) -> bool:
        """
        Delete a habit.

        Args:
            habit_id: Habit ID

        Returns:
            True if deleted, False if not found
        """
        for i, habit in enumerate(self.habits):
            if habit["id"] == habit_id:
                del self.habits[i]
                self.data_manager.save_data("habits", self.habits)
                return True
        return False
