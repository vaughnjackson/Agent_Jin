# Digital Life Assistant - Production Skill

**Version**: 1.0.0
**Category**: Personal Productivity
**Author**: Claude Skills Factory
**License**: MIT

---

## Overview

The **Digital Life Assistant** is a comprehensive personal life management system powered by Claude Code. It helps you track personal growth, manage daily tasks, build healthy habits, organize your schedule, and never miss important follow-ups.

### Key Features

- **Personal Growth Tracking**: Set SMART goals, track milestones, reflect on progress
- **Task Management**: Smart prioritization with Eisenhower Matrix, deadline tracking
- **Habit Building**: Streak counting, wellness goals, pattern analysis
- **Schedule Organization**: Calendar management, conflict detection, time blocking
- **Reminders**: Smart alerts, recurring patterns, context-based notifications
- **Local Data Storage**: All data stored locally for privacy (JSON format)
- **Optional API Integration**: Hooks for Google Calendar, Notion, Todoist

---

## Installation

### Quick Install (Recommended)

```bash
# Copy skill to personal Claude Code skills directory
cp -r digital-life-assistant ~/.claude/skills/

# Create data directory
mkdir -p ~/.claude/skills/digital-life-assistant/data

# Verify installation
cd ~/.claude/skills/digital-life-assistant
ls -la
```

### Project-Level Install

```bash
# Copy to project-specific skills directory
mkdir -p .claude/skills
cp -r digital-life-assistant .claude/skills/

# Create data directory
mkdir -p .claude/skills/digital-life-assistant/data
```

### Verify Installation

Open Claude Code and ask:
```
Hey Claude, can you show me my tasks for today?
```

If the skill is loaded, Claude will respond with task management capabilities.

---

## File Structure

```
digital-life-assistant/
├── SKILL.md                    # Main skill definition with YAML frontmatter
├── README.md                   # This file
├── HOW_TO_USE.md              # Usage examples and invocation patterns
├── task_manager.py            # Task creation, prioritization, analytics
├── habit_tracker.py           # Habit logging, streak counting, motivation
├── progress_tracker.py        # Goal management, milestone tracking
├── schedule_organizer.py      # Calendar events, conflict detection
├── reminder_system.py         # Reminders with recurring patterns
├── data_manager.py            # JSON persistence, backup, validation
├── sample_input.json          # Example input format
├── expected_output.json       # Example output format
├── config.example.json        # Configuration template
└── data/                      # Data directory (created on first run)
    ├── tasks.json
    ├── habits.json
    ├── progress.json
    ├── schedule.json
    ├── reminders.json
    └── backups/               # Automatic backups (last 30 kept)
```

---

## Quick Start

### 1. First Time Setup

```
Hey Claude, I just installed the digital-life-assistant skill. Help me get started!
```

Claude will guide you through:
- Creating your first goal
- Adding initial tasks
- Setting up habits to track
- Understanding the interface

### 2. Daily Usage

**Morning:**
```
Good morning! What's on my plate today?
```

**Throughout the day:**
```
Log my workout - 30 minutes running
Mark task "Finish report" as complete
What's my meditation streak?
```

**Evening:**
```
Show what I accomplished today
Set a reminder to call mom tomorrow at 2pm
```

### 3. Weekly Review

```
Generate my weekly progress review
```

---

## Core Capabilities

### Task Management

**Create Tasks:**
```
Add a task: Finish quarterly report by Friday, high priority
```

**Prioritize with Eisenhower Matrix:**
- **Urgent & Important**: Do first
- **Important, Not Urgent**: Schedule
- **Urgent, Not Important**: Delegate
- **Neither**: Eliminate

**Track Completion:**
- View today's tasks
- Check overdue items
- Analyze productivity trends

### Habit Tracking

**Log Habits:**
```
Log my morning meditation - 10 minutes
```

**Track Streaks:**
- Current streak counter
- Longest streak achieved
- Milestone alerts (7, 14, 21, 30+ days)

