"""Computed feature-clearance verification for the SEWCP clocking map.

WHY THIS EXISTS
---------------
`spec/00` §3.2 declares the feature clocking map *"binding on every component"*
and closed with a prose line reading **"No conflicts."** That line checked four
hand-picked pairs. It omitted the Ø260 BC kinematic locators entirely, and as a
result three of the twelve outer choke stations sat on the same three rays as the
three top locators, with the Ø12.000 counterbore overlapping the M5 slot by
4.5 mm radially and the Ø22 washer pad almost completely. **ECR-D-010.**

The defect is not the collision. The defect is that a claim of "no conflicts" was
recorded, believed and frozen without anything ever computing it — the same shape
as `OI-V-02` (a registry with no check) and as the approval-supersession problem
`aief_approval` addresses. So the claim is now computed.

WHAT IT DOES
------------
It reads the clocking map out of `spec/00` §3.2 — so the frozen specification
remains the input, not a copy of it — pairs it with a declared footprint table,
and computes the minimum centre distance for every pair of features that share a
face. A pair fails when that distance is less than the sum of the two footprint
radii plus the declared minimum wall.

WHAT IT DOES NOT DO
-------------------
It is a planar clearance check over circular and radially-slotted footprints on a
shared face. It is not a solid modeller: it does not reason about depth except
through the coarse `face` key, and it will not find an interference between two
features on the same face at different depths that do not overlap axially. Those
are reported as pairs to inspect rather than silently passed. The intent is to
make the *class* of defect ECR-D-010 belongs to impossible to freeze unnoticed,
not to replace CAD interference checking.
"""

from .check import Feature, Finding, check, load_map  # noqa: F401

__all__ = ["Feature", "Finding", "check", "load_map"]
