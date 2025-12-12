# CLAUDE.md - Quick Reference Guide

> **Purpose**: This file serves as a central navigation point for Claude to quickly understand the Agent_Jin system structure and locate critical information in new sessions.

---

## 🎯 Quick Start for New Sessions

When starting a new session, read this file first to understand:
- System architecture and key components
- Location of critical files and documentation
- Common workflows and commands
- Project-specific conventions

---

## 📁 System Overview

**Project Name**: Agent_Jin
**Framework**: PAI (Personal AI Infrastructure) v0.9.1
**Base**: Claude Code by Anthropic
**Runtime**: Bun (NOT Node.js)
**Language**: TypeScript
**Package Manager**: Bun

---

## 🗺️ Critical File Locations

### Configuration Files
- **Main Config**: `.claude/settings.json` - Identity, paths, preferences
- **Environment**: `.claude/.env` - API keys and secrets
- **MCP Config**: `.claude/.mcp.json` - MCP server configuration
- **Sessions**: `.claude/agent-sessions.json` - Active session tracking

### Core Documentation
- **System Philosophy**: `.claude/skills/CORE/CONSTITUTION.md`
- **Architecture**: `.claude/skills/CORE/Architecture.md`
- **Skill System Guide**: `.claude/skills/CORE/SkillSystem.md`
- **Main PAI Skill**: `.claude/skills/CORE/SKILL.md`
- **Hook System**: `.claude/skills/CORE/HookSystem.md`
- **History System**: `.claude/skills/CORE/HistorySystem.md`
- **Prompting Guide**: `.claude/skills/CORE/Prompting.md`

### Project Root
- **Main README**: `README.md` - Comprehensive PAI documentation
- **PAI Contract**: `PAI_CONTRACT.md` - Core system guarantees
- **Update Guide**: `PAI_SYNC_GUIDE.md` - How to update PAI
- **Security**: `SECURITY.md` - Security documentation
- **Changelog**: `CHANGELOG-2025-11-20.md` - Version history

---

## 🏗️ Directory Structure

```
Agent_Jin/
├── .claude/                      # ALL PAI configuration lives here
│   ├── skills/                   # Self-contained AI capabilities
│   │   ├── CORE/                # System docs, constitution, identity
│   │   ├── StoryExplanation/    # 24-item narrative format
│   │   ├── Art/                 # Visual content generation
│   │   ├── Research/            # Multi-source research
│   │   ├── Fabric/              # 248+ native AI patterns
│   │   ├── BrightData/          # 4-tier web scraping
│   │   ├── Observability/       # Real-time monitoring dashboard
│   │   ├── CreateCLI/           # CLI tool templates
│   │   ├── Createskill/         # Skill creation templates
│   │   ├── Prompting/           # Prompt engineering
│   │   ├── AlexHormoziPitch/    # Business pitch generation
│   │   └── Ffuf/                # Web fuzzing
│   ├── agents/                  # Specialized AI personalities
│   ├── hooks/                   # Event-driven automation
│   ├── history/                 # Automatic work documentation
│   │   ├── sessions/            # Session summaries
│   │   ├── raw-outputs/         # Raw tool outputs
│   │   └── extractions/         # Extracted knowledge
│   ├── commands/                # Slash commands
│   ├── config/                  # Additional configs
│   ├── tools/                   # Utility scripts
│   ├── Observability/           # Real-time dashboard app
│   ├── voice-server/            # TTS integration
│   ├── scratchpad/              # Current session workspace
│   └── setup.sh                 # Initial setup wizard
├── docs/                        # Documentation assets
├── .github/                     # GitHub workflows
└── [Root documentation files]
```

---

## 🎨 Skills System

### What are Skills?
Skills are **self-contained AI capabilities** with:
- Routing logic (when to activate)
- Workflows (how to execute)
- Documentation (how to use)
- Tools (supporting scripts)

### Active Skills

