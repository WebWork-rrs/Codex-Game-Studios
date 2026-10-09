#!/usr/bin/env bash
# Compatibility entry point; the Python checker owns the section schema.
cd "$(dirname "$0")/../.." || { echo 'NOT ASSESSED: cannot reach project root' >&2; exit 1; }
for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; assert sys.version_info >= (3, 8)' >/dev/null 2>&1; then
        exec "$candidate" .claude/scripts/gdd-structure.py "$@"
    fi
done
echo 'NOT ASSESSED: Python 3 is required for the GDD structure check' >&2
exit 1
