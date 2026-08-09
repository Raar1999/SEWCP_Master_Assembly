"""AIEF execution layer - bounded task dispatch and result sharing.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Contract: `.ai/project/EXECUTION_ARCHITECTURE.md`, authorised by rank-1 decision
EXEC-D-001 (option A - project partition only). Every rule implemented here is a
restatement of a section of that contract; the citation is on the implementing
function.

This package writes nothing under `.ai/core/`, changes no manifest field and
touches no frozen artifact. It reads instance records in partition `project` and
reports.
"""

from __future__ import annotations

__all__ = [
    "records",
    "scope",
    "graph",
    "checks",
]

INDEX_PATH = ".ai/project/EXEC.md"
TASKS_DIR = ".ai/project/tasks"
RESULTS_DIR = ".ai/project/results"

#: EXECUTION_ARCHITECTURE.md section 5.2 - the framework-protected set. No task
#: write scope may reach these without an enumerated grant; AGENT-CONTRACT.md
#: section Prohibition, the manifest `partitions` write-access rules and LAW-01
#: already forbid them.
#:
#: `framework/**` was absent from the first draft of this tuple and VER-009
#: FIND-Q9-2 caught it: the frozen amendment set and `framework.manifest.json`
#: are rank-3 freeze-registry artifacts, and T-001's own forbidden actions named
#: them while X-04 could not see them. `project/ledger/**` is added on the same
#: ground - LAW-09 reserves ledger writes to session close.
PROTECTED_WRITE = (
    ".ai/core/**",
    ".ai/*.md",          # partition `root` - BOOT.md, FRAMEWORK.md, README.md are
                         # framework-only and generated; VER-009 FIND-Q9-2 second
                         # pass caught that `.ai/core/**` cannot see them
    "spec/**",
    "framework/**",
    ".ai/project/FROZEN.md",
    ".ai/project/approvals/**",
    ".ai/project/ledger/**",
)

#: EXECUTION_ARCHITECTURE.md section 4 - the task states, which are also the
#: level-2 headings of the index.
STATES = (
    "ACTIVE",
    "READY",
    "BLOCKED",
    "AWAITING-DECISION",
    "COMPLETE",
)

STATE_HEADINGS = {
    "Active": "ACTIVE",
    "Ready": "READY",
    "Blocked": "BLOCKED",
    "Awaiting decision": "AWAITING-DECISION",
    "Complete": "COMPLETE",
}
