# Extract Book Workflow

Automated book extraction using Fabric patterns with automatic formatting and saving to history/extractions. USE WHEN user says "extract book ideas", "extract book recommendations", "save book extraction", or requests Fabric pattern extraction for books.

## 🎯 Load Full PAI Context

**Before starting any task with this skill, load complete PAI context:**

`read ${PAI_DIR}/skills/CORE/SKILL.md`

## Workflow Overview

This workflow:
1. Identifies the appropriate Fabric pattern for book extraction
2. Applies the pattern natively (using Claude's full context, not CLI)
3. Formats the results into a structured markdown file
4. Saves to `${PAI_DIR}/history/extractions/YYYY-MM/` with proper naming
5. Notifies observability system of the extraction

## Available Book Extraction Patterns

| Pattern | Use Case | Output Format |
|---------|----------|---------------|
| `extract_book_ideas` | Extract 50-100 key ideas from a book | Bulleted IDEAS list |
| `extract_book_recommendations` | Extract actionable recommendations | Bulleted RECOMMENDATIONS list |
| `extract_wisdom` | General wisdom extraction | IDEAS, INSIGHTS, QUOTES, HABITS, FACTS, REFERENCES |
| `summarize` | General book summary | Structured summary |

**Default:** Use `extract_book_ideas` unless user specifically requests recommendations or wisdom.

## Execution Steps

### Step 1: Gather Book Information

Ask user or search for:
- Book title
- Author name
- Publication year (if available)

If user provides just a book title, use WebSearch to find author and basic info.

### Step 2: Read the Appropriate Pattern

```bash
# For book ideas (default)
read ${PAI_DIR}/skills/Fabric/tools/patterns/extract_book_ideas/system.md

# For recommendations
read ${PAI_DIR}/skills/Fabric/tools/patterns/extract_book_recommendations/system.md

# For comprehensive wisdom
read ${PAI_DIR}/skills/Fabric/tools/patterns/extract_wisdom/system.md
```

### Step 3: Apply Pattern Natively

**DO NOT spawn fabric CLI.** Apply the pattern instructions directly to your knowledge of the book.

The pattern instructions contain the exact format requirements. Follow them precisely.

### Step 4: Format Output for History

Use this template structure:

```markdown
# [Book Title] - [Pattern Type]

**Author:** [Author Name]
**Extracted by:** Agent ${DA}
**Date:** [YYYY-MM-DD]
**Pattern Used:** Fabric `[pattern_name]`

**Core Thesis:** [One-line summary of main argument]

---

## [MAIN SECTION - IDEAS/RECOMMENDATIONS/etc]:

[Pattern output here - bulleted list]

---

## Sources

- [Source 1](URL)
- [Source 2](URL)
- [etc.]

---

## Book Overview

**Published:** [Year/Date]
**Core Philosophy:** [Brief description]

**Structure:**
- Part/Chapter overview

**Unique Value:** [What makes this book special]

**Who Should Read:**
- Target audience points

---

## Key Philosophical Concepts

[Main concepts from the book]

---

## Practical Tools Provided

[If applicable - exercises, frameworks, etc.]

---

## Notable Quotes

[If extracted - key quotes from the book]

---

## Related Content

[Related books, author's other work, etc.]
```

### Step 5: Generate Filename

Create kebab-case filename from book title:
- Remove articles: "the", "a", "an"
- Replace spaces with hyphens
- Lowercase
- Add pattern suffix

**Examples:**
- "The Almanack of Naval Ravikant" + `extract_book_ideas` → `almanack-naval-ravikant-ideas.md`
- "So Good They Can't Ignore You" + `extract_book_ideas` → `so-good-cant-ignore-you-ideas.md`
- "Zen and the Art of Making a Living" + `extract_book_recommendations` → `zen-art-making-living-recommendations.md`

### Step 6: Save to History Directory

```bash
# Create directory if needed
YEAR_MONTH=$(date +%Y-%m)
EXTRACTION_DIR="${PAI_DIR}/history/extractions/${YEAR_MONTH}"
mkdir -p "${EXTRACTION_DIR}"

# Write file
write ${EXTRACTION_DIR}/[filename].md
```

### Step 7: Notify Observability System

```bash
${PAI_DIR}/tools/skill-workflow-notification ExtractBook Fabric
```

### Step 8: Confirm to User

Provide user with:
- Confirmation that extraction is complete
- File location (as clickable link)
- Brief stats (number of ideas/recommendations extracted)

## Usage Examples

**Example 1: Extract book ideas**
```
User: "Extract book ideas for The Almanack of Naval Ravikant"
→ WebSearch for book information
→ Read extract_book_ideas pattern
→ Apply pattern to Naval's book
→ Format with metadata and sources
→ Save to history/extractions/2025-12/almanack-naval-ravikant-ideas.md
→ Notify observability
→ Confirm to user with file link
```

**Example 2: Extract recommendations from book**
```
User: "Extract recommendations from Zen and the Art of Making a Living"
→ Identify pattern: extract_book_recommendations
→ Read pattern
→ Apply to book content
→ Format and save to history/extractions/2025-12/zen-art-making-living-recommendations.md
→ Confirm with user
```

**Example 3: Shorthand request**
```
User: "Extract So Good They Can't Ignore You by Cal Newport"
→ Assume extract_book_ideas (default)
→ Search for book info
→ Apply pattern
→ Save to history/extractions/2025-12/so-good-cant-ignore-you-ideas.md
→ Provide clickable link to user
```

## Pattern Application Notes

**Native Execution:**
- Read pattern system.md to understand exact requirements
- Apply instructions directly using your knowledge of the book
- DO NOT spawn `fabric -p pattern_name` CLI
- This gives you full conversation context and your model's power

**Quality Standards:**
- Follow pattern's exact output format (bullet points, word limits, etc.)
- Extract the specified number of items (50-100 for ideas, etc.)
- Order by most interesting/surprising/insightful first
- Vary wording, avoid repetition
- No warnings or notes, just the requested sections

**When You Don't Know the Book:**
- Use WebSearch to find summaries, key ideas, reviews
- Use WebFetch on book websites, PDF summaries, or Blinkist
- Be honest if content is limited: extract what's available
- Cite all sources in the Sources section

## File Naming Convention

**Format:** `[book-title-kebab-case]-[pattern-suffix].md`

**Pattern Suffixes:**
- `extract_book_ideas` → `-ideas`
- `extract_book_recommendations` → `-recommendations`
- `extract_wisdom` → `-wisdom`
- `summarize` → `-summary`

**Filename Rules:**
- Remove leading articles: "the", "a", "an"
- Lowercase everything
- Replace spaces/punctuation with hyphens
- Remove possessives: "can't" → "cant", "you're" → "youre"
- Keep numbers: "48" stays as "48"

**Examples:**
| Book Title | Pattern | Filename |
|------------|---------|----------|
| The 48 Laws of Power | ideas | `48-laws-power-ideas.md` |
| How to Win Friends and Influence People | recommendations | `how-win-friends-influence-people-recommendations.md` |
| Deep Work | wisdom | `deep-work-wisdom.md` |

## Error Handling

**If book is unknown:**
1. Search for book information
2. If no reliable sources found, inform user
3. Offer to extract from user-provided content instead

**If pattern doesn't exist:**
1. List available patterns
2. Suggest closest match
3. Default to `extract_book_ideas` if uncertain

**If directory doesn't exist:**
1. Create full path: `mkdir -p ${PAI_DIR}/history/extractions/YYYY-MM`
2. Verify creation
3. Proceed with write

## Integration with Other Skills

**Research Skill:**
- Can use Research skill to gather book information
- Combine WebSearch + WebFetch for comprehensive content

**StoryExplanation Skill:**
- After extraction, can create story-format summary
- Combine extracted ideas into narrative

**Observability:**
- All extractions logged via skill-workflow-notification
- Visible in observability dashboard

## Performance Optimization

**Parallel Operations:**
- WebSearch for book info
- Read pattern file
- Execute simultaneously when possible

**Avoid:**
- Multiple sequential web searches
- Re-reading same pattern multiple times
- Spawning external CLI processes

## Expected Output Quality

**Good Extraction:**
✓ 50-100 items (for ideas pattern)
✓ Ordered by insight/interest
✓ Varied wording
✓ Concise (under 20 words per item)
✓ No repetition
✓ Complete metadata
✓ Working source links

**Poor Extraction:**
✗ Only 10-20 items
✗ Random order
✗ Repetitive phrasing
✗ Overly verbose items
✗ Missing metadata
✗ Broken or missing sources

## Success Criteria

Workflow is successful when:
1. ✓ Pattern correctly applied
2. ✓ File saved to correct location
3. ✓ Filename follows convention
4. ✓ Markdown properly formatted
5. ✓ Sources included and working
6. ✓ User receives confirmation with clickable link
7. ✓ Observability notified

## Future Enhancements

**Potential additions:**
- Multiple pattern extraction in one command
- Comparison extractions (extract from 2+ books, compare)
- Cross-reference with existing extractions
- Auto-tagging for content discovery
- Integration with Obsidian/note-taking systems
