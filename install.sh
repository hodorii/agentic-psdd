#!/usr/bin/env sh
# Usage: install.sh link [project-root] [--force] - symlink the conventional locations to methodology/ (relative links)
#        install.sh copy [project-root] [--force] - copy files instead (no dependency on methodology/)
# --force: overwrite files a previous copy install placed and the project has since edited by hand
set -eu
MODE=${1:-}; FORCE=0; ROOT=
[ $# -gt 0 ] && shift
for arg in "$@"; do
  case $arg in
    --force) FORCE=1 ;;
    *) ROOT=$arg ;;
  esac
done
[ -n "$ROOT" ] || ROOT=$(cd "$(dirname "$0")/.." && pwd)
SRC=$(cd "$(dirname "$0")" && pwd -P)
[ "$MODE" = link ] || [ "$MODE" = copy ] || { echo "usage: $0 link|copy [project-root] [--force]" >&2; exit 2; }

# link mode hardcodes symlink targets as '../../methodology/...', so it only
# works when '$ROOT/methodology' physically resolves to this same repo (a
# submodule/subtree/symlink named 'methodology' at the project root). Catch a
# mismatch here - before touching anything in the project - instead of
# silently laying down dangling symlinks.
if [ "$MODE" = link ]; then
  target=$(cd "$ROOT/methodology" 2>/dev/null && pwd -P) || target=
  if [ "$target" != "$SRC" ]; then
    cat >&2 <<EOF
error: link mode requires '$ROOT/methodology' to resolve to this methodology repo ($SRC), but it $([ -z "$target" ] && echo "doesn't exist" || echo "resolves to '$target' instead").
Add/point it there first, e.g.:
  git submodule add <url> methodology && methodology/install.sh link
or use 'install.sh copy $ROOT' instead, which has no such dependency.
EOF
    exit 2
  fi
fi

cd "$ROOT"
mkdir -p .agents .claude .kiro/settings

# --- hand-edit protection: a copy install records the SHA-256 of every file it
# placed. Before a later run (link or copy) replaces those files, any file whose
# current hash differs from the recorded one is a project edit - the run stops
# and lists them instead of silently discarding the work. --force overrides.
FILES_MANIFEST=.kiro/settings/.methodology-files-manifest
hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  else shasum -a 256 "$1" | cut -d' ' -f1; fi
}
modified_placed_files() { # prints each recorded file that still exists with a different hash
  [ -f "$FILES_MANIFEST" ] || return 0
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    recorded=${line%% *}; path=${line#* }
    [ -f "$path" ] && [ ! -L "$path" ] || continue
    [ "$(hash_file "$path")" = "$recorded" ] || printf '%s\n' "$path"
  done < "$FILES_MANIFEST"
}
modified=$(modified_placed_files)
if [ -n "$modified" ] && [ "$FORCE" != 1 ]; then
  {
    echo "error: these files were placed by a previous copy install and edited in the project since; this run would overwrite them:"
    printf '%s\n' "$modified" | sed 's/^/  /'
    echo "Move the edits into .kiro/steering or a project-owned skill, or re-run with --force to discard them."
  } >&2
  exit 3
fi
write_files_manifest() { # $@ = placed directories; copy mode only
  : > "$FILES_MANIFEST"
  for dir in "$@"; do
    [ -d "$dir" ] && [ ! -L "$dir" ] || continue
    find "$dir" -type f | LC_ALL=C sort | while IFS= read -r f; do
      printf '%s %s\n' "$(hash_file "$f")" "$f"
    done >> "$FILES_MANIFEST"
  done
}

place() { # $1 = target path in project, $2 = relative link, $3 = source path
  rm -rf "$1"
  if [ "$MODE" = link ]; then ln -s "$2" "$1"; else cp -R "$3" "$1"; fi
}

# --- AGENTS.md: the project keeps owning this file. We only prepend/refresh a
# managed pointer block at the top; everything else in the file is preserved.
# Not a symlink: a tool that overwrites AGENTS.md in place (no unlink, just
# write) would otherwise write through the symlink and corrupt the source.
# Router the pointer names: the submodule in link mode; a copy under
# .kiro/settings in copy mode (copy installs have no methodology/ directory).
if [ "$MODE" = link ]; then ROUTER=methodology/AGENTS.md; else ROUTER=.kiro/settings/methodology/AGENTS.md; fi
POINTER_BEGIN='<!-- methodology:begin -->'
POINTER_END='<!-- methodology:end -->'
pointer_block() {
  printf '%s\n' \
    "$POINTER_BEGIN" \
    "Spec-driven work (\`\$kiro-*\` skills, \`.kiro/specs\`, \`.kiro/steering\`): read \`$ROUTER\` first. Other work does not need it." \
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
# A manifest of the names we placed lets a later run prune skills that were
# since removed (or renamed) upstream - otherwise link mode leaves dangling
# symlinks and copy mode leaves stale copies behind forever.
SKILLS_MANIFEST=.kiro/settings/.methodology-skills-manifest
skill_exists_in_src() { [ -d "$SRC/skills/$1" ]; }
prune_removed_skills() { # $1 = target skills dir
  dest=$1
  [ -f "$SKILLS_MANIFEST" ] || return 0
  while IFS= read -r old_name; do
    [ -n "$old_name" ] || continue
    skill_exists_in_src "$old_name" || rm -rf "$dest/$old_name"
  done < "$SKILLS_MANIFEST"
}
place_skills() { # $1 = target skills dir (.agents/skills or .claude/skills)
  dest=$1
  # migrate off a prior whole-directory symlink (or any non-directory) first - 
  # otherwise mkdir -p is a no-op and placing individual skills through it
  # would reach into methodology/skills/ itself via the old symlink.
  [ -d "$dest" ] && [ ! -L "$dest" ] || rm -f "$dest"
  mkdir -p "$dest"
  prune_removed_skills "$dest"
  for skill_dir in "$SRC"/skills/*/; do
    name=$(basename "$skill_dir")
    place "$dest/$name" "../../methodology/skills/$name" "$skill_dir"
  done
}
place_skills .agents/skills
place_skills .claude/skills
for skill_dir in "$SRC"/skills/*/; do basename "$skill_dir"; done > "$SKILLS_MANIFEST"

place .kiro/settings/templates ../../methodology/templates "$SRC/templates"
rm -rf .kiro/settings/methodology
if [ "$MODE" = copy ]; then mkdir -p .kiro/settings/methodology && cp "$SRC/AGENTS.md" .kiro/settings/methodology/AGENTS.md; fi

if [ "$MODE" = copy ]; then
  placed_dirs=".kiro/settings/templates .kiro/settings/methodology"
  for dest in .agents/skills .claude/skills; do
    for skill_dir in "$SRC"/skills/*/; do placed_dirs="$placed_dirs $dest/$(basename "$skill_dir")"; done
  done
  # shellcheck disable=SC2086
  write_files_manifest $placed_dirs
else
  rm -f "$FILES_MANIFEST"
fi
echo "installed ($MODE) into $ROOT"
