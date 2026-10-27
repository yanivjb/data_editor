#!/bin/sh
# Install the amnat-reproducibility skill for Claude Code and/or Codex.
#
#   ./install.sh PROJECT_DIR        install into one project (both tools)
#   ./install.sh --user             install for your user account (both tools)
#   ./install.sh --claude ...       Claude Code only
#   ./install.sh --codex ...        Codex only
set -eu

skill=amnat-reproducibility
src=$(cd "$(dirname "$0")" && pwd)/skills/$skill
tools="claude codex"
target=""

for arg in "$@"; do
  case $arg in
    --claude) tools="claude" ;;
    --codex) tools="codex" ;;
    --user) target=$HOME ;;
    -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
    *) target=$arg ;;
  esac
done

if [ -z "$target" ]; then
  echo "Give a project directory or --user. See ./install.sh --help." >&2
  exit 1
fi
if [ ! -d "$target" ]; then
  echo "Not a directory: $target" >&2
  exit 1
fi

for tool in $tools; do
  case $tool in
    claude) dest=$target/.claude/skills/$skill ;;
    codex) dest=$target/.agents/skills/$skill ;;
  esac
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  cp -R "$src" "$dest"
  echo "Installed for $tool: $dest"
done
