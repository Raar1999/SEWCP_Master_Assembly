# SEWCP-200 · MDR-001 — Coolant Channel Routing Topology

**Component:** 01 — Cooling Plate · **Part Number:** SEWCP-200
**Record class:** Modelling decision record (`implementation/*/cad/`, per `implementation/README.md`)
**Raised by:** `mechanical.cad-engineer`
**Decided by:** human owner, live rank-1 instruction
**Date:** 2026-08-10
**Affects:** implementation package §5 sketch `S3`; §6 step `6.09`; feature-strategy rows 06–07

---

## 1 · Why a decision was required

`spec/01` §3.1 delegates the routing and specifies no centreline:

> "CAD shall route the serpentine to satisfy the table **before** optimizing for path length."

The frozen baseline therefore fixes the *constraints* on the channel but not its *topology*.
Selecting a topology changes compliance with `CP-11` (radial temperature uniformity ≤ 1.5 °C
across Ø280 at 3 kW) and with `CP-02` (4.0 L/min at ΔP < 1.5 bar), so it is an engineering
decision. `AGT-cad-engineer` forbids this role from making one; it was escalated and ruled.

`spec/01` §2.1 already records that `CP-02`'s ΔP is **not re-derived** after `ECR-D-002` and
"shall be verified before build release". **This decision does not close that.**

## 2 · Decision

**Concentric bifilar (counterflow) arc serpentine.**

Supply and return are interleaved radially so that each pass is flanked by passes at a
different point in the 10.8 K coolant rise, rather than running monotonically inward.

Grounds:

- `CP-IF-10` places both ports at r = 125.0, only 30° apart (255° inlet, 285° outlet). The
  circuit is therefore necessarily **out-and-back**, and a bifilar interleave is the only
  arrangement of that family that never crosses itself in a single milled plane.
- `CP-11` is a **radial** uniformity requirement against a 10.8 K coolant rise. Counterflow
  pairing holds the local radial mean roughly flat; sequential inward routing would impose the
  full rise as a monotonic radial gradient.
- Concentric arcs are co-ordinate with the exclusion pattern, which is itself organised on bolt
  circles, so keep-out compliance reduces largely to a radius comparison.

Rejected: bifilar Archimedean spiral (lowest ΔP, but pitch must open locally at the lift-pin
stations and path length is set by the wind rather than by the design basis); bifilar chordal
boustrophedon (simplest CAM, but pass length varies with the chord, giving an azimuthal
gradient — the weakest fit to a radial uniformity requirement).

## 3 · Constraint set — derived, not chosen

Channel width `ch_width` = 10.0, so **centreline clearance = keep-out radius + 5.0**.

| Feature | Axis r | Azimuths | Keep-out (to wall) | Source |
|---|---|---|---|---|
| Central He bore | 0 | — | 15.0 | `spec/01` §3.1 |
| HV feed bores | 30 | 0°, 180° | 12.0 | `spec/01` §3.1 |
| RTD port 1 | 40 | 75° | 6.0 | `spec/01` §3.1 |
| Inner choke fasteners | 45 | 45/135/225/315° | 8.0 | `spec/01` §3.1 |
| Lift pin bores | 100 | 30/150/270° | 12.0 | `spec/01` §3.1 |
| RTD port 2 | 100 | 165° | 6.0 | `spec/01` §3.1 |
| Top kinematic locators | 130 | 75/195/315° | 8.5 | `spec/01` §3.1 (`ECR-D-007` action 1) |
| Outer choke fasteners | 135 | 0°+n·30° | 8.0 | non-binding — wall limit r 127 lies outboard of the envelope |
| RTD port 3 | 140 | 225° | 6.0 | outside envelope |
| Ring taps / bottom locators / RF land | 151 / 153 / 128–146 | — | — | outside envelope |
| Plate OD and external surfaces | 160 | — | 5.0 | non-binding |

Envelope: channel wall confined to r 30.0 → 125.0 (`ch_env_id`/`ch_env_od`), and to
**r ≤ 121.5** at 75°/195°/315° where the locator row governs.
Geometry limits: `ch_bend_r` 5.0 minimum centreline bend, `ch_corner_r` 3.0 minimum corner.
Port pockets: channel locally deepened to `ch_depth_port` 10.00, ramped back to 6.00 over 15 mm.

## 4 · Consequence that must be respected in S3

Solving the table above for a **constant-radius** pass centreline `rc` gives:

```
envelope                35.0 <= rc <= 120.0
top locators                    rc <= 116.5      (wall <= 121.5)
lift pins               rc <= 83.0  or  rc >= 117.0
inner choke             rc <= 32.0  or  rc >=  58.0
RTD @ r=40                              rc >=  51.0
HV bores                                rc >=  47.0
-----------------------------------------------------------
feasible                58.0 <= rc <= 83.0        (25 mm band)
outboard band           rc >= 117.0 AND rc <= 116.5   -> EMPTY
```

Two results follow, and both are checkable:

1. **No constant-radius pass can exist outboard of the lift-pin circle.** The band closes by
   0.5 mm — squeezed between the 12.0 mm lift-pin keep-out at r = 100 and the 121.5 mm locator
   wall limit. The outermost pass must be locally modulated: pushed out ≈ 0.5 mm at 30°/150°/270°,
   or pulled in at 75°/195°/315°. Either is a shallow, R5-compliant waviness.
2. **The two constant-radius passes cannot reach the design basis alone.** At rc = 63.0 and
   78.0 (5.0 mm rib) they develop 2π(63 + 78) ≈ **886 mm** against the ≈ 2.2 m of `spec/01`
   §2.1. The balance must come from the outboard region, which is precisely the region that
   requires the weave. This is the intended reading of §3.1: satisfy the table first, then
   recover path length.

**Superseded working figure.** The illustrative schedule offered at the point of decision —
four passes at r = 115/95/75/55, 20 mm pitch, ≈ 2136 mm — **fails this check**: the r = 115 and
r = 95 passes both foul the 12.0 mm lift-pin keep-out at r = 100. It is recorded here only so
it is not re-derived. **No pass radius is fixed by this record.**

## 5 · What remains open

The **pass schedule** — count, radii, rib widths, crossover azimuths, and the local deviations
at the three lift-pin stations — is a *derivation* against §3, to be closed in sketch `S3` at
step 6.09 with the geometry present, and verified at `G-19`, `G-20` and `M-07`.

Rib width between adjacent channel passes is not constrained by any frozen artifact. If the FSW
internal-rib passes require a minimum rib for tool shoulder engagement, that is a manufacturing
input this record does not have, and it will be raised as an ECR-Q rather than assumed.

## 6 · Traceability

| Cites | |
|---|---|
| `spec/01` §2.1 | Design basis: 10 × 6 section, Re ≈ 8,300, ≈ 2.2 m developed path, ΔT 10.8 K, ΔP open |
| `spec/01` §3.1 | Keep-out table, envelope, delegation of routing to CAD |
| `spec/01` `CP-IF-10` | Port positions, radii and local deepening |
| `spec/01` `CP-05`, `CP-11`, `CP-02` | Proof pressure, uniformity, flow requirements |
| `implementation/01_.../SEWCP-200_CAD_Implementation_Package.md` | §5 `S3`, §6 step 6.09 |

Introduces no dimension, interface or material not traceable to `spec/**`
(`implementation/README.md` rule 1).