**Get Motivated:**
- Personalized encouragement
- Progress visualization
- Pattern analysis

### Goal & Progress Tracking

**Set Goals:**
```
Create a goal to run a 5K race by June 2026
```

**Track Milestones:**
- Define checkpoints
- Mark achievements
- Calculate progress percentage

**Reflect:**
- Guided reflection prompts
- Weekly/monthly reviews
- Insights and recommendations

### Schedule Organization

**Manage Events:**
```
Create event: Team meeting tomorrow 2-3pm
```

**Detect Conflicts:**
- Automatic overlap detection
- Scheduling suggestions
- Time blocking

**Optional Google Calendar Sync:**
- Two-way synchronization
- Requires API setup (see configuration)

### Reminders

**Set Reminders:**
```
Remind me to submit expense report on Friday at 10am
```

**Recurring Patterns:**
- Daily, weekly, monthly, yearly
- Custom recurrence
- Snooze and reschedule

---

## Python Modules

### task_manager.py

**Key Functions:**
- `create_task()`: Add new task with priority/category/tags
- `get_tasks_by_eisenhower_matrix()`: Smart prioritization
- `get_daily_summary()`: Today's task overview
- `get_productivity_stats()`: Analytics and trends

### habit_tracker.py

**Key Functions:**
- `create_habit()`: Define new habit to track
- `log_habit()`: Record habit completion
- `get_streak_milestones()`: Current streak and motivation
- `get_daily_habit_checklist()`: Today's habit status

### progress_tracker.py

**Key Functions:**
- `create_goal()`: Set new goal with milestones
- `complete_milestone()`: Mark milestone achieved
- `add_reflection()`: Log personal reflections
- `generate_weekly_review()`: Summary and insights

### schedule_organizer.py

**Key Functions:**
- `create_event()`: Add calendar event
- `detect_conflicts()`: Find scheduling overlaps
- `create_time_block()`: Auto-find available time
- `get_daily_schedule()`: Today's calendar view

### reminder_system.py

**Key Functions:**
- `create_reminder()`: Set new reminder
- `snooze_reminder()`: Postpone notification
- `get_due_reminders()`: Upcoming alerts
- `complete_reminder()`: Mark done (handles recurrence)

### data_manager.py

**Key Functions:**
- `load_data()` / `save_data()`: JSON persistence
- `create_backup()`: Automatic timestamped backups
- `export_all_data()`: Full export for migration
- `validate_data_integrity()`: Check data health

---

## Data Storage

### Local JSON Files

All data stored in: `~/.claude/skills/digital-life-assistant/data/`

**Files:**
- `tasks.json`: All tasks
- `habits.json`: Habit definitions and logs
- `progress.json`: Goals, milestones, reflections
- `schedule.json`: Calendar events
- `reminders.json`: Active and completed reminders

### Automatic Backups

- Created before every save operation
- Timestamped format: `tasks_20251230_153045.json`
- Last 30 backups retained automatically
- Located in: `data/backups/`

### Data Schemas

**Task:**
```json
{
  "id": "uuid",
  "title": "Task title",
  "priority": "high|medium|low",
  "status": "pending|in-progress|completed",
  "due_date": "2025-12-30",
  "category": "work",
  "tags": ["urgent"],
  "created_at": "ISO timestamp",
  "completed_at": "ISO timestamp or null"
}
```

**Habit:**
```json
{
  "id": "uuid",
  "name": "Meditation",
  "category": "wellness",
  "target_frequency": "daily",
  "current_streak": 14,
  "longest_streak": 21,
  "logs": [
    {
      "date": "2025-12-30",
      "completed": true,
      "notes": "10 minutes morning"
    }
  ]
}
```

---

## Optional API Configuration

### Setup Config File

1. Copy template:
```bash
cp config.example.json config.json
```

2. Add to `.gitignore`:
```bash
echo "config.json" >> .gitignore
```

3. Edit `config.json` with your API credentials

