#!/usr/bin/env bash
# Push this manuscript to an Overleaf project through the git bridge,
# following skills/overleaf/SKILL.md (token via credential helper, never in a URL).
#
# Usage (on a machine where OVERLEAF_TOKEN is set):
#   bash push_to_overleaf.sh            # stops if any project file would be overwritten
#   FORCE=1 bash push_to_overleaf.sh    # overwrite those files
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-6b0524aa7e92e361ad0a03e0}"
BRANCH="ccr-b8438cc8-elhv3w"
REPO="https://github.com/Guylaban/My-stuff"
: "${OVERLEAF_TOKEN:?OVERLEAF_TOKEN is not set in this shell}"

ol() {
  git -c credential.helper= \
      -c credential.helper='!f() { echo "username=git"; echo "password=${OVERLEAF_TOKEN}"; }; f' "$@"
}

WORK="$(mktemp -d)"
echo "Working in $WORK"

# 1. Manuscript sources from GitHub (only this folder is needed).
git clone --quiet --depth 1 --branch "$BRANCH" "$REPO" "$WORK/src"
SRC="$WORK/src/manuscripts/thri-genai-evaluation"

# 2. The Overleaf project.
ol clone --quiet "https://git.overleaf.com/${PROJECT_ID}" "$WORK/overleaf"
DST="$WORK/overleaf"
echo "Current Overleaf project contents:"
(cd "$DST" && git ls-files | sed 's/^/  /')

FILES=(main.tex references.bib README.md supplementary/precision_planning.py)
while IFS= read -r f; do FILES+=("$f"); done < <(cd "$SRC" && ls sections/*.tex)

# 3. Refuse to overwrite different existing files unless FORCE=1.
conflicts=()
for f in "${FILES[@]}"; do
  if [ -e "$DST/$f" ] && ! cmp -s "$SRC/$f" "$DST/$f"; then conflicts+=("$f"); fi
done
if [ "${#conflicts[@]}" -gt 0 ] && [ "${FORCE:-0}" != "1" ]; then
  echo "These files already exist in the Overleaf project and differ:"
  printf '  %s\n' "${conflicts[@]}"
  echo "Nothing was pushed. Re-run with FORCE=1 to overwrite them."
  exit 1
fi

for f in "${FILES[@]}"; do
  mkdir -p "$DST/$(dirname "$f")"
  cp "$SRC/$f" "$DST/$f"
done

cd "$DST"
git add -A
if git diff --cached --quiet; then
  echo "Overleaf project already up to date."
  exit 0
fi
git -c user.name="$(git config user.name || echo Author)" \
    -c user.email="$(git config user.email || echo author@example.com)" \
    commit --quiet -m "Add THRI manuscript: Evaluate the Role, Not the Model"
ol push --quiet origin master
echo "Pushed to https://www.overleaf.com/project/${PROJECT_ID}"
echo "Set the main document to main.tex in Overleaf (Menu > Main document)."
echo "Working copy left at $WORK (delete with: rm -rf \"$WORK\")"
