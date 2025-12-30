"""
Progress Tracking Module for Digital Life Assistant.

Handles goal management, milestone tracking, reflection prompts,
and progress visualization for personal growth.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class ProgressTracker:
    """Track personal growth goals and milestones."""

    CATEGORIES = ["fitness", "career", "learning", "financial", "relationships", "wellness", "creative", "other"]
    STATUSES = ["planning", "in-progress", "completed", "on-hold", "cancelled"]

    def __init__(self, data_manager):
        """
        Initialize ProgressTracker with data persistence layer.

        Args:
            data_manager: DataManager instance for persistence
        """
        self.data_manager = data_manager
        self.goals = self.data_manager.load_data("progress")

    def create_goal(
        self,
        title: str,
        description: str = "",
        category: str = "other",
        target_date: Optional[str] = None,
        milestones: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new goal.

        Args:
            title: Goal title
            description: Detailed description
            category: Goal category
            target_date: Target completion date (YYYY-MM-DD)
            milestones: List of milestone dictionaries with 'title' key

        Returns:
            Created goal object
        """
        if category not in self.CATEGORIES:
            category = "other"

        # Process milestones
        processed_milestones = []
        if milestones:
            for milestone in milestones:
                processed_milestones.append({
                    "id": str(uuid.uuid4()),
                    "title": milestone.get("title", ""),
                    "target_date": milestone.get("target_date"),
                    "completed": False,
                    "completed_at": None,
                    "notes": milestone.get("notes", ""),
                })

        goal = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "category": category,
            "target_date": target_date,
            "milestones": processed_milestones,
            "progress_percentage": 0,
            "status": "planning",
            "reflections": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.goals.append(goal)
        self.data_manager.save_data("progress", self.goals)
        return goal

    def get_goal_by_id(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Get a goal by ID."""
        for goal in self.goals:
            if goal["id"] == goal_id:
                return goal
        return None

    def update_goal(self, goal_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a goal.

        Args:
            goal_id: Goal ID
            updates: Dictionary of fields to update

        Returns:
            Updated goal or None if not found
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return None

        allowed_fields = ["title", "description", "category", "target_date", "status", "progress_percentage"]
        for field in allowed_fields:
            if field in updates:
                goal[field] = updates[field]

        goal["updated_at"] = datetime.now().isoformat()
        self.data_manager.save_data("progress", self.goals)
        return goal

    def add_milestone(
        self,
        goal_id: str,
        title: str,
        target_date: Optional[str] = None,
        notes: str = "",
    ) -> Optional[Dict[str, Any]]:
        """
        Add a milestone to a goal.

        Args:
            goal_id: Goal ID
            title: Milestone title
            target_date: Target completion date
            notes: Optional notes

        Returns:
            Updated goal or None if not found
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return None

        milestone = {
            "id": str(uuid.uuid4()),
            "title": title,
            "target_date": target_date,
            "completed": False,
            "completed_at": None,
            "notes": notes,
        }

        goal["milestones"].append(milestone)
        self._recalculate_progress(goal)

        goal["updated_at"] = datetime.now().isoformat()
        self.data_manager.save_data("progress", self.goals)
        return goal

    def complete_milestone(
        self,
        goal_id: str,
        milestone_id: str,
        notes: str = "",
    ) -> Optional[Dict[str, Any]]:
        """
        Mark a milestone as completed.

        Args:
            goal_id: Goal ID
            milestone_id: Milestone ID
            notes: Optional completion notes

        Returns:
            Updated goal or None if not found
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return None

        for milestone in goal["milestones"]:
            if milestone["id"] == milestone_id:
                milestone["completed"] = True
                milestone["completed_at"] = datetime.now().isoformat()
                if notes:
                    milestone["notes"] = notes
                break

        self._recalculate_progress(goal)

        goal["updated_at"] = datetime.now().isoformat()
        self.data_manager.save_data("progress", self.goals)
        return goal

    def _recalculate_progress(self, goal: Dict[str, Any]) -> None:
        """
        Recalculate progress percentage based on completed milestones.

        Args:
            goal: Goal object to update
        """
        if not goal["milestones"]:
            return

        completed_count = sum(1 for m in goal["milestones"] if m["completed"])
        total_count = len(goal["milestones"])

        goal["progress_percentage"] = round((completed_count / total_count) * 100)

        # Auto-update status based on progress
        if goal["progress_percentage"] == 100 and goal["status"] != "completed":
            goal["status"] = "completed"
        elif goal["progress_percentage"] > 0 and goal["status"] == "planning":
            goal["status"] = "in-progress"

    def add_reflection(
        self,
        goal_id: str,
        content: str,
        reflection_type: str = "general",
    ) -> Optional[Dict[str, Any]]:
        """
        Add a reflection entry to a goal.

        Args:
            goal_id: Goal ID
            content: Reflection content
            reflection_type: Type (general, weekly, monthly, quarterly)

        Returns:
            Updated goal or None if not found
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return None

        reflection = {
            "id": str(uuid.uuid4()),
            "type": reflection_type,
            "content": content,
            "created_at": datetime.now().isoformat(),
        }

        goal["reflections"].append(reflection)
        goal["updated_at"] = datetime.now().isoformat()
        self.data_manager.save_data("progress", self.goals)
        return goal

    def get_reflection_prompts(self, goal_id: str) -> List[str]:
        """
        Get guided reflection prompts for a goal.

        Args:
            goal_id: Goal ID

        Returns:
            List of reflection prompts
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return []

        prompts = [
            f"What progress have you made on '{goal['title']}' this week?",
            "What obstacles or challenges did you encounter?",
            "What did you learn about yourself through this process?",
            "What adjustments should you make to your approach?",
            "Who or what helped you make progress?",
            "What are you most proud of so far?",
            "What's your next small step forward?",
        ]

        # Add category-specific prompts
        if goal["category"] == "fitness":
            prompts.extend([
                "How is your body responding to your training?",
                "What changes have you noticed in your energy levels?",
            ])
        elif goal["category"] == "learning":
            prompts.extend([
                "What new concepts or skills have you mastered?",
                "How are you applying what you've learned?",
            ])
        elif goal["category"] == "career":
            prompts.extend([
                "What professional relationships have you strengthened?",
                "What new opportunities have emerged?",
            ])

        return prompts

    def get_goals_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get all goals with a specific status."""
        return [g for g in self.goals if g["status"] == status]

    def get_goals_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all goals in a specific category."""
        return [g for g in self.goals if g["category"] == category]

    def get_upcoming_milestones(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get upcoming milestones across all goals.

        Args:
            days: Number of days to look ahead

        Returns:
            List of upcoming milestones with goal context
        """
        future_date = (datetime.now() + timedelta(days=days)).date().isoformat()
        upcoming = []

        for goal in self.goals:
            if goal["status"] in ["in-progress", "planning"]:
                for milestone in goal["milestones"]:
                    if (
                        not milestone["completed"]
                        and milestone["target_date"]
                        and milestone["target_date"] <= future_date
                    ):
                        upcoming.append({
                            "goal_id": goal["id"],
                            "goal_title": goal["title"],
                            "milestone_id": milestone["id"],
                            "milestone_title": milestone["title"],
                            "target_date": milestone["target_date"],
                        })

        # Sort by target date
        upcoming.sort(key=lambda x: x["target_date"])
        return upcoming

    def get_progress_summary(self, goal_id: str) -> Dict[str, Any]:
        """
        Get comprehensive progress summary for a goal.

        Args:
            goal_id: Goal ID

        Returns:
            Progress summary
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return {}

        total_milestones = len(goal["milestones"])
        completed_milestones = sum(1 for m in goal["milestones"] if m["completed"])
        pending_milestones = total_milestones - completed_milestones

        # Calculate days since creation
        created_date = datetime.fromisoformat(goal["created_at"]).date()
        days_active = (datetime.now().date() - created_date).days

        # Calculate days until target
        days_until_target = None
        if goal["target_date"]:
            target_date = datetime.fromisoformat(goal["target_date"]).date()
            days_until_target = (target_date - datetime.now().date()).days

        # Determine if on track
        on_track = None
        if days_until_target and days_until_target > 0 and total_milestones > 0:
            expected_progress = (days_active / (days_active + days_until_target)) * 100
            actual_progress = goal["progress_percentage"]
            on_track = actual_progress >= expected_progress

        return {
            "goal_id": goal["id"],
            "title": goal["title"],
            "category": goal["category"],
            "status": goal["status"],
            "progress_percentage": goal["progress_percentage"],
            "total_milestones": total_milestones,
            "completed_milestones": completed_milestones,
            "pending_milestones": pending_milestones,
            "days_active": days_active,
            "days_until_target": days_until_target,
            "on_track": on_track,
            "recent_reflections": goal["reflections"][-3:] if goal["reflections"] else [],
        }

    def get_all_goals_overview(self) -> Dict[str, Any]:
        """
        Get overview of all goals.

        Returns:
            Summary of all goals by status and category
        """
        overview = {
            "total_goals": len(self.goals),
            "by_status": {},
            "by_category": {},
            "total_milestones": 0,
            "completed_milestones": 0,
        }

        for goal in self.goals:
            # Count by status
            status = goal["status"]
            overview["by_status"][status] = overview["by_status"].get(status, 0) + 1

            # Count by category
            category = goal["category"]
            overview["by_category"][category] = overview["by_category"].get(category, 0) + 1

            # Count milestones
            overview["total_milestones"] += len(goal["milestones"])
            overview["completed_milestones"] += sum(1 for m in goal["milestones"] if m["completed"])

        return overview

    def generate_weekly_review(self) -> Dict[str, Any]:
        """
        Generate a weekly progress review across all goals.

        Returns:
            Weekly review summary
        """
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()

        # Find recently completed milestones
        recent_completions = []
        for goal in self.goals:
            for milestone in goal["milestones"]:
                if milestone["completed"] and milestone["completed_at"] >= week_ago:
                    recent_completions.append({
                        "goal_title": goal["title"],
                        "milestone_title": milestone["title"],
                        "completed_at": milestone["completed_at"],
                    })

        # Find active goals with progress
        active_goals = self.get_goals_by_status("in-progress")

        # Find upcoming milestones
        upcoming = self.get_upcoming_milestones(days=7)

        return {
            "period": "Last 7 days",
            "milestones_completed": len(recent_completions),
            "recent_completions": recent_completions,
            "active_goals": len(active_goals),
            "upcoming_milestones": upcoming,
            "reflection_prompt": "What was your biggest win this week? What will you focus on next week?",
        }

    def delete_goal(self, goal_id: str) -> bool:
        """
        Delete a goal.

        Args:
            goal_id: Goal ID

        Returns:
            True if deleted, False if not found
        """
        for i, goal in enumerate(self.goals):
            if goal["id"] == goal_id:
                del self.goals[i]
                self.data_manager.save_data("progress", self.goals)
                return True
        return False
