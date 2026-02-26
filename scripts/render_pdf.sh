#!/usr/bin/env bash
# Render Grace-Mar White Paper and Business Prospectus to PDF
# Uses Pandoc + Eisvogel template. See docs/pdf-setup.md for prerequisites.
# Can use bundled tools (tools/) when Homebrew is not available.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$REPO_ROOT/docs"
OUTPUT_DIR="${OUTPUT_DIR:-$DOCS_DIR}"
ARCH=$(uname -m)

# Prefer system pandoc; fall back to bundled
if command -v pandoc &>/dev/null; then
  PANDOC_CMD=pandoc
elif [[ -x "$REPO_ROOT/tools/pandoc-3.9-x86_64/bin/pandoc" ]] && [[ "$ARCH" == "x86_64" ]]; then
  PANDOC_CMD="$REPO_ROOT/tools/pandoc-3.9-x86_64/bin/pandoc"
elif [[ -x "$REPO_ROOT/tools/pandoc-3.9-arm64/bin/pandoc" ]] && [[ "$ARCH" == "arm64" ]]; then
  PANDOC_CMD="$REPO_ROOT/tools/pandoc-3.9-arm64/bin/pandoc"
else
  PANDOC_CMD=""
fi

# Prefer xelatex; fall back to bundled Tectonic
if command -v xelatex &>/dev/null; then
  PDF_ENGINE=xelatex
elif [[ -x "$REPO_ROOT/tools/tectonic" ]]; then
  PDF_ENGINE="$REPO_ROOT/tools/tectonic"
else
  PDF_ENGINE=""
fi

# Pandoc template locations (in order of precedence)
PANDOC_DATA="${PANDOC_DATA_DIR:-$HOME/.local/share/pandoc}"
if [[ -d "$HOME/.pandoc" ]]; then
  PANDOC_DATA="$HOME/.pandoc"
fi
EISVOGEL="$PANDOC_DATA/templates/eisvogel.latex"

# Eisvogel install URL (latest release)
EISVOGEL_URL="https://github.com/Wandmalfarbe/pandoc-latex-template/releases/download/v3.4.0/Eisvogel-3.4.0.tar.gz"

install_eisvogel() {
  echo "Installing Eisvogel template..."
  mkdir -p "$PANDOC_DATA/templates"
  local tmpdir
  tmpdir=$(mktemp -d)
  if curl -sL "$EISVOGEL_URL" -o "$tmpdir/eisvogel.tar.gz" 2>/dev/null; then
    tar -xzf "$tmpdir/eisvogel.tar.gz" -C "$tmpdir"
    local tpl
    tpl=$(find "$tmpdir" -name "eisvogel.tex" -o -name "eisvogel.latex" 2>/dev/null | head -1)
    if [[ -n "$tpl" && -f "$tpl" ]]; then
      cp "$tpl" "$PANDOC_DATA/templates/eisvogel.latex"
      echo "Eisvogel installed to $PANDOC_DATA/templates/eisvogel.latex"
    else
      echo "Could not find template in archive. Try manual install: $EISVOGEL_URL"
      exit 1
    fi
    rm -rf "$tmpdir"
  else
    echo "Failed to download Eisvogel. Install manually: $EISVOGEL_URL"
    exit 1
  fi
}

render() {
  local input="$1"
  local output="$2"
  local title="$3"
  local subtitle="$4"

  local template_args=()
  if [[ -f "$EISVOGEL" ]]; then
    template_args=(--template="$EISVOGEL" -V toc-title="Contents" -V book=false)
  else
    echo "Note: Eisvogel not found. Use './scripts/render_pdf.sh --install-eisvogel' to install."
    echo "Rendering with default template..."
  fi

  "$PANDOC_CMD" "$input" -o "$output" \
    --pdf-engine="$PDF_ENGINE" \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    -V colorlinks=true \
    -V title="$title" \
    -V subtitle="$subtitle" \
    -V author="Grace-Mar" \
    -V date="February 2026" \
    --toc \
    --toc-depth=3 \
    --number-sections \
    "${template_args[@]}"

  echo "  → $output"
}

# Parse args
if [[ "${1:-}" == "--install-eisvogel" ]]; then
  install_eisvogel
  exit 0
fi

# Check prerequisites
if [[ -z "$PANDOC_CMD" ]]; then
  echo "Error: pandoc not found."
  echo "  - With Homebrew: brew install pandoc"
  echo "  - Without Homebrew: run ./scripts/setup_pdf_tools.sh to download bundled Pandoc"
  exit 1
fi

if [[ -z "$PDF_ENGINE" ]]; then
  echo "Error: no PDF engine (xelatex or Tectonic) found."
  echo "  - With Homebrew: brew install --cask mactex-no-gui"
  echo "  - Without Homebrew: run ./scripts/setup_pdf_tools.sh to download bundled Tectonic"
  exit 1
fi

# Render
echo "Rendering PDFs..."
echo ""

render \
  "$DOCS_DIR/WHITE-PAPER.md" \
  "$OUTPUT_DIR/WHITE-PAPER.pdf" \
  "Grace-Mar White Paper" \
  "Identity Infrastructure for the Agent Web"

render \
  "$DOCS_DIR/BUSINESS-PROSPECTUS.md" \
  "$OUTPUT_DIR/BUSINESS-PROSPECTUS.pdf" \
  "Grace-Mar — Business Prospectus" \
  "Identity Infrastructure for the Agent Web"

echo ""
echo "Done. PDFs written to $OUTPUT_DIR/"
