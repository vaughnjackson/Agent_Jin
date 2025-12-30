---
name: digital-life-assistant
description: Personal life management system tracking growth, tasks, habits, schedules, and reminders with local data persistence and optional API integration (project)
---

# Digital Life Assistant

A comprehensive AI-powered personal life management system that helps you track your personal growth, manage daily tasks, build healthy habits, organize your schedule, and never miss important follow-ups. All data is stored locally for privacy and portability, with optional integration hooks for Google Calendar, Notion, and Todoist.

## Workflow Routing

**AUTO-ACTIVATE when user says:**
- "Show my tasks", "What's on my plate", "What should I do today"
- "Log [habit]", "Track [habit]", "I just [habit]"
- "What's on my calendar", "What's my schedule"
- "How's my progress on [goal]", "Show my goals"
- "Set reminder", "Remind me to"
- "What did I accomplish", "Daily summary", "Weekly review"
- "Show habit streaks", "How's my [habit] going"

**DO NOT activate for:**
- General programming/coding tasks
- File operations unrelated to personal life data
- System configuration or setup questions

| User Intent | Trigger Phrases | Action |
|-------------|----------------|--------|
| **View Tasks** | "show tasks", "what's on my plate", "priorities" | Load and display tasks from data/tasks.json |
| **Log Habits** | "log [habit]", "track [habit]", "completed [habit]" | Update habit logs in data/habits.json |
| **Check Schedule** | "calendar", "schedule", "what's today" | Display events from data/schedule.json |
| **Goal Progress** | "progress on [goal]", "how's [goal] going" | Show goal status from data/progress.json |
| **Set Reminders** | "remind me", "set reminder" | Create reminder in data/reminders.json |
| **Daily Review** | "what did I do", "daily summary", "weekly review" | Aggregate data across all modules |

---

## Capabilities

### Personal Growth & Progress Tracking
- **Goal Setting & Tracking**: Define SMART goals and track progress over time
- **Milestone Logging**: Record achievements and celebrate wins
- **Reflection Prompts**: Guided self-reflection for continuous improvement
- **Progress Visualization**: See your growth trends and patterns
- **Weekly/Monthly Reviews**: Automated progress summaries and insights

### Task & Priority Management
- **Task Creation**: Add tasks with priorities, deadlines, and contexts
- **Smart Prioritization**: Eisenhower Matrix (Urgent/Important) and custom scoring
- **Task Categories**: Work, Personal, Health, Learning, etc.
- **Due Date Tracking**: Never miss a deadline
- **Completion Analytics**: Track productivity patterns

### Habit & Wellness Tracking
- **Habit Building**: Track daily habits with streak counting
- **Wellness Goals**: Monitor exercise, meditation, sleep, water intake, etc.
- **Streak Motivation**: Visual streak tracking and milestone alerts
- **Trend Analysis**: Identify patterns in your wellness journey
- **Custom Metrics**: Define and track any personal metric

### Schedule & Calendar Organization
- **Event Management**: Create, update, and view calendar events
- **Conflict Detection**: Automatically identify scheduling conflicts
- **Time Blocking**: Allocate focused time for important work
- **Daily/Weekly Views**: See your schedule at a glance
- **Optional Google Calendar Sync**: Two-way sync (requires API token)

### Reminders & Follow-ups
- **Smart Reminders**: Set reminders for tasks, events, and follow-ups
- **Recurring Reminders**: Daily, weekly, monthly patterns
- **Context-Based Alerts**: Location or event-triggered reminders
- **Follow-up Tracking**: Never drop the ball on important connections
- **Snooze & Reschedule**: Flexible reminder management

## Input Requirements

All interactions are conversational through Claude Code. You can:

### Natural Language Inputs
- "Add a task: Finish quarterly report by Friday, high priority"
- "Log my workout: 30 minutes running"
- "What's my meditation streak?"
- "Show my schedule for tomorrow"
- "Set a reminder to call mom next Tuesday"

### Structured Data (Optional)
For bulk imports or integrations, supports JSON format:

```json
{
  "task": {
    "title": "Complete project proposal",
    "priority": "high",
    "due_date": "2025-01-15",
    "category": "work",
    "tags": ["urgent", "client"]
  }
}
```

### Data Persistence
All data stored in local JSON files:
- `~/.claude/skills/digital-life-assistant/data/tasks.json`
- `~/.claude/skills/digital-life-assistant/data/habits.json`
- `~/.claude/skills/digital-life-assistant/data/progress.json`
- `~/.claude/skills/digital-life-assistant/data/schedule.json`
- `~/.claude/skills/digital-life-assistant/data/reminders.json`

## Output Formats

