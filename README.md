# 🌊 SEAS Core

> **The foundational template for Self-Evolving Agent Skills (SEAS).**  
> Standardized for autonomous learning, metacognition, and safety.

---

## 🚀 Quick Start

SEAS Core enables AI agents to transcend static instructions by implementing a **Metacognition Loop**:
- **Journal**: Record objective facts and subjective reasoning.
- **Meditate**: Analyze history to identify growth patterns.
- **Evolve**: Self-patch instructions and scripts.
- **Verify**: Guarantee system integrity via automated testing.

---

## 📂 Skill Structure

The following structure defines a SEAS-compliant skill. Items marked as **Mandatory** are required for the self-evolution engine to function.

```text
seas-core/
├── 📄 SKILL.md            [Mandatory]  # Primary instructions & Evolution metadata
├── 📁 scripts/            [Mandatory]  # Logic for meditation, verification, and archival
├── 📁 journals/           [Mandatory]  # Short-term memory (Cases & Experiences)
├── 📁 archives/           [Mandatory]  # Long-term memory (History & Snapshots)
├── 📁 references/         [Mandatory]  # Knowledge base and specifications
│   └── 📘 Meta-Specification.md         # The blueprint for self-evolution
└── 📁 assets/             [Optional]   # Static resources (images, icons, etc.)
```

---

## 🔄 The Metacognition Loop

1. **Real-time Journaling**: Every failure or complex success is logged in `journals/`.
2. **Periodic Meditation**: When the threshold is met, the agent aggregates and analyzes journals.
3. **Verified Evolution**: The agent applies improvements and verifies them against `scripts/verify_integrity.py`.
4. **Permanent Archival**: Processed journals are archived into `archives/` with a full rollback snapshot.

---

## 📘 Technical Reference

For a deep dive into the architectural constraints, safety protocols, and implementation details, please refer to the:

👉 **[Meta-Specification (Internal Link)](references/Meta-Specification.md)**

---

## 🛠️ Development Note

This project is a living experiment, co-architected by a human developer and the **Gemini CLI Agent**. It demonstrates the power of agent-led system evolution.

---

## ⚖️ License

Licensed under the Apache License, Version 2.0. See the `LICENSE` file for details.
