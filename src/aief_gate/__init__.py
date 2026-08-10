"""Mechanical evaluation of the LC-M04-EXIT criteria C1-C7.

WHY THIS EXISTS
---------------
`GATES.md` declares C1-C7 *"binary and evidence-based"*. Until now they were
evaluated by hand and written into prose. This repository has a recorded history
of exactly that failing: `VER-014` found four rounds of hand-written status
labels that had gone stale because nothing recomputed them, and `OI-V-02` records
the general form - **a declared property with no standing check is a property
that drifts.**

So the gate is computed, not asserted. `python -m aief_gate` prints one line per
criterion with the evidence it rests on, and exits non-zero if any criterion is
not PASS. A cold session reproduces the verdict without reading this
conversation, which is what the LC-M04 handoff requires.

WHAT IS AND IS NOT MECHANICAL
-----------------------------
C1-C4, C5 and C7 are fully mechanical: existence, schema conformance, digest
reproduction, approval-chain state and register membership are all decidable from
repository bytes.

C6 is **not** fully mechanical and is not pretended to be. A machine can confirm
that a verification report exists for each disposition and that its verifier
identity differs from the author identity; it cannot confirm that the verifier
obtained its evidence itself. The checker reports what it verified and names the
residue as requiring the QA reading. Reporting a judgement it did not make would
be the defect this module exists to prevent.
"""

from .criteria import Criterion, GateReport, evaluate  # noqa: F401

__all__ = ["Criterion", "GateReport", "evaluate"]
