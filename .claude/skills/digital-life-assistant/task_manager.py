"""
Task Management Module for Digital Life Assistant.

Handles task creation, prioritization using Eisenhower Matrix (Urgent/Important),
completion tracking, and productivity analytics.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class TaskManager:
    """Manage tasks with smart prioritization and completion tracking."""

    PRIORITY_LEVELS = ["low", "medium", "high", "urgent"]
    CATEGORIES = ["work", "personal", "health", "learning", "finance", "social", "other"]
    STATUSES = ["pending", "in-progress", "completed", "cancelled"]

    def __init__(self, data_manager):
        """
        Initialize TaskManager with data persistence layer.

        Args:
            data_manager: DataManager instance for persistence
        """
        self.data_manager = data_manager
        self.tasks = self.data_manager.load_data("tasks")

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: Optional[str] = None,
        category: str = "other",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new task.

        Args:
            title: Task title
            description: Optional task description
            priority: Priority level (low, medium, high, urgent)
            due_date: Due date in YYYY-MM-DD format
            category: Task category
            tags: Optional list of tags

        Returns:
            Created task object
        """
        if priority not in self.PRIORITY_LEVELS:
            priority = "medium"

        if category not in self.CATEGORIES:
            category = "other"

        task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending",
            "due_date": due_date,
            "category": category,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "updated_at": datetime.now().isoformat(),
        }

        self.tasks.append(task)
        self.data_manager.save_data("tasks", self.tasks)
        return task

    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a task by ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a task.

        Args:
            task_id: Task ID
            updates: Dictionary of fields to update

        Returns:
            Updated task or None if not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        # Update allowed fields
        allowed_fields = ["title", "description", "priority", "status", "due_date", "category", "tags"]
        for field in allowed_fields:
            if field in updates:
                task[field] = updates[field]

        task["updated_at"] = datetime.now().isoformat()

        # If status changed to completed, set completed_at
        if updates.get("status") == "completed" and task["status"] == "completed":
            task["completed_at"] = datetime.now().isoformat()

        self.data_manager.save_data("tasks", self.tasks)
        return task

    def complete_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Mark a task as completed."""
        return self.update_task(task_id, {"status": "completed"})

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False if not found
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                del self.tasks[i]
                self.data_manager.save_data("tasks", self.tasks)
                return True
        return False

    def get_tasks_by_filter(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        due_before: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get tasks filtered by various criteria.

        Args:
            status: Filter by status
            priority: Filter by priority
            category: Filter by category
            due_before: Filter tasks due before this date (YYYY-MM-DD)
            tags: Filter tasks containing any of these tags

        Returns:
            List of matching tasks
        """
        filtered_tasks = self.tasks.copy()

        if status:
            filtered_tasks = [t for t in filtered_tasks if t["status"] == status]

        if priority:
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority]

        if category:
            filtered_tasks = [t for t in filtered_tasks if t["category"] == category]

        if due_before:
            filtered_tasks = [
                t for t in filtered_tasks if t["due_date"] and t["due_date"] <= due_before
            ]

        if tags:
            filtered_tasks = [
                t for t in filtered_tasks if any(tag in t["tags"] for tag in tags)
            ]

        return filtered_tasks

    def get_tasks_by_eisenhower_matrix(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categorize tasks using Eisenhower Matrix (Urgent/Important).

        Returns:
            Dictionary with four quadrants:
            - urgent_important: Do first
            - not_urgent_important: Schedule
            - urgent_not_important: Delegate
            - not_urgent_not_important: Eliminate
        """
        today = datetime.now().date()
        matrix = {
            "urgent_important": [],
            "not_urgent_important": [],
            "urgent_not_important": [],
            "not_urgent_not_important": [],
        }

        pending_tasks = self.get_tasks_by_filter(status="pending")

        for task in pending_tasks:
            is_urgent = False
            is_important = task["priority"] in ["high", "urgent"]

            # Determine urgency based on due date
            if task["due_date"]:
                due_date = datetime.fromisoformat(task["due_date"]).date()
                days_until_due = (due_date - today).days
                is_urgent = days_until_due <= 2  # Due within 2 days

            # Also consider explicit "urgent" priority
            if task["priority"] == "urgent":
                is_urgent = True

            # Categorize into quadrant
            if is_urgent and is_important:
                matrix["urgent_important"].append(task)
            elif not is_urgent and is_important:
                matrix["not_urgent_important"].append(task)
            elif is_urgent and not is_important:
                matrix["urgent_not_important"].append(task)
            else:
                matrix["not_urgent_not_important"].append(task)

        return matrix

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get all overdue tasks."""
        today = datetime.now().date().isoformat()
        pending_tasks = self.get_tasks_by_filter(status="pending")
        return [t for t in pending_tasks if t["due_date"] and t["due_date"] < today]

    def get_today_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks due today."""
        today = datetime.now().date().isoformat()
        return self.get_tasks_by_filter(status="pending", due_before=today)

    def get_upcoming_tasks(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get tasks due in the next N days.

        Args:
            days: Number of days to look ahead

        Returns:
            List of upcoming tasks
        """
        today = datetime.now().date()
        future_date = (today + timedelta(days=days)).isoformat()
        return self.get_tasks_by_filter(status="pending", due_before=future_date)

    def get_productivity_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Calculate productivity statistics.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with productivity metrics
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        recent_completed = [
            t for t in self.tasks
            if t["status"] == "completed" and t["completed_at"] and t["completed_at"] >= cutoff_date
        ]

        recent_created = [
            t for t in self.tasks
            if t["created_at"] >= cutoff_date
        ]

        # Category breakdown
        category_counts = {}
        for task in recent_completed:
            cat = task["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Calculate completion rate
        total_tasks = len(recent_created)
        completed_tasks = len(recent_completed)
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return {
            "period_days": days,
            "total_created": total_tasks,
            "total_completed": completed_tasks,
            "completion_rate": round(completion_rate, 1),
            "category_breakdown": category_counts,
            "avg_tasks_per_day": round(completed_tasks / days, 1) if days > 0 else 0,
            "pending_tasks": len(self.get_tasks_by_filter(status="pending")),
            "overdue_tasks": len(self.get_overdue_tasks()),
        }

    def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort tasks by priority (urgent > high > medium > low) and due date.

        Args:
            tasks: List of tasks to prioritize

        Returns:
            Sorted list of tasks
        """
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}

        def sort_key(task):
            priority_score = priority_order.get(task["priority"], 4)
            # Tasks without due dates go to the end
            due_date = task["due_date"] if task["due_date"] else "9999-12-31"
            return (priority_score, due_date)

        return sorted(tasks, key=sort_key)

    def get_daily_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive daily summary.

        Returns:
            Summary of today's tasks and priorities
        """
        today_tasks = self.get_today_tasks()
        overdue_tasks = self.get_overdue_tasks()
        matrix = self.get_tasks_by_eisenhower_matrix()

        prioritized_today = self.prioritize_tasks(today_tasks)

        return {
            "date": datetime.now().date().isoformat(),
            "total_tasks_today": len(today_tasks),
            "overdue_tasks": len(overdue_tasks),
            "urgent_important": len(matrix["urgent_important"]),
            "top_priorities": prioritized_today[:5],  # Top 5 tasks
            "eisenhower_matrix": {
                "do_first": len(matrix["urgent_important"]),
                "schedule": len(matrix["not_urgent_important"]),
                "delegate": len(matrix["urgent_not_important"]),
                "eliminate": len(matrix["not_urgent_not_important"]),
            },
        }
