# Self-Evolving Agent Skill (SEAS) Specification
**Version:** 0.1.0 (Draft)  
**Status:** Experimental

## 1. Overview
The Self-Evolving Agent Skill (SEAS) is an extension of the standard Agent Skill specification. It introduces a "Metacognition Loop" that allows an agent to record execution failures (Cases) and reasoning paths (Experiences), and periodically synthesize these into permanent improvements (Evolution) without human intervention.

## 2. Directory Structure
A SEAS-compliant skill MUST adhere to the following directory structure:

```text
<skill-name>/
├── SKILL.md                 # Primary instructions (Mutable by Agent)
├── scripts/                 # Executable scripts (Mutable by Agent)
├── references/              # Static documentation (Mutable by Agent)
├── journals/                # [NEW] Short-term memory & failure logs
│   ├── <YYYYMMDD-HHMMSS>/   # Unique session ID
│   │   ├── case.md          # Objective facts (The "What")
│   │   └── experience.md    # Subjective reasoning (The "How")
│   └── ...
├── archives/                # [NEW] Long-term storage of processed journals
│   ├── HISTORY.md           # Global evolution log
│   ├── update-<timestamp>.zip
│   └── ...
└── assets/                  # Static resources (Optional)
```

## 3. Metadata Extensions
The `SKILL.md` YAML frontmatter MUST include the following extension fields to control the evolution behavior:

```yaml
---
name: my-evolving-skill
description: A skill that gets better over time.
# ... standard fields ...
evolution:
  enabled: true
  meditation_threshold: 3   # Number of journals required to trigger evolution
  test_command: "./test.sh" # [NEW] Command to verify skill integrity
  max_loops: 2              # [NEW] Max attempts to fix the same error fingerprint
  max_history_size: 50MB    # (Optional) Limit for the archives folder
---
```

## 4. The Journal System (Short-Term Memory)
When a skill encounters an error, unexpected behavior, or a complex success, it MUST generate a new directory in `journals/` using the format `YYYYMMDD-HHMMSS`.

### 4.1. case.md (Objective Reality)
Records the **facts** of the execution context. Must avoid inference.
*   **Format:** Markdown
*   **Required Sections:**
    *   `# Context`: System environment, input arguments, working directory.
    *   `# Trigger`: The specific user prompt or sub-agent call.
    *   `# Event`: Raw error logs, stack traces, or unexpected output.

### 4.2. experience.md (Subjective Cognition)
Records the **reasoning** and attempts to solve the case.
*   **Format:** Markdown
*   **Required Sections:**
    *   `# Attempted Solutions`: List of methods tried.
    *   `# Outcome`: Success or Failure.
    *   `# Confidence Level`:
        *   `Level 1 (Unknown)`: No clear understanding.
        *   `Level 2 (Hypothesis)`: Probable cause identified/Workaround found.
        *   `Level 3 (Solved)`: Root cause confirmed and fixed.

## 5. The Evolution Protocol (Metacognition)
This process is triggered automatically upon Skill activation if `count(journals) >= evolution.meditation_threshold`.

### 5.1. Meditation Phase (LLM-Driven)
1.  **Aggregation**: The agent executes a script (e.g., `scripts/meditate.py`) to aggregate content from all unprocessed journals.
2.  **Context Loading**: The content is loaded into the Agent's context.
3.  **LLM Analysis**: The Agent (LLM) analyzes the aggregated data to identify patterns, root causes, and necessary improvements, deciding which journals to act upon and which to defer.

### 5.2. Action Phase
The agent performs one of the following actions for each identified pattern:

*   **UPDATE (SKILL.md)**: Add new guidelines, constraints, or examples.
*   **FIX (Scripts)**: Patch bugs in `scripts/`.
*   **DOCUMENT (References)**: Create/Update `references/troubleshooting.md`.
*   **DEFER**: Leave the journal in `journals/` if the pattern is inconclusive.

### 5.3. Safety Mechanisms (New)
The evolution process must include checks to prevent regression and infinite loops.

#### 5.3.1. Verification (Sandbox Test)
*   **Requirement**: If `test_command` is defined in metadata, it MUST be executed after any `UPDATE` or `FIX` action.
*   **Success**: Proceed to Archival Phase.
*   **Failure**: 
    1.  **Rollback**: Revert changes to `SKILL.md` or `scripts/`.
    2.  **Record**: Create a new journal (Level 1) describing the failed evolution attempt.
    3.  **Abort**: Stop the current evolution cycle.

#### 5.3.2. Loop Detection (Fingerprinting)
*   **Fingerprint**: A hash or unique signature derived from the `case.md` error event.
*   **Check**: If the same fingerprint appears in `archives/HISTORY.md` or `journals/` more than `max_loops` times without successful resolution:
    *   **Action**: Mark as `DEFER`.
    *   **Notify**: Generate an `ALARM.md` in the root or notify the user for manual intervention.

### 5.4. Archival Phase
For all journals processed (excluding DEFER):
1.  **Snapshot**: Capture the state of `SKILL.md`, `scripts/`, or `references/` BEFORE any modifications were applied.
2.  **Generate Changelog**: Summary of what changed.
3.  **Package**: Create `archives/update-<timestamp>.zip` containing:
    *   The processed journal folders.
    *   The `changelog.md`.
    *   **The `pre-update-snapshot/` folder** containing the original files before modification.
4.  **Update History**: Append the changelog entry to `archives/HISTORY.md`.
5.  **Cleanup**: Delete the processed folders from `journals/`.

## 6. Implementation Guidelines
*   **Safety**: The evolution process MUST NOT delete the `SKILL.md` entirely. It should prefer appending or precise replacement.
*   **Atomic**: The `Action Phase` should try to be atomic. If possible, backup files before modification.
*   **Transparency**: The `HISTORY.md` serves as an audit trail. It must be human-readable.
