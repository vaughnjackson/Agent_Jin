# How to Use the Digital Life Assistant Skill

Hey Claude, I just added the "digital-life-assistant" skill. Can you help me get organized with my tasks, habits, and goals?

## Quick Start Examples

### Example 1: Morning Routine Check
```
Good morning! What's on my plate today?
```

**What you'll get:**
- List of tasks prioritized by importance and urgency
- Today's calendar events
- Habits to log
- Active reminders
- Motivational insights on your streaks

---

### Example 2: Add a Task
```
Add a task: Finish quarterly report by Friday, high priority, work category
```

**What you'll get:**
- Confirmation of task creation
- Task details with unique ID
- Suggestions for scheduling
- Conflict warnings if applicable

---

### Example 3: Log a Habit
```
Log my workout - 45 minutes strength training
```

**What you'll get:**
- Confirmation of habit logged
- Updated streak count
- Progress toward milestones
- Motivational message

---

### Example 4: Check Progress on a Goal
```
How's my progress on my fitness goal?
```

**What you'll get:**
- Overall progress percentage
- Completed vs. pending milestones
- Timeline analysis (on track / behind / ahead)
- Recent reflections
- Suggestions for next steps

---

### Example 5: Set a Reminder
```
Set a reminder to call mom next Tuesday at 2pm
```

**What you'll get:**
- Confirmation of reminder creation
- Reminder details
- Options for recurring patterns
- Context suggestions

---

## What to Provide

### For Task Management
- Task title and description
- Priority level (low, medium, high, urgent)
- Due date (flexible format: "Friday", "Jan 15", "2025-01-15")
- Category (work, personal, health, learning, etc.)
- Optional tags

### For Habit Tracking
- Habit name
- Category (wellness, fitness, productivity, learning, etc.)
- Frequency (daily, weekly, custom)
- Optional numerical value (e.g., "30 minutes")

### For Goal Setting
- Goal title and description
- Category (fitness, career, learning, financial, etc.)
- Target date
- Milestones (optional)

### For Calendar Events
- Event title
- Start and end time
- Event type (meeting, appointment, block, etc.)
- Optional: location, attendees

### For Reminders
- What to be reminded about
- When (date and time)
- Priority level
- Optional: recurring pattern

---

## What You'll Get

### Daily Summary
- Prioritized task list (Eisenhower Matrix)
- Today's calendar events
- Habit checklist
- Active reminders
- Progress updates

### Analytics & Insights
- Productivity statistics
- Habit streak trends
- Goal progress tracking
- Time management analysis
- Personalized recommendations

### Motivational Support
- Streak milestone celebrations
- Progress encouragement
- Weekly review summaries
- Reflection prompts

---

## Advanced Usage

### Eisenhower Matrix Prioritization
```
Show my tasks using the Eisenhower Matrix
```

**Categories:**
- **Do First**: Urgent & Important
- **Schedule**: Not Urgent but Important
- **Delegate**: Urgent but Not Important
- **Eliminate**: Not Urgent & Not Important

---

### Weekly Review
```
Generate my weekly progress review
```

**Includes:**
- Completed tasks and milestones
- Habit consistency analysis
- Goal progress updates
- Upcoming priorities
- Reflection prompts

---

### Conflict Detection
```
Find scheduling conflicts in my calendar for next week
```

**Shows:**
- Overlapping events
- Double-booked time slots
- Suggestions for resolution

---

### Habit Streaks & Milestones
```
What are my current habit streaks?
```

**Displays:**
- Current streak for each habit
- Longest streak achieved
- Days until next milestone
- Motivational insights

---

### Export Data
```
Export all my data for backup
```

**Creates:**
- Timestamped export folder
- All data in JSON format
- Config file (sanitized, no API tokens)
- Ready for import on another system

---

## Natural Language Flexibility

The skill understands various ways of asking:

**Tasks:**
- "Add task: [description]"
- "Create a new task for [description]"
- "I need to [description] by [date]"

**Habits:**
- "Log [habit name]"
- "I did [habit name] today"
- "Mark [habit name] as complete"

**Goals:**
- "Create a goal to [description]"
- "I want to [description] by [date]"
- "Track my progress on [goal]"

**Reminders:**
- "Remind me to [action] on [date/time]"
- "Set a reminder for [action]"
- "Don't let me forget to [action]"

---

## Tips for Best Results

### 1. Be Specific
- **Good**: "Finish quarterly financial report by Friday 5pm, high priority"
- **Less Good**: "Do report"

### 2. Use Categories Consistently
- Pick categories that match your life (work, personal, health, etc.)
- Stick to the same categories for better analytics

### 3. Review Daily
- Start each day with: "What's on my plate today?"
- End each day with: "Show completed tasks and habit logs"

### 4. Reflect Weekly
- Every Sunday (or your preferred day): "Generate my weekly review"
- Use reflection prompts to track personal growth

### 5. Track Consistently
- Log habits daily (even if you miss one)
- Update task status as you progress
- Add reflections to your goals regularly

---

## Installation Check

To verify the skill is installed correctly:

```
Hey Claude, show me my task management capabilities
```

If installed, Claude will describe the Digital Life Assistant features and offer to help you get started.

---

## Privacy & Data

- **All data stored locally** in `~/.claude/skills/digital-life-assistant/data/`
- **No external services** unless you configure API integration
- **Automatic backups** created before each save (last 30 kept)
- **Export anytime** for backup or migration

---

## Getting Help

If you need help with specific features:

```
How do I [specific task] with the digital life assistant?
```

Examples:
- "How do I set up recurring reminders?"
- "How do I track progress on long-term goals?"
- "How do I export my data for backup?"

---

Happy organizing! Start with: **"Good morning! What's on my plate today?"**
