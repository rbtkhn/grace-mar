#!/usr/bin/env python3
"""
Demo: CMC lookup integration.

Shows the lookup flow: LIBRARY → CMC → full LLM.
Run with CMC cloned and index built for a real demonstration.

  # Clone and build CMC first:
  git clone https://github.com/rbtkhn/civilization_memory.git repos/civilization_memory
  cd repos/civilization_memory && python3 tools/cmc-index-search.py build

  # Then run demo (set path if not sibling):
  CIVILIZATION_MEMORY_PATH=./repos/civilization_memory python3 scripts/demo_cmc_lookup.py

  # Full end-to-end (LIBRARY → CMC → REPHRASE) — requires OPENAI_API_KEY:
  CIVILIZATION_MEMORY_PATH=./repos/civilization_memory python3 scripts/demo_cmc_lookup.py --full

  # Test routing (off-scope question skips CMC):
  CIVILIZATION_MEMORY_PATH=./repos/civilization_memory python3 scripts/demo_cmc_lookup.py "how do you spell elephant"
"""

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


def main():
    from bot.lookup_cmc import query_cmc, _get_cmc_path, should_route_to_cmc

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    question = args[0] if args else "What did the Romans use aqueducts for?"
    full_demo = "--full" in sys.argv

    print(f"Question: {question}\n")

    cmc_path = _get_cmc_path()
    if cmc_path:
        print(f"CMC path: {cmc_path}")
        route = should_route_to_cmc(question)
        print(f"Route to CMC: {route} (scope match)")
        result = query_cmc(question, limit=3)
        if not route:
            print("\nCMC: skipped (question outside civilizational/historical scope)")
        elif result:
            print("\n--- CMC result (snippets passed to REPHRASE) ---\n")
            print(result[:1200] + ("..." if len(result) > 1200 else ""))
            print("\n--- End CMC ---")

            if full_demo and os.getenv("OPENAI_API_KEY"):
                print("\n--- Full flow: REPHRASE → Grace-Mar voice ---\n")
                from bot.core import _rephrase_lookup
                reply = _rephrase_lookup(question, result, channel_key="demo")
                print(reply)
            else:
                print("\n(Flow: LIBRARY miss → CMC hit → REPHRASE → reply)")
                if full_demo and not os.getenv("OPENAI_API_KEY"):
                    print("(Set OPENAI_API_KEY for --full REPHRASE)")
        elif route:
            print("\nCMC: No matches (index may need build, or topic not in corpus)")
            print("  Run: cd CMC && python3 tools/cmc-index-search.py build")
    else:
        print("CMC path: not found")
        print("\nSetup:")
        print("  1. Clone: git clone https://github.com/rbtkhn/civilization_memory.git repos/civilization_memory")
        print("  2. Build: cd repos/civilization_memory && python3 tools/cmc-index-search.py build")
        print("  3. Set:   export CIVILIZATION_MEMORY_PATH=$(pwd)/repos/civilization_memory")
        print("\nLookup flow when CMC is available:")
        print("  LIBRARY (books) → miss")
        print("  CMC (civilizational history) → query → snippets")
        print("  REPHRASE → Grace-Mar voice → reply")


if __name__ == "__main__":
    main()