| Skill | Purpose | Entry Point |
|-------|---------|-------------|
| **CORE** | System identity, constitution, architecture | `.claude/skills/CORE/SKILL.md` |
| **StoryExplanation** | 24-item narrative format | `.claude/skills/StoryExplanation/` |
| **Art** | Visual content generation | `.claude/skills/Art/` |
| **Research** | Multi-source research workflows | `.claude/skills/Research/` |
| **Fabric** | 248+ AI patterns (native execution) | `.claude/skills/Fabric/` |
| **BrightData** | Progressive web scraping | `.claude/skills/BrightData/` |
| **Observability** | Real-time agent monitoring | `.claude/skills/Observability/` |
| **CreateCLI** | CLI tool generation | `.claude/skills/CreateCLI/` |
| **Createskill** | Skill creation templates | `.claude/skills/Createskill/` |
| **Prompting** | Prompt engineering patterns | `.claude/skills/Prompting/` |
| **AlexHormoziPitch** | Business pitch generation | `.claude/skills/AlexHormoziPitch/` |
| **Ffuf** | Web fuzzing integration | `.claude/skills/Ffuf/` |

---

## 🔧 System Components

### 1. Hook System
**Location**: `.claude/hooks/`
**Purpose**: Event-driven automation that captures work and manages state
**Documentation**: `.claude/skills/CORE/HookSystem.md`

Common hooks:
- Session start/end notifications
- Tool output capture
- Session summary generation
- Tab title updates

### 2. History System (UOCS)
**Location**: `.claude/history/`
**Purpose**: Automatic documentation of all work
**Documentation**: `.claude/skills/CORE/HistorySystem.md`

Structure:
- `sessions/` - Session summaries
- `raw-outputs/` - Raw tool outputs
- `extractions/` - Extracted knowledge

### 3. Agent Personalities
**Location**: `.claude/agents/`
**Purpose**: Specialized AI identities for different tasks
**Examples**: Engineer, Researcher, Designer personas

### 4. Observability Dashboard
**Location**: `.claude/Observability/`
**Purpose**: Real-time WebSocket monitoring of agent activity
**Features**: Live charts, event timelines, swim lanes, multiple themes

### 5. Voice Server
**Location**: `.claude/voice-server/`
**Purpose**: Text-to-speech feedback using ElevenLabs
**Platform**: macOS service with menubar integration

---

## 📝 The Thirteen Founding Principles

PAI is built on 13 foundational principles (see `README.md` or `.claude/skills/CORE/Architecture.md`):

1. **Clear Thinking + Prompting is King**
2. **Scaffolding > Model**
3. **As Deterministic as Possible**
4. **Code Before Prompts**
5. **Spec / Test / Evals First**
6. **UNIX Philosophy**
7. **ENG / SRE Principles**
8. **CLI as Interface**
9. **Goal → Code → CLI → Prompts → Agents**
10. **Meta / Self Update System**
11. **Custom Skill Management**
12. **Custom History System**
13. **Custom Agent Personalities / Voices**

---

## 🚀 Common Workflows

### Starting a New Session
1. Read this file (`CLAUDE.md`)
2. Check `.claude/scratchpad/` for current work
3. Review `.claude/agent-sessions.json` for active sessions
4. Load relevant skill from `.claude/skills/`

### Creating New Content
1. Check `.claude/scratchpad/` for workspace
2. Use appropriate skill (StoryExplanation, Art, Research, etc.)
3. Follow skill's workflow documentation

### Updating System
```bash
/paiupdate  # or /pa
```

### Running Skills
Skills are invoked contextually based on user requests. Each skill has:
- `SKILL.md` - Main skill documentation
- `Workflow.md` - Step-by-step execution guide
- `tools/` - Supporting scripts

---

## 🔍 Quick Search Patterns

### Find Configuration
```bash
# Main settings
cat .claude/settings.json

# Environment variables
cat .claude/.env
```

### Find Documentation
```bash
# System philosophy
cat .claude/skills/CORE/CONSTITUTION.md

# How to create skills
cat .claude/skills/CORE/SkillSystem.md
```

### Find Current Work
```bash
# Current session workspace
ls -la .claude/scratchpad/

# Recent history
ls -la .claude/history/sessions/
```

---