### Google Calendar Integration

**Requirements:**
- Google Cloud Project with Calendar API enabled
- OAuth 2.0 credentials
- `google-api-python-client` library

**Config:**
```json
{
  "google_calendar": {
    "enabled": true,
    "credentials_path": "/path/to/credentials.json",
    "token_path": "/path/to/token.json",
    "calendar_id": "primary"
  }
}
```

**Setup Guide:** https://developers.google.com/calendar/api/quickstart/python

### Notion Integration

**Requirements:**
- Notion integration token
- Notion database ID

**Config:**
```json
{
  "notion": {
    "enabled": true,
    "api_token": "secret_xyz123...",
    "database_id": "abc123..."
  }
}
```

**Setup Guide:** https://developers.notion.com/docs/getting-started

### Todoist Integration

**Requirements:**
- Todoist API token

**Config:**
```json
{
  "todoist": {
    "enabled": true,
    "api_token": "your_token_here"
  }
}
```

**Setup Guide:** https://todoist.com/prefs/integrations

**Note:** All API integrations are **completely optional**. The skill works fully with local storage only.

---

## Example Workflows

### Morning Routine
```
1. "Good morning! What's on my plate today?"
2. Review tasks, calendar, habits
3. "Show high-priority tasks in Eisenhower Matrix"
4. Log morning habits: "Log meditation and exercise"
```

### Weekly Planning
```
1. "Generate my weekly progress review"
2. Review completed tasks and milestones
3. "What goals am I behind on?"
4. "Show upcoming calendar for next week"
5. "Create time block for deep work, 3 hours, Wednesday"
```

### Goal Tracking
```
1. "How's my progress on fitness goal?"
2. Review milestones and timeline
3. "Add reflection: [your thoughts]"
4. "What's my next milestone?"
```

---

## Troubleshooting

### Skill Not Loading

**Check installation:**
```bash
ls -la ~/.claude/skills/digital-life-assistant/
```

**Verify SKILL.md has proper YAML:**
```bash
head -n 5 ~/.claude/skills/digital-life-assistant/SKILL.md
```

Should show:
```yaml
---
name: digital-life-assistant
description: Personal life management system...
---
```

### Data Not Persisting

**Check data directory:**
```bash
ls -la ~/.claude/skills/digital-life-assistant/data/
```

**Validate data integrity:**
```
Hey Claude, validate my digital life assistant data integrity
```

### Restore from Backup

```
Hey Claude, restore my tasks from the most recent backup
```

Or specify timestamp:
```
Restore tasks from backup 20251230_100000
```

---

## Privacy & Security

### Local-First Design
- All data stored on your machine
- No cloud services by default
- Full control over your data

### API Integrations (Optional)
- Explicitly opt-in only
- Credentials stored in `config.json` (excluded from git)
- Rate limits apply (free tiers)

### Best Practices
1. Add `config.json` to `.gitignore`
2. Back up data directory regularly
3. Review API permissions before enabling
4. Use strong tokens/passwords

---

## Contributing

This skill is part of the Claude Skills Factory. Improvements welcome!

### Report Issues
- Data integrity problems
- Feature requests
- Bug reports

### Extend Functionality
- Add new habit categories
- Custom productivity metrics
- Additional API integrations

---

## License

MIT License - See LICENSE file for details

---

## Support

For questions or issues:
1. Check HOW_TO_USE.md for examples
2. Ask Claude: "How do I [task] with digital life assistant?"
3. Review troubleshooting section above

---

## Version History

### v1.0.0 (2025-12-30)
- Initial release
- Task management with Eisenhower Matrix
- Habit tracking with streak counting
- Personal growth and goal tracking
- Schedule organization and conflict detection
- Reminder system with recurring patterns
- Local JSON data persistence
- Optional API integration hooks (Google Calendar, Notion, Todoist)
- Automatic backup system
- Data validation and integrity checks

---

**Built with Claude Code Skills Factory**
**Powered by Claude Code**
