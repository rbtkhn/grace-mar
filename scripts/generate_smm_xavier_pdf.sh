#!/usr/bin/env bash
# Regenerate print HTML + PDF for Xavier: full training pack (mission + handbook + key materials).
# Uses smm-xavier-handbook-bundle.md (built from repo sources). macOS: Chrome headless.
#
# Environment
# - Run on a normal macOS host with Google Chrome or Chromium installed. Headless Chrome often
#   aborts or fails in sandboxed/CI/agent environments that restrict GPU/display; if PDF step fails,
#   run this script locally or open the generated HTML in a browser → Print → Save as PDF.
#
# Noise
# - Chrome may spew benign stderr (display link, GCM, updater). By default stderr is suppressed
#   for the print step only. Set CHROME_PDF_VERBOSE=1 to see full Chrome stderr for debugging.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$REPO_ROOT/scripts/build_xavier_handbook_bundle.py"
MD="$REPO_ROOT/docs/skill-work/work-politics/smm-xavier-handbook-bundle.md"
HTML="$REPO_ROOT/docs/skill-work/work-politics/smm-xavier-handbook-bundle-print.html"
PDF="$REPO_ROOT/docs/skill-work/work-politics/smm-xavier-handbook-bundle.pdf"

python3 "$REPO_ROOT/scripts/handbook_md_to_print_html.py" "$MD" -o "$HTML"

CHROME=""
for c in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
  if [[ -x "$c" ]]; then CHROME="$c"; break; fi
done

if [[ -z "$CHROME" ]]; then
  echo "Chrome not found. Open this file in a browser and Print → Save as PDF:"
  echo "  $HTML"
  exit 0
fi

chrome_pdf() {
  "$CHROME" --headless=new --disable-gpu --disable-logging --no-pdf-header-footer \
    --print-to-pdf="$PDF" "file://$HTML"
}

if [[ -n "${CHROME_PDF_VERBOSE:-}" ]]; then
  chrome_pdf
else
  chrome_pdf 2>/dev/null
fi

if [[ ! -s "$PDF" ]]; then
  echo "error: PDF missing or empty: $PDF" >&2
  echo "hint: run on macOS with Chrome, or set CHROME_PDF_VERBOSE=1 and retry to see Chrome stderr." >&2
  exit 1
fi

echo "Wrote $PDF"