### Conversational Responses
Claude provides natural language summaries:
- "You have 5 high-priority tasks today. Top priority: Finish quarterly report (due Friday)"
- "Great job! Your meditation streak is 14 days. You're 6 days away from your 20-day milestone!"
- "You have a scheduling conflict: Team meeting (2pm-3pm) overlaps with Client call (2:30pm-3:30pm)"

### Structured Data
JSON output for integrations or exports:
```json
{
  "daily_summary": {
    "date": "2025-12-30",
    "tasks_completed": 8,
    "tasks_pending": 5,
    "habits_logged": 3,
    "habit_streaks": {
      "meditation": 14,
      "exercise": 7
    },
    "upcoming_events": 2,
    "active_reminders": 3
  }
}
```

### Visual Reports (Optional)
- Progress charts and graphs
- Habit streak calendars
- Task completion trends
- Weekly productivity reports

## How to Use

### Getting Started
```
Hey Claude, I just installed the digital-life-assistant skill. Can you help me set up my first goal and tasks?
```

### Daily Interactions
```
Show me my tasks for today prioritized by importance

Log my morning routine: 10 minutes meditation, 30 minutes exercise

What's on my calendar for this week?

Set a reminder to review quarterly goals on Friday at 2pm
```

### Progress Tracking
```
How's my progress on my fitness goal?

Show my habit streaks for this month

What did I accomplish last week?

Help me reflect on my personal growth this quarter
```

### Advanced Usage
```
Analyze my productivity patterns and suggest improvements

Find scheduling conflicts in my calendar for next week

What tasks are overdue and need immediate attention?

Export my habit data for the last 3 months
```

## Scripts

### Core Modules

- **`task_manager.py`**: Task creation, prioritization, completion tracking, and analytics
- **`habit_tracker.py`**: Habit logging, streak counting, pattern analysis, and motivation
- **`progress_tracker.py`**: Goal management, milestone tracking, reflection prompts, and progress visualization
- **`schedule_organizer.py`**: Calendar event management, conflict detection, time blocking, and optional Google Calendar sync
- **`reminder_system.py`**: Reminder creation, recurring patterns, context-based alerts, and notification management
- **`data_manager.py`**: JSON persistence layer, data validation, backup/restore, and API integration hooks

### Optional API Integration

Each module includes hooks for external API integration:
- **Google Calendar API**: Two-way sync for events (requires OAuth token)
- **Notion API**: Sync tasks and notes (requires integration token)
- **Todoist API**: Task synchronization (requires API token)

Configuration is optional and stored in `config.json` (not tracked in version control).

## Best Practices

### Daily Routine
1. **Morning**: Review tasks and priorities for the day
2. **Throughout Day**: Log habits and mark tasks complete as you go
3. **Evening**: Reflect on progress, plan tomorrow

### Weekly Reviews
1. Review completed tasks and habit streaks
2. Update goal progress
3. Check upcoming calendar events
4. Adjust priorities based on insights

### Data Management
1. Local data is automatically backed up with timestamps
2. Export important data periodically
3. Use version control for your data folder (optional)
4. Add API tokens to `config.json` only if you want external sync

### Privacy & Security
1. All data stored locally on your machine
2. No data sent to external services without explicit API configuration
3. API tokens stored in `config.json` (add to `.gitignore`)
4. Regular backups recommended

## Limitations

### Data Persistence
- **Local-only by default**: Data is not synced across devices unless you configure API integration
- **Manual backup**: You must back up data folder yourself (or use git)
- **No cloud storage**: All data is local for privacy (optional APIs can change this)

### API Integrations
- **Optional**: All APIs require manual setup (OAuth, tokens)
- **Rate limits**: Free tiers have API call limits
- **Authentication**: Google Calendar requires OAuth flow (complex setup)

### Functionality
- **No mobile app**: Access via Claude Code only (desktop/laptop)
- **No real-time alerts**: Reminders shown when you interact with Claude Code
- **No voice input**: Text-based interaction only
- **Limited visualization**: Basic charts (no advanced dashboards)

### Accuracy
- **Manual logging**: You must log habits and tasks (no automatic tracking)
- **Self-reported data**: Progress depends on honest input
- **Pattern analysis**: Insights are data-driven but require interpretation

### When NOT to Use This Skill
- If you need real-time mobile push notifications (use dedicated apps)
- If you require team collaboration features (use project management tools)
- If you want automatic time tracking (use time-tracking software)
- If you need medical-grade health tracking (consult healthcare professionals)

## Data Structure

### Task Schema
```json
{
  "id": "unique-task-id",
  "title": "Task title",
  "description": "Optional details",
  "priority": "high|medium|low",
  "status": "pending|in-progress|completed",
  "due_date": "2025-12-30",
  "category": "work|personal|health|learning",
  "tags": ["tag1", "tag2"],
  "created_at": "2025-12-30T10:00:00Z",
  "completed_at": null
}
```

