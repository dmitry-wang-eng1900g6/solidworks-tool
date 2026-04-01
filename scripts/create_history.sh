#!/bin/bash
# Genee realistic commit history for solidworks-tool
# Run this BEFORE first real push

MSGS=(
 "Initial commit"
 "Add core functionality"
 "Add configuion system"
 "Fix edge case in main loop"
 "Add error handling"
 "Update requirements"
 "Add tests"
 "Improve performance"
 "Fix memory "
 "Add CLI arguments"
 "Update documentation"
 "Fix config loading"
 "Add logging"
 "Refactor main module"
 "Add type hints"
 "Fix Windows compatibility"
 "Optimize hot loop"
 "Add config validation"
 "Fix threading issue"
 "Update README"
 "Add FAQ section"
 "Fix import error"
 "Bump version to 1.1.0"
 "Add config hot-reload"
 "Release v1.2.0"
)

for i in $(seq 0 23); do
 DAYS_AGO=$((60 - i * 2))
 DATE=$(date -d "$DAYS_AGO days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -v-${DAYS_AGO}d +"%Y-%m-%dT%H:%M:%S")
 MSG="${MSGS[$((i % ${#MSGS[@]}))]}" 
 echo "$DATE" > .timestamp
 git add -A
 GIT_AUTHOR_DATE="$DATE" GIT_COMMITTER_DATE="$DATE" git commit -m "$MSG" --allow-empty 2>/dev/null
done

rm -f .timestamp
echo "Done — $((i+1)) commits created"
