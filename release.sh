#!/usr/bin/env sh
# Usage: release.sh X.Y.Z -m "tag body" [--dry-run]
# Checks, runs tests, writes VERSION, commits, tags vX.Y.Z (annotated), pushes main with the tag. Rules: RELEASING.md
set -eu
cd "$(dirname "$0")"

NEW=; BODY=; DRY=0
while [ $# -gt 0 ]; do
  case $1 in
    -m) [ $# -ge 2 ] || { echo "-m needs a tag body" >&2; exit 2; }; BODY=$2; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *) NEW=$1; shift ;;
  esac
done

die() { echo "release: $*" >&2; exit 1; }

printf '%s\n' "$NEW" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' || die "usage: $0 X.Y.Z -m \"tag body\" [--dry-run]"
[ "$DRY" = 1 ] || [ -n "$BODY" ] || die "tag body is required: -m \"user-visible changes\""

[ "$(git branch --show-current)" = main ] || die "release only from main"
[ -z "$(git status --porcelain)" ] || die "working tree is not clean"
git fetch -q --tags origin
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || die "main differs from origin/main (pull or push first)"
git rev-parse -q --verify "refs/tags/v$NEW" >/dev/null && die "tag v$NEW already exists"

CUR=0.0.0; [ -f VERSION ] && CUR=$(tr -d '[:space:]' < VERSION)
[ "$CUR" != "$NEW" ] || die "VERSION is already $NEW"
TOP=$(printf '%s\n%s\n' "$CUR" "$NEW" | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)
[ "$TOP" = "$NEW" ] || die "$NEW is not greater than $CUR"

LAST=$(git describe --tags --abbrev=0 2>/dev/null || true)
echo "release: $CUR -> $NEW (since ${LAST:-the first commit})"
git log --oneline ${LAST:+"$LAST"..}HEAD | head -40

python3 -m unittest tests/doc-lint/test_doc_lint.py >/dev/null 2>&1 || die "tests failed: python3 -m unittest tests/doc-lint/test_doc_lint.py"
echo "release: tests passed"

[ "$DRY" = 0 ] || { echo "release: dry run, nothing written"; exit 0; }

printf '%s\n' "$NEW" > VERSION
git add VERSION
git commit -q -m "agentic-psdd $NEW"
git tag -a "v$NEW" -m "$BODY"
git push origin main "v$NEW"
echo "release: v$NEW pushed"