### Habit Schema
```json
{
  "id": "unique-habit-id",
  "name": "Meditation",
  "category": "wellness",
  "target_frequency": "daily",
  "logs": [
    {
      "date": "2025-12-30",
      "completed": true,
      "notes": "10 minutes morning meditation"
    }
  ],
  "current_streak": 14,
  "longest_streak": 21,
  "created_at": "2025-12-01T00:00:00Z"
}
```

### Goal Schema
```json
{
  "id": "unique-goal-id",
  "title": "Run a 5K race",
  "description": "Complete a 5K race by June 2026",
  "category": "fitness",
  "target_date": "2026-06-30",
  "milestones": [
    {
      "title": "Run 1 mile without stopping",
      "completed": true,
      "completed_at": "2025-11-15"
    }
  ],
  "progress_percentage": 35,
  "status": "in-progress",
  "created_at": "2025-10-01T00:00:00Z"
}
```

## Installation

### Quick Install (Recommended)
```bash
# Copy skill to personal Claude Code skills directory
cp -r digital-life-assistant ~/.claude/skills/

# Create data directory
mkdir -p ~/.claude/skills/digital-life-assistant/data
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
```
Hey Claude, can you show me my tasks for today?
```

If the skill is loaded, Claude will respond with task management capabilities.

## Optional API Setup

### Google Calendar Integration

1. **Create Google Cloud Project**: https://console.cloud.google.com/
2. **Enable Google Calendar API**
3. **Create OAuth 2.0 credentials**
4. **Download credentials JSON**
5. **Add to config**:
```json
{
  "google_calendar": {
    "enabled": true,
    "credentials_path": "/path/to/credentials.json",
    "token_path": "/path/to/token.json"
  }
}
```

### Notion Integration

1. **Create Notion Integration**: https://www.notion.so/my-integrations
2. **Copy integration token**
3. **Add to config**:
```json
{
  "notion": {
    "enabled": true,
    "api_token": "your-notion-integration-token",
    "database_id": "your-database-id"
  }
}
```

### Todoist Integration

1. **Get Todoist API token**: https://todoist.com/prefs/integrations
2. **Add to config**:
```json
{
  "todoist": {
    "enabled": true,
    "api_token": "your-todoist-api-token"
  }
}
```

**Note**: API integrations are completely optional. The skill works fully with local storage only.

## Examples

### Example 1: Morning Routine
```
User: Good morning! What's on my plate today?

Claude: Good morning! Here's your daily overview:

Tasks (5 pending):
1. HIGH: Finish quarterly report (due Friday)
2. HIGH: Prepare presentation for client (due today, 2pm)
3. MEDIUM: Review code pull requests
4. MEDIUM: Schedule dentist appointment
5. LOW: Update team wiki

Calendar (3 events):
- 10:00am - Team standup (30 min)
- 2:00pm - Client presentation (60 min)
- 4:00pm - 1-on-1 with Sarah (30 min)

Habits to log today:
- Morning meditation (streak: 13 days)
- Exercise (streak: 6 days)
- Read 20 pages (streak: 10 days)

Reminders:
- Call mom (due today, 5pm)

You're making great progress! Keep up your meditation streak - you're 7 days away from your 20-day goal!
```

### Example 2: Habit Tracking
```
User: Log my workout - 45 minutes strength training

Claude: Excellent! I've logged your workout.

Exercise streak: 7 days
Longest streak: 12 days
This week: 5/7 days completed

You're building great consistency! 5 more days to match your personal record. Keep it up!
```

### Example 3: Progress Review
```
User: How's my progress on my fitness goal?

Claude: Your fitness goal: "Run a 5K race by June 2026"

Progress: 35% complete

Milestones achieved (2/5):
✅ Run 1 mile without stopping (Nov 15)
✅ Run 2 miles continuously (Dec 10)

Upcoming milestones:
⏳ Run 3 miles continuously (target: Jan 15)
⏳ Complete 5K training program (target: Apr 1)
⏳ Run first 5K race (target: Jun 30)

Recent habit tracking:
- Exercise: 7-day streak (excellent!)
- Healthy eating: 12-day streak (amazing!)

Insights:
You're ahead of schedule! At this pace, you'll complete your 3-mile milestone 2 weeks early. Your consistent exercise habit is paying off. Consider adding a long run once per week to build endurance.
```

## Version History

- **v1.0.0** (2025-12-30): Initial release
  - Task management with smart prioritization
  - Habit tracking with streak counting
  - Personal growth and goal tracking
  - Schedule organization and conflict detection
  - Reminder system with recurring patterns
  - Local JSON data persistence
  - Optional API integration hooks (Google Calendar, Notion, Todoist)
