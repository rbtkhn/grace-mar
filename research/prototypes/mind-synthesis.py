"""
Simple templating synthesis for three-lens output (WORK only; draft).
Run after the three analytical lenses; output is draft until operator approves.
In production: may call LLM wrapper; see docs/skill-work/work-strategy/synthesis-engine.md.
"""


def synthesize_minds(
    mearsheimer_text: str, mercouris_text: str, barnes_text: str
) -> str:
    """
    Simple templating synthesis (expand later with grace-mar-llm.txt prompt).
    In production: call your LLM wrapper here.
    """
    convergence = (
        "High (energy infrastructure as primary lever in multipolar conflicts)"
    )
    tensions = [
        "- Mearsheimer: Predicts prolonged structural grind due to security dilemma",
        "- Mercouris: Highlights Iran's asymmetric resilience delaying decisive outcomes",
        "- Barnes: Flags domestic U.S. fractures & elite incentives creating earlier off-ramps",
    ]
    synthesis = (
        "Grace-Mar Synthesis: This escalation underscores systemic fragility in global energy security. "
        "Military actions accelerate multipolar realignments, but exhaustion and domestic pressures may force de-escalation. "
        "Individuals can stay curious by tracking independent maritime data and neutral diplomacy channels."
    )
    return (
        f"**Convergence**: {convergence}\n**Productive Tensions**:\n"
        + "\n".join(tensions)
        + f"\n**Grace-Mar Synthesis**: {synthesis}"
    )
