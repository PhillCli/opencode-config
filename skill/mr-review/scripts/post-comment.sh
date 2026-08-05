#!/usr/bin/env bash
# post-comment.sh — Post a review comment on an MR.
#
# With glab:  positioned inline diff comments (file + line)
# Without glab: prints the comment for the caller to post via the GitLab API
#
# Usage:
#   post-comment.sh [--mr <IID>] --message <text>
#   post-comment.sh [--mr <IID>] --file <path> --line <N[:M]> --message <text>
#   post-comment.sh [--mr <IID>] --file <path> --old-line <N> --message <text>
#   post-comment.sh [--mr <IID>] --reply <discussion-id> --message <text>
#
set -euo pipefail

MR_IID=""
FILE=""
LINE=""
OLD_LINE=""
REPLY_ID=""
MESSAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mr) [[ $# -ge 2 ]] || { echo "error: --mr requires a value" >&2; exit 2; }; MR_IID="$2"; shift 2 ;;
    --file) [[ $# -ge 2 ]] || { echo "error: --file requires a value" >&2; exit 2; }; FILE="$2"; shift 2 ;;
    --line) [[ $# -ge 2 ]] || { echo "error: --line requires a value" >&2; exit 2; }; LINE="$2"; shift 2 ;;
    --old-line) [[ $# -ge 2 ]] || { echo "error: --old-line requires a value" >&2; exit 2; }; OLD_LINE="$2"; shift 2 ;;
    --reply) [[ $# -ge 2 ]] || { echo "error: --reply requires a value" >&2; exit 2; }; REPLY_ID="$2"; shift 2 ;;
    --message) [[ $# -ge 2 ]] || { echo "error: --message requires a value" >&2; exit 2; }; MESSAGE="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [ -z "$MESSAGE" ]; then
  echo "error: --message is required" >&2
  exit 1
fi

FULL_MESSAGE="$MESSAGE"

# ── Validate flag combinations ────────────────────────────────────────
if [ -n "$LINE" ] && [ -n "$OLD_LINE" ]; then
  echo "error: --line and --old-line cannot be used together" >&2
  exit 1
fi

if { [ -n "$LINE" ] || [ -n "$OLD_LINE" ]; } && [ -z "$FILE" ]; then
  echo "error: --line/--old-line require --file" >&2
  exit 1
fi

if [ -n "$REPLY_ID" ] && [ -n "$FILE" ]; then
  echo "error: --reply and --file are mutually exclusive" >&2
  exit 1
fi

# ── Check for glab ────────────────────────────────────────────────────
HAS_GLAB=false
if command -v glab >/dev/null 2>&1; then
  HAS_GLAB=true
fi

if [ "$HAS_GLAB" = true ]; then
  # ── Post with glab ──────────────────────────────────────────────────
  ARGS=()
  if [ -n "$MR_IID" ]; then
    ARGS+=("$MR_IID")
  fi

  if [ -n "$REPLY_ID" ]; then
    ARGS+=(--reply "$REPLY_ID")
  elif [ -n "$FILE" ]; then
    ARGS+=(--file "$FILE")
    if [ -n "$LINE" ]; then
      ARGS+=(--line "$LINE")
    elif [ -n "$OLD_LINE" ]; then
      ARGS+=(--old-line "$OLD_LINE")
    fi
  fi

  if printf '%s\n' "$FULL_MESSAGE" | glab mr note create "${ARGS[@]}" >&2; then
    echo "posted: true"
  else
    echo "posted: false"
    echo "reason: glab mr note create failed"
    exit 1
  fi
else
  # ── No glab — output for manual posting ──────────────────────────
  echo "posted: false"
  echo "reason: glab not available"
  echo "action: post manually via GitLab API or configure a GitLab MCP server"
  echo ""
  echo "=== COMMENT_PAYLOAD ==="

  if [ -n "$FILE" ]; then
    echo "type: diff"
    echo "file: $FILE"
    if [ -n "$LINE" ]; then
      echo "line: $LINE (new side)"
    elif [ -n "$OLD_LINE" ]; then
      echo "old_line: $OLD_LINE (old side)"
    fi
  elif [ -n "$REPLY_ID" ]; then
    echo "type: reply"
    echo "discussion_id: $REPLY_ID"
  else
    echo "type: general"
  fi

  echo ""
  echo "=== MESSAGE ==="
  printf '%s\n' "$FULL_MESSAGE"
fi
