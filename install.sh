#!/usr/bin/env sh
# Usage: install.sh link [project-root]   — symlink the conventional locations to methodology/ (relative links)
#        install.sh copy [project-root]   — copy files instead (no dependency on methodology/)
set -eu
MODE=${1:-}; ROOT=${2:-$(cd "$(dirname "$0")/.." && pwd)}
SRC=$(cd "$(dirname "$0")" && pwd)
[ "$MODE" = link ] || [ "$MODE" = copy ] || { echo "usage: $0 link|copy [project-root]" >&2; exit 2; }
cd "$ROOT"
mkdir -p .agents .claude .kiro/settings

place() { # $1 = target path in project, $2 = relative link, $3 = source path
  rm -rf "$1"
  if [ "$MODE" = link ]; then ln -s "$2" "$1"; else cp -R "$3" "$1"; fi
}

# --- AGENTS.md: the project keeps owning this file. We only prepend/refresh a
# managed pointer block at the top; everything else in the file is preserved.
# Not a symlink: a tool that overwrites AGENTS.md in place (no unlink, just
# write) would otherwise write through the symlink and corrupt the source.
POINTER_BEGIN='<!-- methodology:begin -->'
POINTER_END='<!-- methodology:end -->'
pointer_block() {
  printf '%s\n' \
    "$POINTER_BEGIN" \
    'Full methodology: `methodology/AGENTS.md` — read it before doing anything here.' \
    "$POINTER_END"
}
rest_without_pointer() { # $1 = file; strips a prior pointer block (and the blank line after it) wherever it sits
  [ -f "$1" ] || return 0
  awk -v b="$POINTER_BEGIN" -v e="$POINTER_END" '
    $0==b {skip=1; next}
    $0==e {skip=0; afterEnd=1; next}
    afterEnd && $0=="" {afterEnd=0; next}
    {afterEnd=0}
    !skip {print}
  ' "$1"
}
write_agents_md() {
  rest=$(rest_without_pointer AGENTS.md)
  {
    pointer_block
    [ -n "$rest" ] && printf '\n%s\n' "$rest"
  } > AGENTS.md.new
  mv AGENTS.md.new AGENTS.md
}
write_agents_md

# --- skills: place each methodology skill individually so a project's own
# skills sitting alongside kiro-* ones (or a different set entirely) are
# left untouched instead of being hidden behind one whole-directory symlink.
place_skills() { # $1 = target skills dir (.agents/skills or .claude/skills)
  dest=$1
  # migrate off a prior whole-directory symlink (or any non-directory) first —
  # otherwise mkdir -p is a no-op and placing individual skills through it
  # would reach into methodology/skills/ itself via the old symlink.
  [ -d "$dest" ] && [ ! -L "$dest" ] || rm -f "$dest"
  mkdir -p "$dest"
  for skill_dir in "$SRC"/skills/*/; do
    name=$(basename "$skill_dir")
    place "$dest/$name" "../../methodology/skills/$name" "$skill_dir"
  done
}
place_skills .agents/skills
place_skills .claude/skills

place .kiro/settings/templates ../../methodology/templates "$SRC/templates"
echo "installed ($MODE) into $ROOT"
