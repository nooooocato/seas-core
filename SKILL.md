---
name: seas-core
description: The foundational template for Self-Evolving Agent Skills (SEAS). Standardized for autonomous learning and safety.
version: 1.0.0
evolution:
  enabled: true
  meditation_threshold: 3
  test_command: "python3 scripts/verify_integrity.py"
  max_loops: 2
  max_history_size: 100MB
---

# SEAS Core Template

This skill implements the Self-Evolving Agent Skill specification. It is designed to be a "living" instruction set that improves based on its own execution history.

## Guidelines

- **Always Log**: Create a journal entry for ANY non-trivial failure or complex success.
- **Fact vs. Reason**: Keep `case.md` objective and `experience.md` subjective.
- **Verification is Mandatory**: NEVER commit an evolution change without passing `test_command`.
- **Snapshot Before Change**: Before editing instructions or scripts, ensure a backup exists or use the archival system to track state.

## Procedures

### Phase 1: Journaling (Real-time)
If an error occurs or a new pattern is discovered:
1. `mkdir -p journals/$(date +%Y%m%d-%H%M%S)`
2. Document the facts in `case.md`.
3. Document the reasoning/fix in `experience.md`.

### Phase 2: Meditation (Triggered)
If `count(journals/) >= meditation_threshold`:
1. **Aggregate**: Run `python3 scripts/meditate.py`.
2. **Analyze**: Read the aggregated report and identify patterns.
3. **Decide**: Choose to `UPDATE` (instructions), `FIX` (code), or `DEFER` (wait for more data).

### Phase 3: Action & Verification
1. **Execute**: Apply the chosen changes to `SKILL.md`, `scripts/`, or `references/`.
2. **Verify**: Run `python3 scripts/verify_integrity.py`.
3. **Rollback**: If verification fails, revert changes and log the failure.

### Phase 4: Archival
1. **Archive**: After successful verification, run `python3 scripts/archive.py` to move processed journals to long-term storage and update `archives/HISTORY.md`.
