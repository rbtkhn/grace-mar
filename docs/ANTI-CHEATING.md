# Anti-Cheating Framework

If the cognitive fork serves as a credential, it must be cheat-resistant.

## Attack Vectors

| Attack | Description | Severity |
|--------|-------------|----------|
| **Fabrication** | Create fake learning history retroactively | Critical |
| **Outsourcing** | Parent/tutor teaches instead of student | High |
| **Cramming** | Bulk upload right before evaluation | Medium |
| **Identity fraud** | Use someone else's fork | Critical |
| **AI ghostwriting** | Have ChatGPT generate content | High |
| **Collusion** | Share answers with peers | Medium |

## Defense Layers

### Layer 1: Temporal Integrity

Real learning happens over time. Fake learning is compressed.

| Defense | Mechanism |
|---------|-----------|
| Timestamped interactions | Cryptographically timestamped, cannot be backdated |
| Velocity limits | Flags anomalous growth patterns |
| Learning curves | Real learning shows struggle → mastery |
| Gap detection | Real students have breaks; robotic consistency is suspicious |

### Layer 2: Behavioral Fingerprinting

How you learn is as unique as what you learn.

| Defense | Mechanism |
|---------|-----------|
| Reasoning patterns | Fork encodes *how* student thinks |
| Error patterns | Real learners make characteristic mistakes |
| Interest trajectories | Authentic learners have organic evolution |
| Linguistic fingerprint | Word choices, sentence structures |
| Interaction patterns | Keystroke dynamics, pauses, corrections |

### Layer 3: Verification Touchpoints

Periodic real-world anchors that can't be outsourced.

| Defense | Mechanism |
|---------|-----------|
| Live sessions | Periodic video sessions, recorded |
| Proctored challenges | In-person or monitored problem-solving |
| Voice/face verification | Biometric confirmation |
| Third-party attestations | Teachers, mentors, parents |
| Random spot checks | Unpredictable verification |

### Layer 4: Anti-AI-Ghostwriting

Distinguish human teaching from AI generation.

| Defense | Mechanism |
|---------|-----------|
| Process capture | Record the *process*, not just output |
| AI detection | Apply detection models to teaching content |
| Inconsistency injection | Real humans are inconsistent; AI is too consistent |
| Challenge-response | Fork asks clarifying questions |
| Multimodal input | Voice, handwriting, sketches — harder for AI to fake |

### Layer 5: Cryptographic Integrity

The record cannot be altered after the fact.

| Defense | Mechanism |
|---------|-----------|
| Immutable log | Append-only, cannot delete or modify |
| Hash chains | Each entry references previous entries |
| Distributed attestation | Key milestones attested by multiple parties |
| Verifiable credentials | Third parties verify without accessing content |

### Layer 6: Query-Time Verification

The fork must perform, not just report.

| Defense | Mechanism |
|---------|-----------|
| Live querying | Evaluator asks novel questions |
| Depth probing | Follow-ups reveal shallow vs. deep knowledge |
| Transfer challenges | Apply knowledge to new domains |
| Explanation requests | "Why?" exposes real understanding |
| Comparative analysis | Compare fork responses to known student work |

## Trust Tiers

| Tier | Use Case | Verification Level |
|------|----------|-------------------|
| **Self-reported** | Personal growth | Timestamps only |
| **Attested** | Teacher confirms involvement | Social proof + timestamps |
| **Verified** | University admission | Biometrics + proctored + behavioral |
| **Certified** | Professional licensing | Full audit trail + attestation + demo |

## Comparison to Traditional Cheating

| Traditional | Cognitive Fork |
|-------------|----------------|
| Forge diploma (one document) | Fabricate 12 years of behavior (hard) |
| Pay someone for one exam | Impersonate for years (impractical) |
| Lie on CV (no verification) | Fork must perform on demand |
| Memorize for test (surface) | Fork must reason and transfer (deep) |

## Design Goal

Make authentic learning the path of least resistance:
- **Expensive** to fake (years of effort)
- **Risky** to fake (detection is likely)
- **Impractical** to fake (easier to just learn)

---

*Document version: 1.0*  
*Last updated: February 2026*
