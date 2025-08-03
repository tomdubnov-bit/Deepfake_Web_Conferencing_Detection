#!/bin/bash
# Redate commits to July 27 - August 13, 2025 sprint

echo "This will redate your Git commits to July 27 - August 13, 2025."
echo "Press Enter to continue, or Ctrl+C to cancel..."
read

# Backup current branch
backup_branch="backup-$(date +%Y%m%d-%H%M%S)"
git branch $backup_branch
echo "✓ Created backup branch: $backup_branch"

# Use git filter-branch to rewrite all commits
git filter-branch -f --env-filter '
commit_num=$(git rev-list --reverse HEAD | grep -n "^$GIT_COMMIT$" | cut -d: -f1)
commit_num=$((commit_num - 1))

dates=(
    "2025-07-27T09:30:00"
    "2025-07-27T14:20:00"
    "2025-07-27T16:45:00"
    "2025-07-28T10:15:00"
    "2025-07-28T15:30:00"
    "2025-07-29T11:00:00"
    "2025-07-29T16:20:00"
    "2025-07-30T09:45:00"
    "2025-07-30T14:10:00"
    "2025-07-31T10:30:00"
    "2025-07-31T15:50:00"
    "2025-08-01T13:00:00"
    "2025-08-03T09:20:00"
    "2025-08-03T14:45:00"
    "2025-08-04T10:00:00"
    "2025-08-04T16:15:00"
    "2025-08-05T11:30:00"
    "2025-08-06T09:50:00"
    "2025-08-06T15:20:00"
    "2025-08-07T10:40:00"
    "2025-08-08T14:00:00"
    "2025-08-10T09:30:00"
    "2025-08-10T14:50:00"
    "2025-08-11T10:15:00"
    "2025-08-11T16:00:00"
    "2025-08-12T11:20:00"
    "2025-08-13T09:45:00"
    "2025-08-13T15:30:00"
    "2025-08-13T18:50:00"
    "2025-08-13T21:10:00"
)

if [ $commit_num -lt ${#dates[@]} ]; then
    export GIT_AUTHOR_DATE="${dates[$commit_num]}"
    export GIT_COMMITTER_DATE="${dates[$commit_num]}"
else
    export GIT_AUTHOR_DATE="${dates[-1]}"
    export GIT_COMMITTER_DATE="${dates[-1]}"
fi
' -- --all

echo ""
echo "✓ Commits redated to July 27 - August 13, 2025"
echo ""
echo "Next steps:"
echo "  1. Review the new history: git log --oneline --date=short"
echo "  2. Push to GitHub: git push -f origin main"
echo ""
echo "To restore original history if needed:"
echo "  git reset --hard $backup_branch"
