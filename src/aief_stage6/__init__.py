"""aief_stage6 - deterministic Compiler Stage 6 increment for AIEF 1.0.0.

Actor provenance: software.software-engineer - S-2026-08-08-07 (AMD-20 form).
Dispatch: CMP-BLOCK-004 minimum deterministic Stage 6 increment per
AIEF-AMD-010 (AMD-25..AMD-33) and AIEF-AMD-012 (AMD-39/AMD-40).

Normative sources (every behaviour in this package traces to one of these):

- framework/framework.manifest.json  metadata.reproducible
  (digest_constructions DC-1..DC-5, tokenizer_families TF-1/TF-2,
  budget_measurement_record, distributable, build_time_reproducibility),
  schemas[sch-core-manifest], validation V-01..V-25, generation_order[6].
- framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md
- framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md
- .ai/project/BINDING.md, .ai/project/FROZEN.md, .ai/project/STATE.md
- .ai/core/schemas/SCH-core-manifest.schema.json

This package NEVER writes into .ai/**, framework/** or spec/** (read-only
inputs; enforced by paths.assert_write_allowed). All build output goes to
build/stage6/** and is PREVIEW output: no canonical core/MANIFEST.lock, no
BINDING pin write, no ledger entry (Stage 6 execution remains unauthorized,
OQ-14).
"""

__version__ = "0.1.0"
