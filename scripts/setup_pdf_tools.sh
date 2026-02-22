#!/usr/bin/env bash
# Download Pandoc and Tectonic for PDF rendering (no Homebrew required)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TOOLS_DIR="$REPO_ROOT/tools"
ARCH=$(uname -m)

# Map uname to download arch
if [[ "$ARCH" == "arm64" || "$ARCH" == "aarch64" ]]; then
  PANDOC_ARCH="arm64"
  TECTONIC_ARCH="aarch64"
else
  PANDOC_ARCH="x86_64"
  TECTONIC_ARCH="x86_64"
fi

mkdir -p "$TOOLS_DIR"
cd "$TOOLS_DIR"

# Pandoc 3.9
PANDOC_DIR="pandoc-3.9-${PANDOC_ARCH}"
if [[ ! -x "$TOOLS_DIR/$PANDOC_DIR/bin/pandoc" ]]; then
  echo "Downloading Pandoc for $PANDOC_ARCH..."
  curl -sL -o pandoc.zip "https://github.com/jgm/pandoc/releases/download/3.9/pandoc-3.9-${PANDOC_ARCH}-macOS.zip"
  unzip -o pandoc.zip
  rm pandoc.zip
  echo "  → $TOOLS_DIR/$PANDOC_DIR/bin/pandoc"
else
  echo "Pandoc already present: $PANDOC_DIR"
fi

# Tectonic 0.15.0
if [[ ! -x "$TOOLS_DIR/tectonic" ]]; then
  echo "Downloading Tectonic for $TECTONIC_ARCH..."
  curl -sL -o tectonic.tar.gz "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-${TECTONIC_ARCH}-apple-darwin.tar.gz"
  tar -xzf tectonic.tar.gz
  rm tectonic.tar.gz
  echo "  → $TOOLS_DIR/tectonic"
else
  echo "Tectonic already present"
fi

echo ""
echo "Done. Run ./scripts/render_pdf.sh to generate PDFs."
