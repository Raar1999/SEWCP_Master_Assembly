"""Approval-chain integrity for frozen artifacts.

WHY THIS MODULE EXISTS
----------------------
`LAW-10` clause 2: *"An approval is invalidated automatically when the bound
content hash changes."* An approval binds a **whole-file** DC-1 digest. When two
ECRs disposition against the same frozen volume in sequence, the second
approval's edit changes the file and so invalidates the first approval - even
though the second change was itself lawful and approved.

That is not a bookkeeping nuisance. `LC-M04-EXIT` criteria C1-C4 read, verbatim,
*"the approval `subject_hash` does not reproduce"* as a FAIL. `spec/01` alone
carries dispositions for ECR-D-001, D-002, D-003, D-004 and D-007. Under the
literal reading at most **one** of those criteria can pass at any instant, and
which one depends on edit order. The gate is unsatisfiable by construction, and
re-approving every prior ECR at each new digest is O(ECRs x edits) and breaks
again on the next edit.

THE INVARIANT THIS MODULE OWNS
------------------------------
The human owner ruled (session S-2026-08-10-01, recorded at `GATES.md`
Supersession of approvals) that an approval carries one of three states against
the live tree:

  LIVE               subject_hash == DC-1(subject_path) in the working tree.
  SUPERSEDED-VALID   an unbroken chain of approvals on the same subject_path,
                     each carrying prior_hash equal to its predecessor's
                     subject_hash, leads from it to a LIVE approval.
  VOID               neither.

C1-C4 are satisfied by LIVE **or** SUPERSEDED-VALID. VOID fails.

The relation is stable under future edits: every lawful change appends a link,
so every earlier approval stays reachable. It is not satisfiable by an unlawful
change: an edit with no approval leaves no LIVE approval on that path at all,
and the whole chain collapses to VOID at once. That is the property the check
below is written to enforce, and `tests/test_approval_chain.py` attacks it
directly rather than only exercising the happy path.

WHAT THIS MODULE DELIBERATELY DOES NOT DO
-----------------------------------------
It does not decide authority, does not read the ECR's engineering content, and
does not re-implement DC-1. The digest construction has exactly one
implementation in this repository - `aief_stage6.digests.dc1_digest`, declared
normatively in `framework.manifest.json` - and a second copy here would be the
same drift defect that ECR-D-005 and ECR-D-006 already record. It is imported,
never re-derived.
"""

from .chain import (  # noqa: F401
    ApprovalRecord,
    ChainReport,
    PathChain,
    State,
    load_approvals,
    verify,
)

__all__ = [
    "ApprovalRecord",
    "ChainReport",
    "PathChain",
    "State",
    "load_approvals",
    "verify",
]