## 🎯 User Preferences & Identity

**Location**: `.claude/settings.json`

Key configuration:
- `DA` - Digital Assistant name (your AI's identity)
- `PAI_DIR` - Root directory path
- `TIME_ZONE` - Timezone for timestamps
- User name, email, preferences

---

## 🔐 Security & Protection

**Protected Files**: `.pai-protected.json`
**Security Docs**: `SECURITY.md`
**Contract**: `PAI_CONTRACT.md`

PAI has a protection system to prevent accidental overwrites of critical files during updates.

---

## 📊 Current Session Info

**Scratchpad Location**: `.claude/scratchpad/`
**Active Sessions**: `.claude/agent-sessions.json`
**Recent Work**: `.claude/history/sessions/`

Check these locations to understand:
- What the user was last working on
- Current session context
- Recent conversation history

---

## 🛠️ Technology Choices (Important!)

| Category | Choice | NOT This |
|----------|--------|----------|
| Runtime | Bun | ❌ Node.js |
| Language | TypeScript | ❌ Python |
| Package Manager | Bun | ❌ npm/yarn/pnpm |
| Format | Markdown | ❌ HTML (for basic content) |
| Testing | Vitest | When needed |
| Voice | ElevenLabs | TTS integration |

---

## 🎓 Learning the System

### For Understanding Architecture
1. Read `.claude/skills/CORE/CONSTITUTION.md` - Philosophy
2. Read `.claude/skills/CORE/Architecture.md` - Technical design
3. Read `README.md` - Full overview

### For Creating Skills
1. Read `.claude/skills/CORE/SkillSystem.md` - Canonical guide
2. Explore `.claude/skills/Createskill/` - Templates
3. Study existing skills as examples

### For Understanding Hooks
1. Read `.claude/skills/CORE/HookSystem.md`
2. Explore `.claude/hooks/` directory
3. Check `settings.json` for hook configuration

---

## 🔄 Update & Maintenance

**Update Command**: `/paiupdate` or `/pa`
**Update Guide**: `PAI_SYNC_GUIDE.md`
**Protection System**: Custom skills and settings are preserved
**Changelog**: `CHANGELOG-2025-11-20.md`

---

## 💡 Pro Tips

1. **Always check scratchpad first** - Shows current work context
2. **Skills are self-documenting** - Each has its own SKILL.md
3. **Use CORE skill for identity** - System personality and preferences
4. **History system tracks everything** - Check `.claude/history/` for past work
5. **Hooks run automatically** - Event-driven, no manual invocation needed
6. **Observability for monitoring** - Real-time view of agent activity
7. **TitleCase for filenames** - PAI convention throughout

---

## 📞 Getting Help

- **Issues**: GitHub issues in PAI repository
- **Discussions**: GitHub discussions
- **Video**: Full PAI walkthrough on YouTube
- **Blog**: "The Real Internet of Things" by Daniel Miessler

---

## ✅ Session Checklist

When starting a new session:

- [ ] Read this file (CLAUDE.md)
- [ ] Check `.claude/scratchpad/` for current work
- [ ] Review `.claude/settings.json` for user preferences
- [ ] Check `.claude/agent-sessions.json` for active sessions
- [ ] Load relevant skill documentation if needed
- [ ] Review `.claude/history/sessions/` for recent context

---

## 🎯 Quick File Reference

**Need to know user preferences?**
→ `.claude/settings.json`

**Need system philosophy?**
→ `.claude/skills/CORE/CONSTITUTION.md`

**Need to understand architecture?**
→ `.claude/skills/CORE/Architecture.md` or `README.md`

**Need to create a skill?**
→ `.claude/skills/CORE/SkillSystem.md`

**Need current work context?**
→ `.claude/scratchpad/` or `.claude/history/sessions/`

**Need to understand hooks?**
→ `.claude/skills/CORE/HookSystem.md`

**Need API keys?**
→ `.claude/.env` (encrypted/protected)

---

**Last Updated**: 2025-12-12
**PAI Version**: 0.9.1
**Framework**: Claude Code by Anthropic
