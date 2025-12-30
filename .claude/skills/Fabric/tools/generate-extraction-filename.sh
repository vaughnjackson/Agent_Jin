#!/usr/bin/env bash
#
# generate-extraction-filename.sh
# Generates kebab-case filename for book extraction files
#
# Usage: generate-extraction-filename.sh "Book Title" "pattern-suffix"
# Example: generate-extraction-filename.sh "The Almanack of Naval Ravikant" "ideas"
# Output: almanack-naval-ravikant-ideas.md

set -euo pipefail

# Check arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 \"Book Title\" \"pattern-suffix\"" >&2
    echo "Example: $0 \"The 48 Laws of Power\" \"ideas\"" >&2
    exit 1
fi

BOOK_TITLE="$1"
PATTERN_SUFFIX="$2"

# Convert to kebab-case
# 1. Lowercase everything
# 2. Remove leading articles (the, a, an)
# 3. Replace apostrophes and possessives
# 4. Replace spaces and non-alphanumeric with hyphens
# 5. Remove common words (of, and, to, for, in, on, at, by)
# 6. Remove multiple consecutive hyphens
# 7. Remove leading/trailing hyphens

filename=$(echo "$BOOK_TITLE" | \
    tr '[:upper:]' '[:lower:]' | \
    sed -E 's/^(the|a|an) +//i' | \
    sed -E "s/'(s|re|ve|d|ll|t)//g" | \
    sed -E "s/[^a-z0-9]+/-/g" | \
    sed -E 's/-(of|and|to|for|in|on|at|by|or)-/-/g' | \
    sed -E 's/-+/-/g' | \
    sed -E 's/^-+|-+$//g')

# Append pattern suffix
filename="${filename}-${PATTERN_SUFFIX}.md"

echo "$filename"
